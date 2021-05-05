import os
import tempfile
import pytest
from examples.basic import server


@pytest.fixture
def app():
    app = server.create_app()
    with app.app_context():
        pass
    yield app
    return

@pytest.fixture
def client(app):
    return app.test_client()