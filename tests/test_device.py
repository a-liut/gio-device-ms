from flask import json
from gfndevice.models import Device

def test_empty_devices(client, database):
    response = client.get('/devices/')

    assert response.status_code == 200
    assert response.get_json() == []


def test_single_device(client, database):
    test_mac = "f6:f1:bb:06:31:71"
    d1 = Device(id=1, mac=test_mac)
    database.session.add(d1)
    database.session.commit()

    response = client.get('/devices/')

    assert response.status_code == 200

    # Check the device
    l = response.get_json()
    assert len(l) == 1

    mac1 = l[0]['mac']

    assert mac1 == test_mac


def test_get_device(client, database):
    test_mac = "f6:f1:bb:06:31:72"
    d1 = Device(id=2, mac=test_mac)
    database.session.add(d1)
    database.session.commit()

    response = client.get('/devices/{}'.format(d1.id))

    assert response.status_code == 200

    # Check the device
    d = response.get_json()
    assert test_mac == d['mac']


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
        'mac': "f6:f1:bb:06:31:73"
    }

    # Create the device
    response = client.post('/devices/', data=json.dumps(data), headers=headers)

    assert response.status_code == 200

    d = response.get_json()

    assert data['mac'] == d['mac']


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
        'mac': "f6:f1:bb:06:31:74"
    }

    # Create the first device
    response = client.post('/devices/', data=json.dumps(data), headers=headers)

    assert response.status_code == 200

    # Try to create a new device with the same MAC address
    response = client.post('/devices/', data=json.dumps(data), headers=headers)

    assert response.status_code == 400
    assert b"MAC already in use" in response.data
