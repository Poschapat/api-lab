# api-lab

API testing of QuickPizza (https://quickpizza.grafana.com) with pytest and requests.

## How to install

```
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```
(Windows PowerShell: `python -m venv .venv`, `.venv\Scripts\activate`,
`pip install -r requirements.txt`)

## How to run the tests

Run all tests:
```
pytest -v
```
Run one test:
```
pytest -v test_ratings.py::test_delete_rating
```
Save the report of a full run:
```
pytest -v --html=report.html --self-contained-html
```


![alt text](image/image3.png)

## Step A2: Base choice coverage

| Block | Input | Test |
| :--- | :--- | :--- |
| C2 decimal | "stars": 3.5 | test_stars_type_decimal |
| C2 text | "stars": "3" | test_stars_type_string |
| C2 missing field | No field stars | test_stars_missing | 
| C3 Pizza does not exist | "pizza_id": 999999999 | test_pizza_not_exist |
| C4 Token missing | No header | test_token_missing | 
| C4 Token wrong length / invalid | token short | test_token_wrong_length |