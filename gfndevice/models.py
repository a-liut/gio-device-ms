import re

from gfndevice.db import db
from datetime import datetime
from sqlalchemy.orm import validates

class Device(db.Model):
    __tablename__ = 'devices'
    id = db.Column(db.Integer, primary_key=True)
    mac = db.Column(db.String(17), nullable=False, unique=True) # MACs are 12 digits + 5 ':'

    readings = db.relationship('Reading', back_populates="device")


    @validates('mac')
    def validate_mac(self, key, mac):
        if not mac:
            raise AssertionError("No MAC provided")

        if not re.match("[0-9a-f]{2}([-:]?)[0-9a-f]{2}(\\1[0-9a-f]{2}){4}$", mac.lower()):
            raise AssertionError("Invalid MAC address")

        if Device.query.filter_by(mac=mac).first():
            raise AssertionError("MAC already in use")

        return mac


    def to_dict(self):
        return {
            "id": self.id,
            "mac": self.mac
        }


    def __repr__(self):
        return "<Device {}, mac={}>".format(self.id, self.mac)


class Reading(db.Model):
    __tablename__ = 'readings'
    id = db.Column(db.Integer, primary_key=True)
    timestamp = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    temperature = db.Column(db.Integer, nullable=False)
    moisture = db.Column(db.Integer, nullable=False)
    light = db.Column(db.Integer, nullable=False)

    device_id = db.Column(db.Integer, db.ForeignKey('devices.id'), nullable=False)
    device = db.relationship('Device', back_populates="readings")


    @validates('temperature', 'moisture', 'light')
    def validate_positive_int(self, key, value):
        if not value:
            raise AssertionError("No {} value provided".format(key))

        if value < 0:
            raise AssertionError("Invalid {} value".format(key))

        return value


    def to_dict(self):
        return {
            "id": self.id,
            "timestamp": self.timestamp,
            "temperature": self.temperature,
            "moisture": self.moisture,
            "light": self.light,
            "device": self.device.id
        }


    def __repr__(self):
        return "<Reading {}, temperature={}, moisture={}, light={}>".format(self.id, self.temperature, self.moisture, self.light)
