from flask import json
from gfndevice.models import Device, Room

def new_test_room(database, room_name):
    r = Room(name=room_name)
    database.session.add(r)
    database.session.flush()

    return r


def test_empty_devices(client, database):
    response = client.get('/devices/')

    assert response.status_code == 200
    assert response.get_json() == []


def test_single_device(client, database):
    test_room_name="TRoom"
    r1 = new_test_room(database, test_room_name)

    test_mac = "f6:f1:bb:06:31:71"
    test_name = "TestDevice"
    d1 = Device(id=1, mac=test_mac, name=test_name, room=r1)
    database.session.add(d1)
    database.session.commit()

    response = client.get('/devices/')

    assert response.status_code == 200

    # Check the device
    l = response.get_json()
    assert len(l) == 1

    assert test_mac == l[0]['mac']
    assert test_name == l[0]['name']


def test_get_device(client, database):
    test_room_name="TRoom1"
    r1 = new_test_room(database, test_room_name)

    test_mac = "f6:f1:bb:06:31:72"
    test_name = "TestDevice1"
    d1 = Device(id=2, mac=test_mac, name=test_name, room=r1)
    database.session.add(d1)
    database.session.commit()

    response = client.get('/devices/{}'.format(d1.id))

    assert response.status_code == 200

    # Check the device
    d = response.get_json()
    assert test_mac == d['mac']
    assert test_name == d['name']


def test_missing_id(client, database):
    response = client.get('/devices/{}'.format("asd"))

    assert response.status_code == 404


def test_device_not_found(client, database):
    # Not found
    response = client.get('/devices/{}'.format(42))

    assert response.status_code == 404


def test_create_device(client, database):
    mimetype = 'application/json'
    headers = {
        'Content-Type': mimetype,
        'Accept': mimetype
    }

    data = {
        'mac': "f6:f1:bb:06:31:73",
        'name': 'test_name'
    }

    # Create the device
    response = client.post('/devices/', data=json.dumps(data), headers=headers)

    assert response.status_code == 200

    d = response.get_json()

    assert data['mac'] == d['mac']
    assert data['name'] == d['name']

    # TODO: test also the room!


def test_create_device_missing_data(client, database):
    mimetype = 'application/json'
    headers = {
        'Content-Type': mimetype,
        'Accept': mimetype
    }

    data = {
    }

    # Create the device
    response = client.post('/devices/', data=json.dumps(data), headers=headers)

    assert response.status_code == 400

    data = {
        'mac': "f6:f1:bb:06:31:73"
    }

    # Create the device
    response = client.post('/devices/', data=json.dumps(data), headers=headers)

    assert response.status_code == 400


def test_create_device_invalid_data(client, database):
    mimetype = 'application/json'
    headers = {
        'Content-Type': mimetype,
        'Accept': mimetype
    }

    data = {
        'mac': "asd"
    }

    # Create the device
    response = client.post('/devices/', data=json.dumps(data), headers=headers)

    assert response.status_code == 400


def test_duplicated_device(client, database):
    mimetype = 'application/json'
    headers = {
        'Content-Type': mimetype,
        'Accept': mimetype
    }

    data = {
        'mac': "f6:f1:bb:06:31:74",
        'name': 'new_name'
    }

    # Create the first device
    response = client.post('/devices/', data=json.dumps(data), headers=headers)

    assert response.status_code == 200

    # Try to create a new device with the same MAC address
    response = client.post('/devices/', data=json.dumps(data), headers=headers)

    assert response.status_code == 400
    assert b"MAC already in use" in response.data


def test_duplicated_name_device(client, database):
    mimetype = 'application/json'
    headers = {
        'Content-Type': mimetype,
        'Accept': mimetype
    }

    data = {
        'mac': "f6:f1:bb:06:31:77",
        'name': 'same_name'
    }

    # Create the first device
    response = client.post('/devices/', data=json.dumps(data), headers=headers)

    assert response.status_code == 200

    data = {
        'mac': "f6:f1:bb:06:31:78",
        'name': 'same_name'
    }

    # Try to create a new device with the same name
    response = client.post('/devices/', data=json.dumps(data), headers=headers)

    assert response.status_code == 400
    assert b"Name already in use" in response.data