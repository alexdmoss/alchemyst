from alchemyst import app
from fakes.fake_note import FakeOrganicNote, FakeInorganicNote, FakePhysicalNote


def test_notes_page(mocker):
    mocker.patch('alchemyst.ui.routes.notes')
    notes_list = mocker.patch('alchemyst.ui.routes.notes_from_dicts')
    notes_list.return_value = [FakeInorganicNote(), FakeOrganicNote(), FakePhysicalNote()]
    with app.test_request_context('/notes', method='GET'):
        request = app.dispatch_request()
        response = app.make_response(request)
        assert response.status_code == 200
        assert "Filter By" in response.get_data(as_text=True)
        assert "Advanced Solid State" in response.get_data(as_text=True)
        assert "Applications of Statistical Mechanics" in response.get_data(as_text=True)
        assert "Alicyclic Chemistry" in response.get_data(as_text=True)


def test_notes_by_category(mocker):
    mocker.patch('alchemyst.ui.routes.notes_by_category')
    notes_list = mocker.patch('alchemyst.ui.routes.notes_from_dicts')
    notes_list.return_value = [FakePhysicalNote()]
    with app.test_request_context('/notes/physical', method='GET'):
        request = app.dispatch_request()
        response = app.make_response(request)
        assert response.status_code == 200
        assert "Filter By" in response.get_data(as_text=True)
        assert "Applications of Statistical Mechanics" in response.get_data(as_text=True)
        assert "Physical - 3rd Year Undergraduate" in response.get_data(as_text=True)
        assert "Starts with basic revision" in response.get_data(as_text=True)


def test_note_page(mocker):
    mocker.patch('alchemyst.ui.routes.get_document')
    mocker.patch('alchemyst.ui.routes.note')
    mocker.patch('alchemyst.ui.routes.note_from_dict')
    note = mocker.patch('alchemyst.ui.routes.note_view')
    note.return_value = FakePhysicalNote()
    with app.test_request_context('/note/advanced-solid-state', method='GET'):
        request = app.dispatch_request()
        response = app.make_response(request)
        assert response.status_code == 200
        assert "Applications of Statistical Mechanics" in response.get_data(as_text=True)
        assert "Author" in response.get_data(as_text=True)
        assert "Alex Moss" in response.get_data(as_text=True)
        assert "basic revision" in response.get_data(as_text=True)
        assert "3rd Year Undergraduate" in response.get_data(as_text=True)


def test_pdf_page(mocker, socket_enabled):
    with app.test_request_context('/pdf/Inorganic/solid_state_advanced.pdf', method='GET'):
        request = app.dispatch_request()
        response = app.make_response(request)
        assert response.status_code == 200
        assert response.headers['Content-Type'] == 'application/pdf'
        assert int(response.headers['Content-Length']) > 65000
