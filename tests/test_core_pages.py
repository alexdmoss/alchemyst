from alchemyst import app


def test_header_footer_nav():
    with app.test_request_context('/', method='GET'):
        request = app.dispatch_request()
        response = app.make_response(request)
        assert response.status_code == 200
        assert "<title>Alchemyst :: " in response.get_data(as_text=True)
        assert "&copy;" in response.get_data(as_text=True)
        assert '<a href="/contact">' in response.get_data(as_text=True)


def test_home_page():
    with app.test_request_context('/', method='GET'):
        request = app.dispatch_request()
        response = app.make_response(request)
        assert response.status_code == 200
        assert "Hello and welcome" in response.get_data(as_text=True)


def test_contact_page():
    with app.test_request_context('/contact', method='GET'):
        request = app.dispatch_request()
        response = app.make_response(request)
        assert response.status_code == 200
        assert "Please use this form to get in touch" in response.get_data(as_text=True)


def test_links_page():
    with app.test_request_context('/links', method='GET'):
        request = app.dispatch_request()
        response = app.make_response(request)
        assert response.status_code == 200
        assert "dead links now" in response.get_data(as_text=True)


def test_about_page():
    with app.test_request_context('/about', method='GET'):
        request = app.dispatch_request()
        response = app.make_response(request)
        assert response.status_code == 200
        assert "About This Site" in response.get_data(as_text=True)


def test_privacy_page():
    with app.test_request_context('/privacy', method='GET'):
        request = app.dispatch_request()
        response = app.make_response(request)
        assert response.status_code == 200
        assert "All content provided on this" in response.get_data(as_text=True)


def test_tags_page():
    with app.test_request_context('/tags', method='GET'):
        request = app.dispatch_request()
        response = app.make_response(request)
        assert response.status_code == 200
        assert "Notes By Tag" in response.get_data(as_text=True)


def test_search_page():
    with app.test_request_context('/search', method='GET'):
        request = app.dispatch_request()
        response = app.make_response(request)
        assert response.status_code == 200
        assert "Search the Notes" in response.get_data(as_text=True)
