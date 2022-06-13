from logging.config import fileConfig

from sqlalchemy import engine_from_config
from sqlalchemy import pool

from alembic import context

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from orm import User, Events, System

some_engine = create_engine('mysql+pymysql://root:22andriy@127.0.0.1:3306/pplab_6')

Session = sessionmaker(bind=some_engine)

session = Session()

if __name__ == "__main__":
    user1 = User(username="Clo", firstName="Ivan", lastName="Piddubniy", password="Dub3", email="Piddubniy@mail.ru", phone="+380682356355")
    user2 = User(username="Clon", firstName="Iva", lastName="Piubniy", password="Dub", email="Iddubniy@mail.ru", phone="+380682346355")
    event1 = Events(header="Something important", description="Something really important", date="2021-11-11")
    systemCall = System(userId=1, eventId=1)
    systemCall1 = System(userId=2, eventId=1)
    session.add(user1)
    session.add(user2)
    session.add(event1)
    session.add(systemCall)
    session.add(systemCall1)
    session.commit()
