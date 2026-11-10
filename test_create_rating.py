import pytest

STARS_ERROR = "number of stars must be between 1 and 5 (inclusive)"

# Base choice: 3 stars as a whole number, a real pizza, the user's token.
def test_base_choice_is_saved(api, auth, pizza_id):
    new = {"pizza_id": pizza_id, "stars": 3}
    res = api.post("/api/ratings", json=new, headers=auth)
    assert res.status_code == 201
    assert res.json()["stars"] == 3
    assert res.json()["pizza_id"] == pizza_id

# C1: a number of stars below 1 or above 5 is refused with a message.
@pytest.mark.parametrize("stars", [0, 6])
def test_stars_out_of_range(api, auth, pizza_id, stars):
    new = {"pizza_id": pizza_id, "stars": stars}
    res = api.post("/api/ratings", json=new, headers=auth)
    assert res.status_code == 400
    assert res.json() == {"error": STARS_ERROR}

# C2: Type of stars - decimal
def test_stars_type_decimal(api, auth, pizza_id):
    res = api.post("/api/ratings", json={"pizza_id": pizza_id, "stars": 3.5}, headers=auth)
    assert res.status_code == 400
    assert "error" in res.json()

# C2: Type of stars - string text
def test_stars_type_string(api, auth, pizza_id):
    res = api.post("/api/ratings", json={"pizza_id": pizza_id, "stars": "3"}, headers=auth)
    assert res.status_code == 400
    assert "error" in res.json()

# C2: Type of stars - missing field
def test_stars_missing(api, auth, pizza_id):
    res = api.post("/api/ratings", json={"pizza_id": pizza_id}, headers=auth)
    assert res.status_code == 400
    assert "error" in res.json()

# C3: Pizza does not exist
def test_pizza_not_exist(api, auth):
    res = api.post("/api/ratings", json={"pizza_id": 999999999, "stars": 3}, headers=auth)
    assert res.status_code in [400, 404]
    assert "error" in res.json()

# C4: Token missing
def test_token_missing(api, pizza_id):
    res = api.post("/api/ratings", json={"pizza_id": pizza_id, "stars": 3})
    assert res.status_code == 401
    assert res.json() == {"error": "authentication failed"}

# C4: Token wrong length / invalid
def test_token_wrong_length(api, pizza_id):
    bad_auth = {"Authorization": "token short"}
    res = api.post("/api/ratings", json={"pizza_id": pizza_id, "stars": 3}, headers=bad_auth)
    assert res.status_code == 401
    assert "error" in res.json()