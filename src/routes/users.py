from flask import Blueprint, jsonify
from http import HTTPStatus
from models import db, User
from utils import APIException

users_bp = Blueprint("users", __name__)

# SELECT user
# FROM users;


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
