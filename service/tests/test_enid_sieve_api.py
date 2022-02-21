from datetime import datetime

from fastapi.testclient import TestClient

from ..main import app


client = TestClient(app)

ENID_SIEVE_API_PATH = '/enids/sieve'

def test_invalid_enid_birthdate():
    malformed_enid = '39608013501312'
    response = client.post(ENID_SIEVE_API_PATH, json={'enid': malformed_enid})
    assert response.status_code == 422
    assert response.json().get('detail', list())[0].get('msg') == 'Malformed birth date.'

def test_invalid_enid_century():
    malformed_enid = '49608013501312'
    response = client.post(ENID_SIEVE_API_PATH, json={'enid': malformed_enid})
    assert response.status_code == 422
    assert response.json().get('detail', list())[0].get('msg') == 'Malformed century.'

def test_invalid_enid_length():
    malformed_enid = '4960801350131'
    response = client.post(ENID_SIEVE_API_PATH, json={'enid': malformed_enid})
    assert response.status_code == 422
    assert response.json().get('detail', list())[0].get('msg') == 'string does not match regex "[0-9]{14}"'

def test_invalid_enid_format():
    malformed_enid = 'abcdef08013501'
    response = client.post(ENID_SIEVE_API_PATH, json={'enid': malformed_enid})
    assert response.status_code == 422
    assert response.json().get('detail', list())[0].get('msg') == 'string does not match regex "[0-9]{14}"'

def test_invalid_enid_governorate():
    malformed_enid = '29608019001312'
    response = client.post(ENID_SIEVE_API_PATH, json={'enid': malformed_enid})
    assert response.status_code == 422
    assert response.json().get('detail', list())[0].get('msg') == 'Malformed Governorate.'

def test_valid_enid():
    valid_enid = '29608013501312'
    response = client.post(ENID_SIEVE_API_PATH, json={'enid': valid_enid})
    assert response.status_code == 200
    response_data = response.json()
    assert response_data.get('century_code') == 2
    assert response_data.get('century_span') == '1900-1999'
    assert response_data.get('birthdate') == '1996-08-01'
    assert response_data.get('governorate') == 'South Sinai'
    assert response_data.get('governorate_code') == 35
    assert response_data.get('gender') == 'male'
    assert response_data.get('check_code') == 2
    assert isinstance(response_data.get('birthdate_unixtimestamp'), int)
    birthdatetime = datetime.fromtimestamp(response_data['birthdate_unixtimestamp'])
    assert birthdatetime.date().day == 1
    assert birthdatetime.date().month == 8
    assert birthdatetime.date().year == 1996 
    