"""
This file includes tests for the API
"""

from starlette.testclient import TestClient
from app.db import count_enteries_tables

def test_health(client: TestClient):
    response = client.get("/health")

    assert response.status_code == 200

# Test that both tables were created sucessfully after the API startup 
def test_table_creation(client: TestClient):
    assert count_enteries_tables() == (0,0)

# Test that both tables were inserted to after a post call 
def test_table_insertion_after_post(client: TestClient):
    response = client.post(
        "/api/shorten_url",
        json={"long_url": "https://www.youtube.com/watch?v=UzxYlbK2c7E&ab_channel=Stanford"},
    )
    assert count_enteries_tables() == (1,1)

# Normal input
def test_successful_post_call(client: TestClient):
    response = client.post(
        "/api/shorten_url",
        json={"long_url": "https://www.youtube.com/watch?v=UzxYlbK2c7E&ab_channel=Stanford"},
    )

    assert response.status_code == 200


def test_fail_post_call_malformed_url(client: TestClient):
    response = client.post(
        "/api/shorten_url",
        json={"long_url": "httasdaps://google.com"},
    )

    assert response.status_code == 422


def test_fail_post_call(client: TestClient):
    response = client.post(
        "/api/shorten_url",
        json={"long_url": 0},
    )
    """ Unprocessable entry because long_url has to be str, but got a
     int type """
    assert response.status_code == 422


def test_visits_fail(client: TestClient):
    response_shorten = client.post(
        "/api/shorten_url",
        json={"long_url": "https://google.com"},
        )
    short_url = response_shorten.json()['short_url'][-6:]
    visit_response = client.get("/visits/{}".format(short_url + 'S'))
    assert visit_response.status_code == 404


def test_increment_visits(client: TestClient):
    response_shorten = client.post(
        "/api/shorten_url",
        json={"long_url": "https://google.com"},
        )
    short_url = response_shorten.json()['short_url'][-6:]
    visit_response = client.get("/visits/{}".format(short_url))
    # Not visited yet
    assert visit_response.json()['visits_count'] == 0
    # First visit
    client.get("/{}".format(short_url))
    visit_response = client.get("/visits/{}".format(short_url))
    assert visit_response.json()['visits_count'] == 1
    # One more visit
    client.get("/{}".format(short_url))
    visit_response = client.get("/visits/{}".format(short_url))
    assert visit_response.json()['visits_count'] == 2


def redirection_visit_fail(client: TestClient):
    response_shorten = client.post(
        "/api/shorten_url",
        json={"long_url": "https://google.com"},
        )
    short_url = response_shorten.json()['short_url'][-6:]
    visit_response = client.get("/{}".format(short_url + 'S'))
    assert visit_response.status_code == 404
