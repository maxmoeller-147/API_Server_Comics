import pytest

ENDPOINTS = [
    "/orders/",
    "/order_comics/",
]

@pytest.mark.parametrize("endpoint", ENDPOINTS)
def test_endpoint(http, endpoint):
    r = http.get(endpoint)
    assert r.status_code == 200, f"{endpoint} returned {r.status_code}: {r.text}"
