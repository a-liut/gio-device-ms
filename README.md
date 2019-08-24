# gio-device-ms

Microservice that stores data of connected devices and their data.

## Build

Run

```bash
docker build -t gio-device-ms:latest .

docker run gio-device-ms:latest
```

## Entities

### Device

A Device represents a physical device registered in the system. Each device is identified by an ID.

#### Fields

- name: *string* - The name of the device.
- mac: *string* -  The MAC address of the device. Must be unique.
- room_id: *int* - The ID of the room to which the device belongs.

Example:

```json
{
    "mac": "f6:f1:bb:06:31:71",
    "name": "device1",
    "room_id": 1
}
```

### Room

A Room is a (possibly empty) collection of devices.

#### Fields

- name: *string* - The name of the room.

Example:

```json
{
    "name": "Room1"
}
```

## Endpoints

- ### /devices

    **GET**: return all registered devices.

    **POST**: register a new device.

- ### /devices/{id}

    **GET**: return the specified device.

- ### /devices/{id}/readings

    **GET**: return all readings of the specified devices.

- ### /rooms

    **GET**: return all registered rooms.

    **POST**: register a new room.

- ### /rooms/{id}

    **GET**: return the specified room.
