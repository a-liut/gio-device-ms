import os

from flask import Flask, request, jsonify


def wrap_error(error=None):
    message = {
            'status': error.code,
            'message': error.description,
    }
    resp = jsonify(message)
    resp.status_code = error.code

    return resp

def create_app(test_config=None):
    """Create and configure an instance of the Flask application."""
    app = Flask(__name__, instance_relative_config=True)
    if test_config is None:
        print("DB: Using DevConfig...")
        app.config.from_object('gfndevice.settings.DevConfig')
    else:
        print("DB: Using test_config...")
        app.config.from_object(test_config)

    # ensure the instance folder exists
    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass

    # apply the blueprints to the app
    from gfndevice import device
    app.register_blueprint(device.bp, url_prefix='/devices')

    # Initialize db
    from gfndevice.db import db
    with app.app_context():
        db.init_app(app)

        db.create_all()


    app.register_error_handler(404, wrap_error)
    app.register_error_handler(400, wrap_error)

    return app