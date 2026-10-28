import pytest
from fakes.fake_note import FakeInorganicNote, FakeOrganicNote, FakePhysicalNote

from alchemyst import app, cache


@pytest.fixture
def client(mocker):
    mocker.patch(
        "alchemyst.api.routes.get_notes",
        return_value=[FakeInorganicNote(), FakeOrganicNote(), FakePhysicalNote()],
    )
    with app.app_context():
        cache.clear()
    return app.test_client()


def test_healthz(client):
    response = client.get("/healthz")
    assert response.status_code == 200
    assert response.get_data(as_text=True) == "OK"


def test_notes(client):
    response = client.get("/api/notes")
    assert response.status_code == 200
    assert len(response.get_json()["notes"]) == 3


# The UI calls note() directly, so only a request through the URL catches the
# route's placeholder and the function's argument drifting apart
def test_note_by_name(client):
    response = client.get("/api/note/advanced-solid-state")
    assert response.status_code == 200
    assert response.get_json()["title"] == "Advanced Solid State"


def test_note_by_id(client):
    response = client.get("/api/note/99")
    assert response.status_code == 200
    assert response.get_json()["name"] == "applications-of-statistical-mechanics"


def test_unknown_note(client):
    response = client.get("/api/note/no-such-note")
    assert response.status_code == 404
