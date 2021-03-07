import requests

def test_status_code_equals_200():
    response = requests.get("http://capstone100.herokuapp.com")
    assert response.status_code == 200
    print(response)

def test_content_type_equals_json():
     response = requests.get("http://capstone100.herokuapp.com")
     assert response.headers["Content-Type"] == "application/json"
     print(response.headers)


def test_country_equals_united_states():
     response = requests.get("http://capstone100.herokuapp.com")
     response_body = response.json()
     assert response_body["success"] == True
     print(response_body)

if __name__ == "__main__":
    test_status_code_equals_200()
    test_content_type_equals_json()
    test_country_equals_united_states()
