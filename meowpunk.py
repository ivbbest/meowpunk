from sqlalchemy import create_engine, MetaData, Table, Column, Integer, String, Text, Date
from sqlalchemy.sql import select, join, text
from sqlalchemy import create_engine
from sqlalchemy.engine.url import URL

from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, Date
from sqlalchemy.orm import sessionmaker
from config import DATABASE, client_file, server_file, cheaters_db

import pandas as pd


Base = declarative_base()

# Создаем объект Engine, который будет использоваться объектами ниже для связи с БД
engine = create_engine(URL.create(**DATABASE))
# Метод create_all создает таблицы в БД , определенные с помощью  DeclarativeBase
Base.metadata.create_all(engine)
# Создаем фабрику для создания экземпляров Session. Для создания фабрики в аргументе
# bind передаем объект engine
Session = sessionmaker(bind=engine)
# Создаем объект сессии из фабрики Session
session = Session()


class Result(Base):
    __tablename__ = 'result'

    id = Column(Integer, primary_key=True)
    timestamp = Column(Date)
    player_id = Column(Integer)
    event_id = Column(String)
    error_id = Column(String)
    json_server = Column(Text)
    json_client = Column(Text)


class Client(Base):
    __tablename__ = 'client'

    # id = Column(Integer, primary_key=True)
    timestamp = Column(Date)
    player_id = Column(Integer)
    error_id = Column(String, primary_key=True)
    json = Column(Text)


class Server(Base):
    __tablename__ = 'server'

    # id = Column(Integer, primary_key=True)
    timestamp = Column(Date)
    event_id = Column(String)
    error_id = Column(String, primary_key=True)
    json = Column(Text)


class Cheaters(Base):
    __tablename__ = 'cheaters'

    player_id = Column(Integer, primary_key=True)
    ban_time = Column(String)


def csv_to_sql(file_name, table_name):
    df = pd.read_csv(file_name)
    df.to_sql(con=engine, name=table_name, if_exists='append')


def table_into_db(db_name, table_name):
    cnx = create_engine(f'sqlite:///{db_name}')
    df = pd.read_sql_table(db_name.split('.')[0], cnx)
    df.to_sql(con=engine, name=table_name, if_exists='append')


# csv_to_sql(server_file, 'server')
# csv_to_sql(client_file, 'client')
# table_into_db(cheaters_db, 'cheaters')

q = session.query(Client, Server)\
                    .join(Server, Client.error_id == Server.error_id).all()

q = session.execute(text("""with result1 as (select * from client cl
inner join server s
on cl.error_id = s.error_id)
select * from
result1 r
where r.player_id not in
(select ch.player_id from cheaters ch)""")).all()



'''
with result1 as (select * from client cl
inner join server s
on cl.error_id = s.error_id)
select * from
result1 r
where r.player_id not in
(select ch.player_id from cheaters ch
where DATEDIFF('day', result1.timestamp, to_timestamp(ch.ban_time, 'MM/DD/YYYY')) <= 1);
'''
print(q)