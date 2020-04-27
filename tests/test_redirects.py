import requests

urls = {
    'http://localhost:5000/contact.php': 'http://localhost:5000/contact',
    'http://localhost:5000/index.php?target=index': 'http://localhost:5000/home',
    'http://localhost:5000/index.php?target=about&pagetitle=About%20the%20Alchemystry%20Site': 'http://localhost:5000/about',
    'http://localhost:5000/index.php?target=links&pagetitle=Alchemystry%20Links': 'http://localhost:5000/links',
    'http://localhost:5000/pdfindex.php': 'http://localhost:5000/notes',
    'http://localhost:5000/pdfindex.php?group=level&value=1&pagetitle=Alchemystry%20-%201st%20Year%20Notes%20(PDF)': 'http://localhost:5000/notes/first-year',
    'http://localhost:5000/pdfindex.php?group=all&value=&offset=0&index=0&orderby=title&direction=ASC': 'http://localhost:5000/notes',
    'http://localhost:5000/pdfindex.php?group=all&value=&offset=50&index=50&orderby=title&direction=ASC': 'http://localhost:5000/notes',
    'http://localhost:5000/pdfindex.php?group=all&value=&orderby=category&direction=asc': 'http://localhost:5000/notes',
    'http://localhost:5000/pdfindex.php?group=all&value=&orderby=category&direction=desc': 'http://localhost:5000/notes',
    'http://localhost:5000/pdfindex.php?group=category&value=Organic&pagetitle=Alchemystry%20-%20Organic%20Notes%20(PDF)': 'http://localhost:5000/notes/organic',
    'http://localhost:5000/pdfindex.php?group=category&value=Inorganic&pagetitle=Alchemystry%20-%20Inorganic%20Notes%20(PDF)': 'http://localhost:5000/notes/inorganic',
    'http://localhost:5000/pdfindex.php?group=category&value=Physical&pagetitle=Alchemystry%20-%20Physical%20Notes%20(PDF)': 'http://localhost:5000/notes/physical',
    'http://localhost:5000/pdfindex.php?group=all&pagetitle=Alchemystry%20-%20All%20the%20Notes%20(PDF)': 'http://localhost:5000/notes',
    'http://localhost:5000/search.php?search_string=alicyclic&search_submit=Go&boolean_type=AND': 'http://localhost:5000/search',
    'http://localhost:5000/pdfindex.php?id=75': 'http://localhost:5000/note/advanced-solid-state',
    'http://localhost:5000/pdfindex.php?id=99': 'http://localhost:5000/note/applications-of-statistical-mechanics',
    'http://localhost:5000/pdfindex.php?id=84': 'http://localhost:5000/note/chromium-iron-and-cobalt-in-synthesis',
    'http://localhost:5000/pdfindex.php?id=93': 'http://localhost:5000/note/protecting-groups-and-carbohydrates',
    'http://localhost:5000/pdfindex.php?id=81': 'http://localhost:5000/note/x-ray-diffraction',
    'http://localhost:5000/pdfindex.php?id=61': 'http://localhost:5000/note/descriptive-p-block-chemistry',
    'http://localhost:5000/pdfindex.php?id=88': 'http://localhost:5000/note/organoelements',
    'http://localhost:5000/pdfindex.php?id=76': 'http://localhost:5000/note/solid-state-electronics'
}

# TODO: still need to cover downloads!


def test_redirect_urls():
    for origin, target in urls.items():
        response = requests.head(origin)
        assert response.status_code == 302
        assert response.headers['Location'] == target
