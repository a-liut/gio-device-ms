# gio-device-ms

The Devices microservice handles rooms and devices registration and devices data storage.
It provides a REST API that allows the Device Driver to register rooms and devices and store their data.
Each devices is associated with an unique identifier (UUID).

All the registering operations are *idempotent*: if a room or a device, identified respectively by their name and MAC address, are registered multiple times, the same UUID is given as response. This allows to preserve the history of the device and handles disconnections from the system.

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

## REST API

- ### /rooms
    
        **GET**: return all registered rooms.
    
        **POST**: register a new room.
    
    Example body:
    ```json
    {
      "name": "Room1"
    }
    ```

- ### /rooms/{roomId}

    **GET**: return the specified room.
    
- ### /rooms/{roomId}/devices

    **GET**: return all registered devices belonging a specific room.

    **POST**: register a new device in a specific room.
    
    Example body:
    ```json
    {
      "mac": "f6:f1:bb:06:31:71",
      "name": "device1"
    }
    ```

- ### /rooms/{roomId}/devices/{deviceId}

    **GET**: return the specified device of a specific room.

- ### /rooms/{roomId}/devices/{deviceId}/readings

    **GET**: return all readings of the specified devices in a specific room.
    
    Optional query parameters
    
    - limit(n): limit the results obtained to the last n entries stored
    
    - name(s): filter the entries to those who have `s` as name
    
    **POST**: register a new reading for the specified device.
    
    Example body:
    ```json
    {
      "name": "temperature",
      "value": "22",
      "unit": "°C"
    }
    ```

- ### /rooms/{roomId}/devices/{deviceId}/actions/{actionName}

    **POST**: trigger the requested action if possible
    
    Example response:
    
    - Successful response
      ```json
      {
        "message": "Done"
      }
      ```
    - Action not available
      ```json
      {
        "message":"action not recognized: test"
      }
      ```
