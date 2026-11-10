import pytest

# The pizza never needs a tool that the customer excluded.
@pytest.mark.parametrize("excluded", [
    ["Knife"], ["Scissors"],                 # block 1 tools
    [],                                      # block 0 tools
    ["Knife", "Scissors"]                    # block 2 tools
    # ["Knife", "Pizza cutter", "Scissors"],   # block 3 tools
    ])

def test_excluded_tool_is_not_used(api, auth, excluded):
    body = {"excludedTools": excluded}
    res = api.post("/api/pizza", json=body, headers=auth)
    assert res.status_code == 200
    assert res.json()["pizza"]["tool"] not in excluded

# A request that no pizza can satisfy gets 400 and a JSON error, never 500.
@pytest.mark.xfail(
    reason="Defect 1: excluding all three tools returns 500 with an empty body "
           "instead of 400 with a JSON error message",
    strict=True)

def test_all_tools_excluded_is_refused(api, auth):
    body = {"excludedTools": ["Knife", "Pizza cutter", "Scissors"]}
    res = api.post("/api/pizza", json=body, headers=auth)
    assert res.status_code == 400
    assert "error" in res.json()