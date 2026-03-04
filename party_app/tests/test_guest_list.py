from typing import Callable

import pytest

from fastapi import status
from fastapi.testclient import TestClient
from sqlmodel import Session

from party_app.main import app
from party_app.models import Guest, Party


# Ensures the endpoint returns the correct guest list for the party and that the party ID is passed to the template
def test_guest_list_page_lists_guests_for_party_by_id(
        session: Session,
        client: TestClient,
        create_party: Callable[..., Party],
        create_guest: Callable[..., Guest],
):
    party = create_party(session=session)
    guest_1 = create_guest(session=session, name="Alice", party=party)
    guest_2 = create_guest(session=session, name="Bob", party=party)

    another_party = create_party(session=session, venue="Another venue")
    create_guest(session=session, party=another_party)

    url = app.url_path_for("guest_list_page", party_id=party.uuid)
    response = client.get(url)

    assert response.status_code == status.HTTP_200_OK
    assert list(response.context["guests"]) == [guest_1, guest_2]
    assert response.context["party_id"] == party.uuid


# Ensures that guest passed in the PUT request are marked as attending and the whole list is returned
def test_mark_guests_attending_updates_guests_returns_whole_list(
        session: Session,
        client: TestClient,
        create_party: Callable[..., Party],
        create_guest: Callable[..., Guest],
):
    # None of the guests are marked as attending
    party = create_party(session=session)
    guest_1 = create_guest(session=session, party=party, attending=False)
    guest_2 = create_guest(session=session, party=party, attending=False)

    url = app.url_path_for(
        "mark_guests_attending_partial", party_id=party.uuid,
    )
    # Send UUID of the first guest to the endpoint to mark them as attending
    response = client.put(url, data={"guest_ids": [guest_1.uuid]})

    # Refresh the guest objects from the database
    session.refresh(guest_1)
    session.refresh(guest_2)

    # Both guests were marked as NOT attending before. After the PUT request, only the first guest should be marked as attending.
    assert guest_1.attending is True
    assert guest_2.attending is False

    # We expect the endpoint to return whole guest list, not just the updated guests
    assert response.status_code == status.HTTP_200_OK
    assert response.context["guests"] == [guest_1, guest_2]


# Ensures that guest passed in the PUT request are marked as NOT attending and the whole list is returned
def test_mark_guests_not_attending_updates_guests_returns_whole_list(
        session: Session,
        client: TestClient,
        create_party: Callable[..., Party],
        create_guest: Callable[..., Guest],
):
    # Both guests are marked as attending
    party = create_party(session=session)
    guest_1 = create_guest(session=session, party=party, attending=True)
    guest_2 = create_guest(session=session, party=party, attending=True)

    url = app.url_path_for(
        "mark_guests_not_attending_partial", party_id=party.uuid,
    )
    # Send UUID of the first guest to the endpoint to mark them as NOT attending
    response = client.put(url, data={"guest_ids": [guest_1.uuid]})

    # Refresh the guest objects from the database
    session.refresh(guest_1)
    session.refresh(guest_2)

    # Both guests were marked as attending before. After the PUT request, the first guest should be marked as NOT attending.
    assert guest_1.attending is False
    assert guest_2.attending is True

    # We expect the endpoint to return whole guest list, not just the updated guests
    assert response.status_code == status.HTTP_200_OK
    assert response.context["guests"] == [guest_1, guest_2]


@pytest.mark.parametrize(
    "guest_attending_status,  search_text, attending_filter, expected_number_of_filtered_guests",
    [
        (True, "an", "all", 1),  # should pass, this is the same as before
        (True, "be", "all", 0),  # should pass, this is the same as before
        (True, "be", "attending", 0),  # should pass since search doesn't match
        (True, "be", "not_attending", 0),  # should pass since search doesn't match
        (True, "an", "attending", 1),  # should pass since search matches and status isn't checked
        (True, "an", "not_attending", 0),  # should fail since search matches but filter doesn't
        (True, "", "attending", 1),  # should pass since empty search matches the result
        (True, "", "not_attending", 0),  # should fail, since search matches, but filter doesn't
        (False, "an", "all", 1),  # should pass since filter is "all"
        (False, "be", "all", 0),  # should pass since filter is "all"
        (False, "be", "attending", 0),  # should pass since search doesn't match
        (False, "be", "not_attending", 0),  # should pass since search doesn't match
        (False, "an", "attending", 0),  # should fail since "an" matches, but "attending" shouldn't
        (False, "an", "not_attending", 1),  # should pass since filter matches even if not checked
        (False, "", "attending", 0), # should fail since filter doesn't match output
        (False, "", "not_attending", 1), # should pass since filter matches output even if not checked
    ],
)
def test_filter_guest_by_status_and_search(
        guest_attending_status,
        search_text,
        attending_filter,
        expected_number_of_filtered_guests,
        session: Session,
        client: TestClient,
        create_party: Callable[..., Party],
        create_guest: Callable[..., Guest],
):
    party = create_party(session=session)
    create_guest(session=session, party=party, name="Anna", attending=guest_attending_status)

    another_party = create_party(session=session, venue="Another venue")
    create_guest(session=session, party=another_party, name="Anna")

    url = app.url_path_for("filter_guests_partial", party_id=party.uuid)
    data = {"guest_search": search_text, "attending_filter": attending_filter}

    response = client.post(url, data=data)

    assert response.status_code == status.HTTP_200_OK
    assert len(response.context["guests"]) == expected_number_of_filtered_guests
