from flask import Blueprint, Response, request, jsonify
from marshmallow import ValidationError
from flask_bcrypt import Bcrypt
from orm import User, System
from session import Session
from validation_schemas import UserSchema
from flask_jwt_extended import create_access_token
from flask_jwt_extended import get_jwt_identity
from flask_jwt_extended import jwt_required
from flask_jwt_extended import JWTManager

user = Blueprint('user', __name__)
bcrypt = Bcrypt()

session = Session()

@user.route('/api/v1/user', methods=['POST'])
def register():
    data = request.get_json(force=True)

    try:
        UserSchema().load(data)
    except ValidationError as err:
        return jsonify(err.messages), 400

    exists = session.query(User).filter_by(username=data['username']).first()
    if exists:
        return Response(status=400, response='User with such username already exists.')

    exists = session.query(User).filter_by(phone=data['phone']).first()
    if exists:
        return Response(status=400, response='User with such phone already exists.')

    exists = session.query(User).filter_by(email=data['email']).first()
    if exists:
        return Response(status=400, response='User with such email already exists.')

    hashed_password = bcrypt.generate_password_hash(data['password'])
    new_user = User(username=data['username'], firstName=data['firstName'], lastName=data['lastName'], password=hashed_password, email=data['email'], phone=data['phone'])

    session.add(new_user)
    session.commit()

    return Response(response='New user was successfully created!')

@user.route('/api/v1/user/<userId>', methods=['GET'])
@jwt_required()
def get_user(userId):
    userData = session.query(User).filter_by(id=userId).first()
    user = get_jwt_identity()
    if not userData:
        return Response(status=404, response='A user with provided ID was not found.')
    if (userData.username != user):
        return Response(status=404, response='You have no access to do this.')

    user_data = {'username': userData.username, 'firstName': userData.firstName, 'lastName': userData.lastName, 
                 'email': userData.email, 'phone': userData.phone }
    return jsonify({"user": user_data})


@user.route('/api/v1/user/<userId>', methods=['PUT'])
@jwt_required()
def update_user(userId):
    data = request.get_json(force=True)
    user = get_jwt_identity();
    try:
        UserSchema().load(data)
    except ValidationError as err:
        return jsonify(err.messages), 400
    userData = session.query(User).filter_by(id=userId).first()
    if not userData:
        return Response(status=404, response='A user with provided ID was not found.')
    if(user!=userData.username):
        return Response(status=404, response='You have no access to do this.')
    if 'username' in data.keys():
        exists = session.query(User).filter_by(username=data['username']).first()
        if exists:
            return Response(status=400, response='User with such username already exists.')
        userData.username = data['username']
    if 'firstName' in data.keys():
        userData.firstName = data['firstName']
    if "lastName" in data.keys():
        userData.lastName = data['lastName']
    if 'password' in data.keys():
        hashed_password = bcrypt.generate_password_hash(data['password'])
        userData.password = hashed_password
    if 'email' in data.keys():
        exists = session.query(User).filter_by(email=data['email']).first()
        if exists:
            return Response(status=400, response='User with such email already exists.')
        userData.email = data['email']
    if 'phone' in data.keys():
        exists = session.query(User).filter_by(phone=data['phone']).first()
        if exists:
            return Response(status=400, response='User with such phone already exists.')
        userData.phone = data['phone']
   

    session.commit()
    access_token = create_access_token(identity=data['username'])
    return jsonify({"access_token": access_token})


@user.route('/api/v1/user', methods=['DELETE'])
@jwt_required()
def delete_user():
    user = get_jwt_identity();
    userData = session.query(User).filter_by(username=user).first()
    if not userData:
        return Response(status=404, response='A user with provided ID was not found.')
   
    session.delete(userData)
    session.commit()
    return Response(response='User was deleted.')