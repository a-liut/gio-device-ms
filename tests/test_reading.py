from flask import json
from gfndevice.models import Device

def test_empty_readings(client, database):
    test_mac = "f6:f1:bb:06:31:79"
    d1 = Device(id=1, mac=test_mac)
    database.session.add(d1)
    database.session.commit()

    response = client.get('/devices/1/readings')

    assert response.status_code == 200
    assert response.get_json() == []


def test_readings_device_not_found(client, database):
    response = client.get('/devices/2/readings')

    assert response.status_code == 404


def test_create_reading(client, database):
    mimetype = 'application/json'
    headers = {
        'Content-Type': mimetype,
        'Accept': mimetype
    }

    data = {
        "temperature": 12,
        "moisture": 123,
        "light": 111
    }

    # Create the reading
    response = client.post('/devices/1/readings', data=json.dumps(data), headers=headers)

    assert response.status_code == 200

    d = response.get_json()

    assert data['temperature'] == d['temperature']
    assert data['moisture'] == d['moisture']
    assert data['light'] == d['light']


def test_create_reading_error(client, database):
    mimetype = 'application/json'
    headers = {
        'Content-Type': mimetype,
        'Accept': mimetype
    }

    data = {
        "temperature": "asd",
        "moisture": "asd",
        "light": "asd"
    }

    response = client.post('/devices/1/readings', data=json.dumps(data), headers=headers)

    assert response.status_code == 400


def test_create_reading_missing_data(client, database):
    mimetype = 'application/json'
    headers = {
        'Content-Type': mimetype,
        'Accept': mimetype
    }

    datas = [
        {
            "temperature": 123
        },
        {
            "moisture": 123
        },
        {
            "light": 123
        },
        {
            "temperature": 123,
            "moisture": 123
        },
        {
            "temperature": 123,
            "light": 123
        },
        {
            "moisture": 123,
            "light": 123
        }
    ]

    for d in datas:
        response = client.post('/devices/1/readings', data=json.dumps(d), headers=headers)
        assert response.status_code == 400


def test_create_reading_invalid_data(client, database):
    mimetype = 'application/json'
    headers = {
        'Content-Type': mimetype,
        'Accept': mimetype
    }

    datas = [
        {
            "temperature": -1
        },
        {
            "moisture": -1
        },
        {
            "light": -1
        },
        {
            "temperature": -1,
            "moisture": -1
        },
        {
            "temperature": -1,
            "light": -1
        },
        {
            "moisture": -1,
            "light": -1
        }
    ]

    for d in datas:
        response = client.post('/devices/1/readings', data=json.dumps(d), headers=headers)
        assert response.status_code == 400
