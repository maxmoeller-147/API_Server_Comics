def test_health(http):
    r = http.get("/health")
    assert r.status_code == 200, r.text
