from flask import Blueprint, jsonify, abort, request
from gfndevice.models import Device, Reading
from gfndevice.db import db


bp = Blueprint('device', __name__)


def get_device(id):
	return Device.query.get(id)
	

@bp.route('/', methods=['GET', 'POST'])
def device():
	if request.method == 'POST':
		data = request.get_json()
		mac = data.get("mac", None)

		try:
			d = Device(mac=mac)

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
		temperature = data.get("temperature", None)
		light = data.get("light", None)
		moisture = data.get("moisture", None)

		try:
			r = Reading(temperature = temperature, light = light, moisture = moisture, device = d)

			db.session.add(r)
			db.session.commit()

			return jsonify(r.to_dict())
		except AssertionError as exception_message:
			abort(400, str(exception_message))

	return jsonify([r.to_dict() for r in d.readings])
