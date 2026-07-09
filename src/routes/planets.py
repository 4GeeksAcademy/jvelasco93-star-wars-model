from flask import Blueprint, jsonify
from http import HTTPStatus
from models import db, Planet
from utils import APIException

planets_bp = Blueprint("planets", __name__)


@planets_bp.route("/planets", methods=["GET"])
def get_planets():
    try:
        planets = db.session.execute(db.select(Planet)).scalars().all()
        return jsonify([planet.serialize() for planet in planets]), HTTPStatus.OK
    except Exception as e:
        raise APIException(
            str(e), status_code=HTTPStatus.INTERNAL_SERVER_ERROR)


@planets_bp.route("/planets/<int:planet_id>", methods=["GET"])
def get_planet(planet_id):
    if planet_id < 0:
        raise APIException("Invalid planet ID",
                           status_code=HTTPStatus.BAD_REQUEST)

    try:
        planet = db.session.get(Planet, planet_id)
        if not planet:
            raise APIException("Planet not found",
                               status_code=HTTPStatus.NOT_FOUND)
        return jsonify(planet.serialize()), HTTPStatus.OK
    except APIException:
        raise
    except Exception as e:
        raise APIException(
            str(e), status_code=HTTPStatus.INTERNAL_SERVER_ERROR)
