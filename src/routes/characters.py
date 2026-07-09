from flask import Blueprint, jsonify
from http import HTTPStatus
from models import db, Character
from utils import APIException

characters_bp = Blueprint("characters", __name__)


@characters_bp.route("/characters", methods=["GET"])
def get_characters():
    try:
        characters = db.session.execute(db.select(Character)).scalars().all()
        return jsonify([character.serialize() for character in characters]), HTTPStatus.OK
    except Exception as e:
        raise APIException(
            str(e), status_code=HTTPStatus.INTERNAL_SERVER_ERROR)


@characters_bp.route("/characters/<int:character_id>", methods=["GET"])
def get_character(character_id):
    if character_id < 0:
        raise APIException("Invalid character ID",
                           status_code=HTTPStatus.BAD_REQUEST)

    try:
        character = db.session.get(Character, character_id)
        if not character:
            raise APIException("Character not found",
                               status_code=HTTPStatus.NOT_FOUND)
        return jsonify(character.serialize()), HTTPStatus.OK
    except APIException:
        raise
    except Exception as e:
        raise APIException(
            str(e), status_code=HTTPStatus.INTERNAL_SERVER_ERROR)
