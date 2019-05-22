from flask import json
from gfndevice.models import Device, Room

def new_test_device(database, id, mac, name, room):
    d1 = Device(id=id, mac=mac, name=name, room=room)
    database.session.add(d1)
    database.session.flush()

    return d1

def new_test_room(database, room_name):
    r = Room(name=room_name)
    database.session.add(r)
    database.session.flush()

    return r

def test_empty_readings(client, database):
    r = new_test_room(database, "test_room")
    new_test_device(database, 1, "f6:f1:bb:06:31:79", "test_dev", r)
    database.session.commit()

    response = client.get('/devices/1/readings')

    assert response.status_code == 200
    assert response.get_json() == []


def test_readings_device_not_found(client, database):
    response = client.get('/devices/2/readings')

    assert response.status_code == 404


def test_create_reading(client, database):
    r = new_test_room(database, "test_room")
    new_test_device(database, 1, "f6:f1:bb:06:31:79", "test_dev", r)
    database.session.commit()

    mimetype = 'application/json'
    headers = {
        'Content-Type': mimetype,
        'Accept': mimetype
    }

    data = {
        "name": "temperature",
        "value": 12,
        "unit": "C°"
    }

    # Create the reading
    response = client.post('/devices/1/readings', data=json.dumps(data), headers=headers)

    assert response.status_code == 200

    reading = response.get_json()

    assert data['name'] == reading['name']
    assert data['value'] == reading['value']
    assert data['unit'] == reading['unit']


def test_create_reading_error(client, database):
    r = new_test_room(database, "test_room")
    new_test_device(database, 1, "f6:f1:bb:06:31:79", "test_dev", r)
    database.session.commit()

    mimetype = 'application/json'
    headers = {
        'Content-Type': mimetype,
        'Accept': mimetype
    }

    data = {
        "name": "asd",
        "value": "asd",
        "unit": ""
    }

    response = client.post('/devices/1/readings', data=json.dumps(data), headers=headers)

    assert response.status_code == 400


def test_create_reading_missing_data(client, database):
    r = new_test_room(database, "test_room")
    new_test_device(database, 1, "f6:f1:bb:06:31:79", "test_dev", r)
    database.session.commit()

    mimetype = 'application/json'
    headers = {
        'Content-Type': mimetype,
        'Accept': mimetype
    }

    datas = [
        {
        },
        {
            "name": "test"
        },
        {
            "value": 123
        },
        {
            "unit": ""
        },
        {
            "value": 123,
            "unit": "C°"
        }
    ]

    for d in datas:
        response = client.post('/devices/1/readings', data=json.dumps(d), headers=headers)
        assert response.status_code == 400


def test_create_reading_invalid_data(client, database):
    r = new_test_room(database, "test_room")
    new_test_device(database, 1, "f6:f1:bb:06:31:79", "test_dev", r)
    database.session.commit()

    mimetype = 'application/json'
    headers = {
        'Content-Type': mimetype,
        'Accept': mimetype
    }

    data = {
            "name": -1,
            "value": 1
        }
    response = client.post('/devices/1/readings', data=json.dumps(data), headers=headers)
    assert response.status_code == 400

    data = {
            "name": "test",
            "value": "asd"
        }
    response = client.post('/devices/1/readings', data=json.dumps(data), headers=headers)
    assert response.status_code == 400

    data = {
            "name": "test2",
            "value": 1,
            "unit": 1
        }
    response = client.post('/devices/1/readings', data=json.dumps(data), headers=headers)
    assert response.status_code == 400