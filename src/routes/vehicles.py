from flask import Blueprint, jsonify
from http import HTTPStatus
from models import db, Vehicle
from utils import APIException

vehicles_bp = Blueprint("vehicles", __name__)


@vehicles_bp.route("/vehicles", methods=["GET"])
def get_vehicles():
    try:
        vehicles = db.session.execute(db.select(Vehicle)).scalars().all()
        return jsonify([vehicle.serialize() for vehicle in vehicles]), HTTPStatus.OK
    except Exception as e:
        raise APIException(
            str(e), status_code=HTTPStatus.INTERNAL_SERVER_ERROR)


@vehicles_bp.route("/vehicles/<int:vehicle_id>", methods=["GET"])
def get_vehicle(vehicle_id):
    if vehicle_id < 0:
        raise APIException("Invalid vehicle ID",
                           status_code=HTTPStatus.BAD_REQUEST)

    try:
        vehicle = db.session.get(Vehicle, vehicle_id)
        if not vehicle:
            raise APIException("Vehicle not found",
                               status_code=HTTPStatus.NOT_FOUND)
        return jsonify(vehicle.serialize()), HTTPStatus.OK
    except APIException:
        raise
    except Exception as e:
        raise APIException(
            str(e), status_code=HTTPStatus.INTERNAL_SERVER_ERROR)
