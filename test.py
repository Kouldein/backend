from flask_jwt_extended import create_access_token
from flask import jsonify
from app import app
from session import Session, some_engine
from orm import User, Base, System, Events
from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine
import json
from datetime import datetime
some_engine = create_engine('mysql+pymysql://root:22andriy@127.0.0.1:3306/pplab_6')

Session = sessionmaker(bind=some_engine)

session = Session()


app_context = app.app_context()
app_context.push()

client = app.test_client()

def test_create_user():
    send_data = {
        "username": "pipasd",
        "firstName": "abdul",
        "lastName": "hamid",
        "password": "Basiloks",
        "email": "iam@mail.ua",
        "phone": "+380665066053"
    }

    url ='/api/v1/user'
    response = client.post(url, data=json.dumps(send_data),content_type='application/json')
    #session.query(User).filter_by(username = send_data["username"]).delete()
    assert response.status_code == 200


def test_create_user_invalid():
    send_data = {
        'username': "pytest",
        'first_name': "pytest",
        'last_name': "pytest",
        'password': "pytest",
        'email': "pytest@gmail.com",
        'phone': "+380465965"
    }

    url ='/api/v1/user'
    response = client.post(url, data=json.dumps(send_data),content_type='application/json')
    assert response.status_code == 400

def test_create_user_invalid_1():  
    send_data = {
        'username': "pipasd",
        'first_name': "pytest",
        'last_name': "pytest",
        'password': "pytesting",
        'email': "pytest@gmail.com",
        'phone': "+380465965"
    }

    url ='/api/v1/user'
    response = client.post(url, data=json.dumps(send_data),content_type='application/json')
    assert response.status_code == 400

def test_create_user_invalid_2():
    send_data = {
        'username': "kokd",
        'first_name': "pytest",
        'last_name': "pytest",
        'password': "pytesting",
        'email': "iam@mail.ua",
        'phone': "+380465965"
    }

    url ='/api/v1/user'
    response = client.post(url, data=json.dumps(send_data),content_type='application/json')
    assert response.status_code == 400

def test_create_user_invalid_3():
    send_data = {
        'username': "kokx",
        'first_name': "pytest",
        'last_name': "pytest",
        'password': "pytesting",
        'email': "pytest@gmail.com",
        'phone': "+380665066053"
    }

    url ='/api/v1/user'
    response = client.post(url, data=json.dumps(send_data),content_type='application/json')
    assert response.status_code == 400
    
def test_get_user():
    user1 = session.query(User).filter_by(username = "pipasd").first()
    access_token = create_access_token(identity='pipasd')
    headers = {
        'Authorization': 'Bearer {}'.format(access_token)
    }
    url ='/api/v1/user/'+str(user1.id)
    response = client.get(url, headers=headers)
    assert response.status_code == 200
    assert json.loads(response.data) == {"user":{
        "username": "pipasd",
        "firstName": "abdul",
        "lastName": "hamid",
        "phone": "+380665066053",
        "email": "iam@mail.ua"
    }}
    session.commit()

def test_update_user():
    send_data = {
        "username": "pipa",
        "firstName": "abdul",
        "lastName": "hamid",
        "password": "Basil",
        "email": "ia@mail.ua",
        "phone": "+38066066053"
    }
    user = session.query(User).filter_by(username = "pipasd").first()
    access_token = create_access_token(identity=user.username)
    headers = {
        'Authorization': 'Bearer {}'.format(access_token)
    }
    url ='/api/v1/user/'+str(user.id)
    response = client.put(url,data=json.dumps(send_data),content_type='application/json', headers=headers)
    send_data = {
        "username": "pipas",
        "firstName": "abdul",
        "lastName": "hamid",
        "password": "Basilokss",
        "email": "ia@mail.ua",
        "phone": "+38066066053"
    }
    
    user = session.query(User).filter_by(username = "pipasd").first()
    access_token = create_access_token(identity=user.username)
    headers = {
        'Authorization': 'Bearer {}'.format(access_token)
    }
    url ='/api/v1/user/'+str(user.id)
    response = client.put(url,data=json.dumps(send_data),content_type='application/json', headers=headers)
    
    assert response.status_code == 200
    send_data = {
        "username": "pipas",
        "password": "Basilokss"
    }
    url ='/api/v1/login'
    response = client.get(url,data=json.dumps(send_data),content_type='application/json', headers=headers)
    assert response.status_code == 200
    user = session.query(User).filter_by(username = "pipas").delete()
    session.commit()

def test_delete_user():
    send_data = {
        "username": "pipasd",
        "firstName": "abdul",
        "lastName": "hamid",
        "password": "Basiloks",
        "email": "iam@mail.ua",
        "phone": "+380665066053"
    }

    url ='/api/v1/user'
    response = client.post(url, data=json.dumps(send_data),content_type='application/json')
    session.commit()
    user = session.query(User).filter_by(username = "pipasd").first()
    access_token = create_access_token(identity=user.username)
    headers = {
        'Authorization': 'Bearer {}'.format(access_token)
    }
    url ='/api/v1/user'
    response = client.delete(url, headers=headers)
    session.commit()
    assert response.status_code == 200

def test_create_event():
    send_data = {
        "username": "pipasd",
        "firstName": "abdul",
        "lastName": "hamid",
        "password": "Basiloks",
        "email": "iam@mail.ua",
        "phone": "+380665066053"
    }

    url ='/api/v1/user'
    response = client.post(url, data=json.dumps(send_data),content_type='application/json')
    session.commit()
    user = session.query(User).filter_by(username = "pipasd").first()
    access_token = create_access_token(identity=user.username)
    headers = {
        'Authorization': 'Bearer {}'.format(access_token)
    }
    send_data = {
         'header': "something",
         'description': "something",
         'date': "2011-11-03 18:21:26"
    }
    url ='/api/v1/events'
    response = client.post(url, data=json.dumps(send_data),content_type='application/json', headers=headers)
    session.commit()
    assert response.status_code == 200
    url ='/api/v1/system'
    response = client.get(url, headers=headers)
    assert response.status_code == 200
    send_data = {
         'header': "somethin",
         'description': "somethin",
         'date': "2011-11-03 18:21:25"
    }
    temp = session.query(Events).order_by(Events.id.desc()).first()
    url ='/api/v1/events/'+str(temp.id)
    response = client.get(url, headers=headers)
    assert response.status_code == 200
    response = client.put(url, data=json.dumps(send_data),content_type='application/json', headers=headers)
    session.commit()
    assert response.status_code == 200
    session.query(System).filter_by(userId = user.id).delete()
    session.query(User).filter_by(id = user.id).delete()
    session.query(Events).filter_by(header = "somethin").delete()
    session.commit()

def test_get_events():
    url ='/api/v1/events'
    response = client.get(url)
    assert response.status_code == 200

def test_delete_events():
    send_data = {
        "username": "pipasd",
        "firstName": "abdul",
        "lastName": "hamid",
        "password": "Basiloks",
        "email": "iam@mail.ua",
        "phone": "+380665066053"
    }

    url ='/api/v1/user'
    response = client.post(url, data=json.dumps(send_data),content_type='application/json')
    session.commit()
    user = session.query(User).filter_by(username = "pipasd").first()
    access_token = create_access_token(identity=user.username)
    headers = {
        'Authorization': 'Bearer {}'.format(access_token)
    }
    send_data = {
         'header': "some",
         'description': "something",
         'date': "2011-11-03 18:21:26"
    }
    url ='/api/v1/events'
    response = client.post(url, data=json.dumps(send_data),content_type='application/json', headers=headers)
    session.commit()
    temp = session.query(Events).order_by(Events.id.desc()).first()
    session.commit()
    session.query(System).filter_by(userId = user.id).delete()
    session.commit()
    url ='/api/v1/events/'+str(temp.id)
    response = client.delete(url, headers=headers)
    session.query(User).filter_by(id = user.id).delete()
    session.commit()
    assert response.status_code == 200



    

    