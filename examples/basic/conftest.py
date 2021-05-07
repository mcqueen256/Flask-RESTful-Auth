import os
import tempfile
import pytest
from . import server as example_server


@pytest.fixture
def app():
    app = example_server.create_app()
    with app.app_context():
        pass
    yield app
    return

@pytest.fixture
def server(app):
    return app.test_client()