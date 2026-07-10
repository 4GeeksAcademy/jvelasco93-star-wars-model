from flask import Blueprint, jsonify
from http import HTTPStatus
from models import Character, Planet, Vehicle, db, User
from utils import APIException

users_bp = Blueprint("users", __name__)


@users_bp.route("/users", methods=["GET"])
def get_users():
    try:
        users: list[User] = db.session.execute(db.select(User)).scalars().all()
        return jsonify([
            user.serialize() for user in users
        ])
    except Exception as e:
        raise APIException(
            str(e), status_code=HTTPStatus.INTERNAL_SERVER_ERROR)


@users_bp.route("/users/<int:user_id>", methods=["GET"])
def get_user(user_id):
    if user_id < 0:
        raise APIException("Invalid user ID",
                           status_code=HTTPStatus.BAD_REQUEST)

    try:
        user = db.session.get(User, user_id)
        if not user:
            raise APIException(
                "User not found", status_code=HTTPStatus.NOT_FOUND)
        return jsonify(user.serialize()), HTTPStatus.OK
    except APIException:
        raise
    except Exception as e:
        raise APIException(
            str(e), status_code=HTTPStatus.INTERNAL_SERVER_ERROR)


@users_bp.route('/users/<int:user_id>/favorites', methods=['GET'])
def get_user_favorites(user_id: int):
    if user_id < 0:
        raise APIException("Invalid user ID",
                           status_code=HTTPStatus.BAD_REQUEST)

    try:
        user = db.session.get(User, user_id)
        if not user:
            raise APIException(
                "User not found", status_code=HTTPStatus.NOT_FOUND)

        return jsonify({
            "planets": [planet.serialize() for planet in user.favorite_planets],
            "characters": [planet.serialize() for planet in user.favorite_characters],
            "vehicles": [vehicle.serialize() for vehicle in user.favorite_vehicles],
        }), HTTPStatus.OK
    except APIException:
        raise
    except Exception as e:
        raise APIException(
            str(e), status_code=HTTPStatus.INTERNAL_SERVER_ERROR)


@users_bp.route('/users/<int:user_id>/favorites/planets/<int:planet_id>', methods=['DELETE'])
def delete_favorite_planet(user_id: int, planet_id: int):
    try:
        user = db.session.get(User, user_id)
        if not user:
            raise APIException(
                "User not found", status_code=HTTPStatus.NOT_FOUND)

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


@users_bp.route("/users/<int:user_id>/favorites/characters/<int:character_id>", methods=["DELETE"])
def delete_favorite_character(user_id, character_id):
    try:
        user = db.session.get(User, user_id)
        if not user:
            raise APIException(
                "User not found", status_code=HTTPStatus.NOT_FOUND)

        character = db.session.get(Character, character_id)
        if not character:
            raise APIException("Character not found",
                               status_code=HTTPStatus.NOT_FOUND)

        if character not in user.favorite_characters:
            raise APIException("Character is not in favorites",
                               status_code=HTTPStatus.NOT_FOUND)

        user.favorite_characters.remove(character)
        db.session.commit()
        return jsonify({"msg": "Character removed from favorites"}), HTTPStatus.OK
    except APIException:
        raise
    except Exception as e:
        raise APIException(
            str(e), status_code=HTTPStatus.INTERNAL_SERVER_ERROR)


@users_bp.route("/users/<int:user_id>/favorites/vehicles/<int:vehicle_id>", methods=["DELETE"])
def delete_favorite_vehicle(user_id, vehicle_id):
    try:
        user = db.session.get(User, user_id)
        if not user:
            raise APIException(
                "User not found", status_code=HTTPStatus.NOT_FOUND)

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
