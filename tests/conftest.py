import os
import pytest

from gfndevice import create_app
from gfndevice.db import db as _db
from gfndevice.settings import TestConfig


@pytest.fixture(scope='module')
def app():
    """Session-wide test `Flask` application."""

    # create the app with common test config
    config = TestConfig()
    app = create_app(config)

    return app


@pytest.fixture(scope='module')
def client(app):
    """A test client for the app."""

    tc = app.test_client()

    # Establish an application context before running the tests.
    ctx = app.app_context()
    ctx.push()
 
    yield tc  # this is where the testing happens!
 
    ctx.pop()


@pytest.fixture(scope='module')
def database(app):
    """Session-wide test database."""

    with app.app_context():
        _db.init_app(app)

        print("Init db...")

        _db.create_all()

        yield _db

        _db.drop_all()