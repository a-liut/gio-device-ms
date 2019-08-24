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
A Device must be related to an existing room.

#### Fields

- name: *string* - The name of the device.
- mac: *string* -  The MAC address of the device. Must be unique.

Example:

```json
{
  "id": "20335c53-6929-4b9d-900e-5548d99fd4e1",
  "name": "device1",
  "mac": "f6:f1:bb:06:31:71",
  "room": "5c8fa383-f9b7-4d80-9572-3276da1ab67d"
}
```

### Room

A Room is a (possibly empty) collection of devices.

#### Fields

- name: *string* - The name of the room.

Example:

```json
{
  "id": "5c8fa383-f9b7-4d80-9572-3276da1ab67d",
  "name": "Room1"
}
```

## Endpoints

- ### /rooms

    **GET**: return all registered rooms.

    **POST**: register a new room.
    Example body:
```json
{
  "name": "Room1"
}
```

- ### /rooms/{id}

    **GET**: return the specified room.
    
- ### /rooms/{id}/devices

    **GET**: return all registered devices belonging a specific room.

    **POST**: register a new device in a specific room.
    
    Example body:
```json
{
  "mac": "f6:f1:bb:06:31:71",
  "name": "device1"
}
```

- ### /rooms/{id}/devices/{id}

    **GET**: return the specified device of a specific room.

- ### /rooms/{id}/devices/{id}/readings

    **GET**: return all readings of the specified devices in a specific room.
    
    Optional query parameters
    
    - limit(n): limit the results obtained to the last n entries stored
    
    **POST**: register a new reading for the specified device.
    
    Example body:
```json
{
  "name": "temperature",
  "value": "22",
  "unit": "°C"
}
```

