from flask import Blueprint, Response, request, jsonify
from marshmallow import ValidationError
from flask_bcrypt import Bcrypt
from orm import System, User, Events
from sqlalchemy import and_
from session import session
from validation_schemas import InputEventsSchema
from flask_jwt_extended import create_access_token
from flask_jwt_extended import get_jwt_identity
from flask_jwt_extended import jwt_required
from flask_jwt_extended import JWTManager

system = Blueprint('system', __name__)
bcrypt = Bcrypt()

@system.route('/api/v1/system', methods=['GET'])
@jwt_required()
def getEvents():
    logged = get_jwt_identity()
    user = session.query(User).filter_by(username=logged).first()
    userData = session.query(System).filter_by(userId=user.id)
    output = []
    for i in userData:
        temp = session.query(Events).filter_by(id=i.eventId).first()
        output.append({'id': temp.id,
                       'header': temp.header,
                       'description': temp.description,
                       'date': temp.date,})
    res = jsonify(output)
    return res

@system.route('/api/v1/system/<username>', methods=['POST'])
@jwt_required()
def addUserToEvent(username):
    data = request.get_json(force=True)

    try:
        InputEventsSchema().load(data)
    except ValidationError as err:
        return jsonify(err.messages), 400
    logged = get_jwt_identity()
    user = session.query(User).filter_by(username=logged).first()
    new_user = session.query(User).filter_by(username=username).first()
    if not new_user:
        return Response(status=404, response='User with such username was not found.')

    exists = session.query(Events.id).filter_by(id=data['eventId']).first()
    if not exists:
        return Response(status=404, response='Event with such id was not found.')
    exists = session.query(System).filter(and_(System.userId==user.id, System.eventId==data['eventId'])).first()
    if not exists:
         return Response(status=404, response='You have no access to do this.')
    new_system = System(userId=new_user.id, eventId=data['eventId'])
    session.add(new_system)
    session.commit()
    session.close()
    return Response(response='User was successfully added!')