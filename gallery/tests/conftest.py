import pytest
from gallery.app import create_app


@pytest.fixture(scope="session")
def app():
    app = create_app()
    with app.app_context():
        yield app
