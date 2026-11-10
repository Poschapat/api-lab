import pytest

# Boundary values for updating stars: 1 and 5 succeed; 0 and 6 are refused without changing data.
@pytest.mark.parametrize("stars,expected_status", [
    (0, 400),
    (1, 200),
    (5, 200),
    (6, 400),
])
def test_update_rating_boundaries(api, auth, rating, stars, expected_status):
    path = f"/api/ratings/{rating['id']}"
    res = api.put(path, json={"stars": stars}, headers=auth)
    assert res.status_code == expected_status

    # Verify state in DB
    check_res = api.get(path, headers=auth)
    assert check_res.status_code == 200
    if expected_status == 200:
        assert check_res.json()["stars"] == stars
    else:
        assert check_res.json()["stars"] == rating["stars"]