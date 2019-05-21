from flask import Blueprint, jsonify, abort, request
from gfndevice.models import Device, Reading, Room
from gfndevice.db import db


bp = Blueprint('room', __name__)


def get_room(id):
	return Room.query.get(id)
	

@bp.route('/', methods=['GET', 'POST'])
def rooms():
	if request.method == 'POST':
		data = request.get_json()
		name = data.get("name", None)

		try:
			r = Room(name=name)

			db.session.add(r)
			db.session.commit()

			return jsonify(r.to_dict())
		except AssertionError as exception_message:
			abort(400, str(exception_message))

	return jsonify([r.to_dict() for r in Room.query.all()])


@bp.route('/<int:id>', methods=(['GET']))
def single_room(id):
	r = get_room(id)

	if not r:
		abort(404)

	return jsonify(r.to_dict())


@bp.route('/<int:id>/devices', methods=(['GET', 'POST']))
def room_device(id):
	r = get_room(id)

	if not r:
		abort(404)

	if request.method == 'POST':
		data = request.get_json()
		device_id = data.get("device_id", None)

		try:
			r.devices.append(device_id)

			db.session.commit()
		except AssertionError as exception_message:
			abort(400, str(exception_message))

	return jsonify([d.to_dict() for d in r.devices])

