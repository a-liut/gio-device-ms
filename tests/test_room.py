from flask import json
from gfndevice.models import Room

def new_test_room(database, room_name):
    r = Room(name=room_name)
    database.session.add(r)
    database.session.flush()

    return r

def test_empty_rooms(client, database):
    response = client.get('/rooms/')

    assert response.status_code == 200
    assert response.get_json() == []


def test_single_room(client, database):
    test_name = "room1"
    new_test_room(database, test_name)
    database.session.commit()

    response = client.get('/rooms/')

    assert response.status_code == 200

    # Check the device
    l = response.get_json()
    assert len(l) == 1

    name1 = l[0]['name']

    assert name1 == test_name


def test_get_device(client, database):
    test_name = "room1"
    r1 = Room(name=test_name)
    database.session.add(r1)
    database.session.commit()

    response = client.get('/rooms/{}'.format(r1.id))

    assert response.status_code == 200

    # Check the device
    r = response.get_json()
    assert test_name == r['name']


def test_missing_id(client, database):
    response = client.get('/rooms/{}'.format("asd"))

    assert response.status_code == 404


def test_room_not_found(client, database):
    # Not found
    response = client.get('/rooms/{}'.format(42))

    assert response.status_code == 404


def test_create_room(client, database):
    mimetype = 'application/json'
    headers = {
        'Content-Type': mimetype,
        'Accept': mimetype
    }

    data = {
        'name': 'testroom'
    }

    # Create the room
    response = client.post('/rooms/', data=json.dumps(data), headers=headers)

    assert response.status_code == 200

    r = response.get_json()

    assert r['name'] == data['name']
    assert r['devices'] == []


# def test_create_device_missing_data(client, database):
#     mimetype = 'application/json'
#     headers = {
#         'Content-Type': mimetype,
#         'Accept': mimetype
#     }

#     data = {
#     }

#     # Create the device
#     response = client.post('/devices/', data=json.dumps(data), headers=headers)

#     assert response.status_code == 400


# def test_create_device_invalid_data(client, database):
#     mimetype = 'application/json'
#     headers = {
#         'Content-Type': mimetype,
#         'Accept': mimetype
#     }

#     data = {
#         'mac': "asd"
#     }

#     # Create the device
#     response = client.post('/devices/', data=json.dumps(data), headers=headers)

#     assert response.status_code == 400


# def test_duplicated_device(client, database):
#     mimetype = 'application/json'
#     headers = {
#         'Content-Type': mimetype,
#         'Accept': mimetype
#     }

#     data = {
#         'mac': "f6:f1:bb:06:31:74"
#     }

#     # Create the first device
#     response = client.post('/devices/', data=json.dumps(data), headers=headers)

#     assert response.status_code == 200

#     # Try to create a new device with the same MAC address
#     response = client.post('/devices/', data=json.dumps(data), headers=headers)

#     assert response.status_code == 400
#     assert b"MAC already in use" in response.data
