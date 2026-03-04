from datetime import date

from fastapi import APIRouter, Depends, Query, Request
from fastapi.responses import HTMLResponse
from sqlmodel import Session, func, select

from party_app.dependency import Templates, get_session
from party_app.models import Party


router = APIRouter(prefix="", tags=["parties"])

_PAGE_SIZE = 6


@router.get("/", name="party_list_page", response_class=HTMLResponse)
def party_list_page(
    request: Request,
    templates: Templates,
    session: Session = Depends(get_session),
    page: int = Query(1, ge=1),
):
    today = date.today()

    # How many parties in the future there are in total
    num_all_parties = session.exec(
        select(func.count(Party.uuid)).where(Party.party_date >= today)
    ).one()

    # Calculate the offset for the current page
    offset = (page - 1) * _PAGE_SIZE

    # Get the parties for the current page (parties between OFFSET and OFFSET + PAGE_SIZE)
    parties = session.exec(
        select(Party).where(Party.party_date >= today).offset(offset).limit(_PAGE_SIZE)
    ).all()

    # Get next page if there are still parties to be loaded
    next_page = page + 1 if (offset + _PAGE_SIZE) <= num_all_parties else None

    # Check if the request is an HTMX Request
    htmx_request = request.headers.get("HX-Request", None)

    # Based on whether it's an HTMX request or not, return the correct template
    if htmx_request:
        template_name = "party_list/partial_party_list.html"
    else:
        template_name = "party_list/page_party_list.html"

    # Return the correct template with part of the parties and info on which page to load next, if it exists
    return templates.TemplateResponse(
        request=request,
        name=template_name,
        context={"parties": parties, "next_page": next_page},
    )
