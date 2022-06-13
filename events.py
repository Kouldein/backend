from flask import Blueprint, Response, request, jsonify
from marshmallow import ValidationError
from flask_bcrypt import Bcrypt
from orm import Events, System, User
from sqlalchemy import and_
from session import session
from validation_schemas import EventsSchema
from flask_jwt_extended import create_access_token
from flask_jwt_extended import get_jwt_identity
from flask_jwt_extended import jwt_required
from flask_jwt_extended import JWTManager

events = Blueprint('events', __name__)
bcrypt = Bcrypt()

@events.route('/api/v1/events', methods=['POST'])
@jwt_required()
def createEvent():
    data = request.get_json(force=True)

    try:
        EventsSchema().load(data)
    except ValidationError as err:
        return jsonify(err.messages), 400

    logged = get_jwt_identity()
    user = session.query(User).filter_by(username=logged).first()
    newEvent = Events(header=data['header'], description=data['description'], date=data['date'])
    session.add(newEvent)
    session.commit()
    newLink = System(userId=user.id, eventId=newEvent.id)
    session.add(newLink)
    session.commit()

    return Response(response='New event was successfully created!')

@events.route('/api/v1/events', methods=['GET'])
def getEvents():
    event = session.query(Events)
    output = []
    for i in event:
        output.append({'id': i.id,
                       'header': i.header,
                       'description': i.description,
                       'date': i.date})
    res = jsonify(output)
    return res

@events.route('/api/v1/events/<eventId>', methods=['GET'])
@jwt_required()
def getEvent(eventId):
    eventData = session.query(Events).filter_by(id=eventId).first()
    if not eventData:
        return Response(status=404, response='An event with provided ID was not found.')
    logged = get_jwt_identity()
    user = session.query(User).filter_by(username=logged).first()
    exist = session.query(System).filter(and_(System.userId==user.id, System.eventId==eventData.id)).first()
    if not exist:
         return Response(status=404, response='You have no access to do this.')
    event_data = {
        'id': eventData.id,
        'header': eventData.header,
        'description': eventData.description,
        'date': eventData.date
    }
    return jsonify({"event": event_data})

@events.route('/api/v1/events/<eventId>', methods=['PUT'])
@jwt_required()
def updateEvent(eventId):
    data = request.get_json(force=True)

    try:
        EventsSchema().load(data)
    except ValidationError as err:
        return jsonify(err.messages), 400

    eventData = session.query(Events).filter_by(id=eventId).first()
    if not eventData:
        return Response(status=404, response='An event with provided ID was not found.')
    logged = get_jwt_identity()
    user = session.query(User).filter_by(username=logged).first()
    exist = session.query(System).filter(and_(System.userId==user.id, System.eventId==eventId)).first()
    if not exist:
         return Response(status=404, response='You have no access to do this.')
    if 'header' in data.keys():
        eventData.header = data['header']
    if 'description' in data.keys():
        eventData.description = data['description']
    if 'date' in data.keys():
        eventData.date = data['date']

    session.commit()
    session.close()
    
    return Response(response='Event was updated.') 


@events.route('/api/v1/events/<eventid>', methods=['DELETE'])
@jwt_required()
def deleteEvent(eventid):
    eventData = session.query(Events).filter_by(id=eventid).first()
    exist = session.query(System).filter_by(eventId=eventid).first()
    if not eventData:
        return Response(status=402, response='An event with provided ID was not found.')
    logged = get_jwt_identity()
    user = session.query(User).filter_by(username=logged).first()
    exists = session.query(System).filter(and_(System.userId==1000, System.eventId==eventid)).first()
    if exists:
         return Response(status=402, response='You have no access to do this.')
    if exist:
        return Response(status=400, response='A event with provided ID a foreign key.')
    session.delete(eventData)
    session.commit()
    session.close()
    return Response(response='Event was deleted.')