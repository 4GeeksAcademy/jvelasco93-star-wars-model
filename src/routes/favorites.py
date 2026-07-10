from flask import Blueprint, jsonify, request
from http import HTTPStatus
from models import db, User, Planet, Character, Vehicle
from utils import APIException

favorites_bp = Blueprint("favorites", __name__)


def _get_user_from_query():
    user_id = request.args.get("user_id", type=int)
    if user_id is None or user_id < 0:
        raise APIException(
            "user_id is required and must be a valid ID", status_code=HTTPStatus.BAD_REQUEST)
    user = db.session.get(User, user_id)
    if not user:
        raise APIException("User not found", status_code=HTTPStatus.NOT_FOUND)
    return user


@favorites_bp.route("/favorite/planet/<int:planet_id>", methods=["POST"])
def add_favorite_planet(planet_id):
    if planet_id < 0:
        raise APIException("Invalid planet ID",
                           status_code=HTTPStatus.BAD_REQUEST)

    try:
        user = _get_user_from_query()

        planet = db.session.get(Planet, planet_id)
        if not planet:
            raise APIException("Planet not found",
                               status_code=HTTPStatus.NOT_FOUND)

        if planet in user.favorite_planets:
            raise APIException("Planet already in favorites",
                               status_code=HTTPStatus.CONFLICT)

        user.favorite_planets.append(planet)
        db.session.commit()
        return jsonify({"msg": "Planet added to favorites"}), HTTPStatus.CREATED
    except APIException:
        raise
    except Exception as e:
        raise APIException(
            str(e), status_code=HTTPStatus.INTERNAL_SERVER_ERROR)


@favorites_bp.route("/favorite/people/<int:people_id>", methods=["POST"])
def add_favorite_people(people_id):
    if people_id < 0:
        raise APIException("Invalid people ID",
                           status_code=HTTPStatus.BAD_REQUEST)

    try:
        user = _get_user_from_query()

        character = db.session.get(Character, people_id)
        if not character:
            raise APIException("People not found",
                               status_code=HTTPStatus.NOT_FOUND)

        if character in user.favorite_characters:
            raise APIException("People already in favorites",
                               status_code=HTTPStatus.CONFLICT)

        user.favorite_characters.append(character)
        db.session.commit()
        return jsonify({"msg": "People added to favorites"}), HTTPStatus.CREATED
    except APIException:
        raise
    except Exception as e:
        raise APIException(
            str(e), status_code=HTTPStatus.INTERNAL_SERVER_ERROR)


@favorites_bp.route("/favorite/planet/<int:planet_id>", methods=["DELETE"])
def delete_favorite_planet(planet_id):
    if planet_id < 0:
        raise APIException("Invalid planet ID",
                           status_code=HTTPStatus.BAD_REQUEST)

    try:
        user = _get_user_from_query()

        planet = db.session.get(Planet, planet_id)
        if not planet:
            raise APIException("Planet not found",
                               status_code=HTTPStatus.NOT_FOUND)

        if planet not in user.favorite_planets:
            raise APIException("Planet is not in favorites",
                               status_code=HTTPStatus.NOT_FOUND)

        user.favorite_planets.remove(planet)
        db.session.commit()
        return jsonify({"msg": "Planet removed from favorites"}), HTTPStatus.OK
    except APIException:
        raise
    except Exception as e:
        raise APIException(
            str(e), status_code=HTTPStatus.INTERNAL_SERVER_ERROR)


@favorites_bp.route("/favorite/people/<int:people_id>", methods=["DELETE"])
def delete_favorite_people(people_id):
    if people_id < 0:
        raise APIException("Invalid people ID",
                           status_code=HTTPStatus.BAD_REQUEST)

    try:
        user = _get_user_from_query()

        character = db.session.get(Character, people_id)
        if not character:
            raise APIException("People not found",
                               status_code=HTTPStatus.NOT_FOUND)

        if character not in user.favorite_characters:
            raise APIException("People is not in favorites",
                               status_code=HTTPStatus.NOT_FOUND)

        user.favorite_characters.remove(character)
        db.session.commit()
        return jsonify({"msg": "People removed from favorites"}), HTTPStatus.OK
    except APIException:
        raise
    except Exception as e:
        raise APIException(
            str(e), status_code=HTTPStatus.INTERNAL_SERVER_ERROR)


@favorites_bp.route("/favorite/vehicle/<int:vehicle_id>", methods=["POST"])
def add_favorite_vehicle(vehicle_id):
    if vehicle_id < 0:
        raise APIException("Invalid vehicle ID",
                           status_code=HTTPStatus.BAD_REQUEST)

    try:
        user = _get_user_from_query()

        vehicle = db.session.get(Vehicle, vehicle_id)
        if not vehicle:
            raise APIException("Vehicle not found",
                               status_code=HTTPStatus.NOT_FOUND)

        if vehicle in user.favorite_vehicles:
            raise APIException("Vehicle already in favorites",
                               status_code=HTTPStatus.CONFLICT)

        user.favorite_vehicles.append(vehicle)
        db.session.commit()
        return jsonify({"msg": "Vehicle added to favorites"}), HTTPStatus.CREATED
    except APIException:
        raise
    except Exception as e:
        raise APIException(
            str(e), status_code=HTTPStatus.INTERNAL_SERVER_ERROR)


@favorites_bp.route("/favorite/vehicle/<int:vehicle_id>", methods=["DELETE"])
def delete_favorite_vehicle(vehicle_id):
    if vehicle_id < 0:
        raise APIException("Invalid vehicle ID",
                           status_code=HTTPStatus.BAD_REQUEST)

    try:
        user = _get_user_from_query()

        vehicle = db.session.get(Vehicle, vehicle_id)
        if not vehicle:
            raise APIException("Vehicle not found",
                               status_code=HTTPStatus.NOT_FOUND)

        if vehicle not in user.favorite_vehicles:
            raise APIException("Vehicle is not in favorites",
                               status_code=HTTPStatus.NOT_FOUND)

        user.favorite_vehicles.remove(vehicle)
        db.session.commit()
        return jsonify({"msg": "Vehicle removed from favorites"}), HTTPStatus.OK
    except APIException:
        raise
    except Exception as e:
        raise APIException(
            str(e), status_code=HTTPStatus.INTERNAL_SERVER_ERROR)
