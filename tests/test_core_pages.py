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
