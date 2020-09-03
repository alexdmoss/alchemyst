from alchemyst import app
from alchemyst.ui.redirects import _get_note_name_from_id
from fakes.fake_note import FakePhysicalNote

urls = {
    '/contact.php': '/contact',
    '/index.php?target=index': '/home',
    '/index.php?target=about&pagetitle=About%20the%20Alchemystry%20Site': '/about',
    '/index.php?target=links&pagetitle=Alchemystry%20Links': '/links',
    '/pdfindex.php': '/notes',
    '/pdfindex.php?group=level&value=1&pagetitle=Alchemystry%20-%201st%20Year%20Notes%20(PDF)': '/notes/first-year',
    '/pdfindex.php?group=level&value=2&pagetitle=Alchemystry%20-%202nd%20Year%20Notes%20(PDF)': '/notes/second-year',
    '/pdfindex.php?group=level&value=3&pagetitle=Alchemystry%20-%203rd%20Year%20Notes%20(PDF)': '/notes/third-year',
    '/pdfindex.php?group=level&value=nope&pagetitle=NOPE': '/notes',
    '/pdfindex.php?group=all&value=&offset=0&index=0&orderby=title&direction=ASC': '/notes',
    '/pdfindex.php?group=all&value=&offset=50&index=50&orderby=title&direction=ASC': '/notes',
    '/pdfindex.php?group=all&value=&orderby=category&direction=asc': '/notes',
    '/pdfindex.php?group=all&value=&orderby=category&direction=desc': '/notes',
    '/pdfindex.php?group=category&value=Organic&pagetitle=Alchemystry%20-%20Organic%20Notes%20(PDF)': '/notes/organic',
    '/pdfindex.php?group=category&value=Inorganic&pagetitle=Alchemystry%20-%20Inorganic%20Notes%20(PDF)': '/notes/inorganic',
    '/pdfindex.php?group=category&value=Physical&pagetitle=Alchemystry%20-%20Physical%20Notes%20(PDF)': '/notes/physical',
    '/pdfindex.php?group=all&pagetitle=Alchemystry%20-%20All%20the%20Notes%20(PDF)': '/notes',
    '/pdfindex.php?group=bad&pagetitle=whatever': '/notes',
    '/search.php?search_string=alicyclic&search_submit=Go&boolean_type=AND': '/search',
    '/pdfindex.php?id=75': '/note/advanced-solid-state',
    '/pdfindex.php?id=84': '/note/chromium-iron-and-cobalt-in-synthesis',
}


def test_redirect_urls(mocker):
    mock_note_lookup = mocker.patch('alchemyst.ui.redirects._get_note_name_from_id')
    notes = {
        "/pdfindex.php?id=75": "advanced-solid-state",
        '/pdfindex.php?id=84': 'chromium-iron-and-cobalt-in-synthesis',
    }

    for origin, target in urls.items():
        mock_note_lookup(origin)
        if 'id=' in origin:
            mock_note_lookup.return_value = notes[origin]
        with app.test_request_context(origin, method='GET'):
            request = app.dispatch_request()
            response = app.make_response(request)
            assert response.status_code == 301
            assert response.headers['Location'] == target


def test_note_lookup(mocker):
    mocker.patch('alchemyst.ui.redirects.note')
    mocker.patch('alchemyst.ui.redirects.note_from_dict')
    note_view = mocker.patch('alchemyst.ui.redirects.note_view')
    note_view.return_value = FakePhysicalNote()
    assert _get_note_name_from_id(99) == 'applications-of-statistical-mechanics'
