import json
import requests


def test_without_question():
    response = requests.post('http://127.0.0.1:5000/ask', json={})
    assert response.status_code == 400
    json_data = json.loads(response.text)
    assert json_data['error'] == 'Question not provided'


def test_with_question():
    response = requests.post('http://127.0.0.1:5000/ask', json={"question": "What's the capital of Israel?"})
    assert response.status_code == 200
