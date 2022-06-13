from flask import Blueprint, Response, request, jsonify
from marshmallow import ValidationError
from flask_bcrypt import Bcrypt
from orm import User, System
from session import session
from validation_schemas import UserSchema, LoginSchema
from flask_jwt_extended import create_access_token
from flask_jwt_extended import get_jwt_identity
from flask_jwt_extended import jwt_required
from flask_jwt_extended import JWTManager

login = Blueprint('login', __name__)
bcrypt = Bcrypt()

@login.route('/api/v1/login', methods=['POST'])
def logining():
    data = request.get_json(force=True)
    try:
        LoginSchema().load(data)
    except ValidationError as err:
        return jsonify(err.messages), 400
    exist = session.query(User).filter_by(username=data['username']).first()
    access_token = create_access_token(identity=data['username'])
    if exist and bcrypt.check_password_hash(exist.password, data['password']):
            return jsonify(access_token)
    else:
        return Response(status=404, response='Invalid username or password.')
   