from sqlalchemy import create_engine, MetaData, Table, Column, \
                         Integer, String, Text, Date, TIMESTAMP
from sqlalchemy.sql import select, join, text
from sqlalchemy.engine.url import URL
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from config import DATABASE, client_file, server_file, cheaters_db, SQL_QUERY

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
    """Таблица итоговых результатов по заданным запросам"""
    __tablename__ = 'result'

    timestamp = Column(TIMESTAMP)
    player_id = Column(Integer, primary_key=True)
    event_id = Column(String)
    error_id = Column(String)
    json_server = Column(Text)
    json_client = Column(Text)


class Client(Base):
    """
    Таблица Client
    """
    __tablename__ = 'client'

    # id = Column(Integer, primary_key=True)
    timestamp = Column('timestamp', TIMESTAMP(timezone=False))
    player_id = Column(Integer)
    error_id = Column(String, primary_key=True)
    json = Column(Text)


class Server(Base):
    """
    Таблица Server
    """
    __tablename__ = 'server'

    # id = Column(Integer, primary_key=True)
    timestamp = Column('timestamp', TIMESTAMP(timezone=False))
    event_id = Column(String)
    error_id = Column(String, primary_key=True)
    json = Column(Text)


class Cheaters(Base):
    """
    Таблица Cheaters
    """
    __tablename__ = 'cheaters'

    player_id = Column(Integer, primary_key=True)
    ban_time = Column(String)


def csv_to_sql(file_name, table_name):
    """
    Обработка csv файла и запись в нужную таблицу из БД
    """
    df = pd.read_csv(file_name)
    df.to_sql(con=engine, name=table_name, if_exists='append')


def table_into_db(db_name, table_name):
    """
    Обработка db файла и запись в нужную таблицу из БД
    """
    cnx = create_engine(f'sqlite:///{db_name}')
    df = pd.read_sql_table(db_name.split('.')[0], cnx)
    df.to_sql(con=engine, name=table_name, if_exists='append')


def main():
    """
    Главная точка входа в скрипт и запуск всего
    """
    csv_to_sql(server_file, 'server')
    csv_to_sql(client_file, 'client')
    table_into_db(cheaters_db, 'cheaters')

    # SQL запрос для поиска данных из 3 таблиц
    q = session.execute(text(SQL_QUERY)).all()

    # в цикле все записываем в таблицу result
    for line in q:
        print(line)
        timestamp, player_id, event_id, error_id, json_server, json_client = line
        row = Result(timestamp=timestamp, player_id=player_id,
                     event_id=event_id, error_id=error_id,
                     json_server=json_server, json_client=json_client)

        session.add(row)
        session.commit()


if __name__ == '__main__':
    main()
