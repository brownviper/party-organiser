from fastapi import status
from fastapi.testclient import TestClient
from sqlmodel import Session, select

from party_app.main import app
from party_app.models import Party


def test_new_party_form_includes_form(client: TestClient):
    url = app.url_path_for("new_party_form_page")

    response = client.get(url)

    assert response.status_code == status.HTTP_200_OK
    assert "new-party-form" in response.text


def test_create_party(session: Session, client: TestClient):
    url = app.url_path_for("new_party_create_page")

    data = {
        "party_date": "2025-06-06",
        "party_time": "18:00:00",
        "venue": "My Venue",
        "invitation": "Come to my party!",
    }

    response = client.post(url, data=data, follow_redirects=False)

    assert len(session.exec(select(Party)).all()) == 1
    assert response.status_code == status.HTTP_302_FOUND
