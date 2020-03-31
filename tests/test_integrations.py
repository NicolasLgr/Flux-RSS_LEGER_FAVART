import os
import pytest
from app import app
from flask import url_for


@pytest.fixture
def client():
    app.config['TESTING'] = True
    app.config['SERVER_NAME'] = 'TEST.test'
    client = app.test_client()
    with app.app_context():
        pass
    app.app_context().push()
    yield client


def test_index_page(client):
    rv = client.get('/')
    assert rv.status_code == 200
    assert b'Log In' in rv.data
    assert b'Sign In' in rv.data

def test_login_page(client):
    rv = client.get('/')
    assert rv.status_code == 200
    assert b'Log In' in rv.data

def test_signin_page(client):
    rv = client.get('/')
    assert rv.status_code == 200
    assert b'Sign In' in rv.data

def test_not_logged(client):
    rv = client.get('/feed')
    assert rv.status_code == 401