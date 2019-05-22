from flask import Blueprint, jsonify, abort, request
from gfndevice.models import Device, Reading, Room
from gfndevice.db import db


bp = Blueprint('device', __name__)


def get_device(id):
	return Device.query.get(id)
	

@bp.route('/', methods=['GET', 'POST'])
def device():
	if request.method == 'POST':
		data = request.get_json()
		mac = data.get("mac", None)
		name = data.get("name", None)
		room_id = data.get("room_id", None)

		try:
			r = None

			if room_id:
				r = Room.query.get(int(room_id))
			
			if not r:
				r = Room.create()
				db.session.add(r)
				db.session.flush()

			d = Device(mac=mac, name=name, room_id=r.id)

			db.session.add(d)
			db.session.commit()

			return jsonify(d.to_dict())
		except AssertionError as exception_message:
			abort(400, str(exception_message))

	return jsonify([d.to_dict() for d in Device.query.all()])


@bp.route('/<int:id>', methods=(['GET']))
def single_device(id):
	d = get_device(id)

	if not d:
		abort(404)

	return jsonify(d.to_dict())


@bp.route('/<int:id>/readings', methods=['GET', 'POST'])
def readings(id):
	d = get_device(id)

	if not d:
		abort(404)

	if request.method == 'POST':
		data = request.get_json()

		name = data.get("name", None)
		value = data.get("value", None)
		unit = data.get("unit", None)

		try:
			r = Reading(name=name, value=value, unit=unit, device = d)

			db.session.add(r)
			db.session.commit()

			return jsonify(r.to_dict())
		except AssertionError as exception_message:
			abort(400, str(exception_message))

	return jsonify([r.to_dict() for r in d.readings])
