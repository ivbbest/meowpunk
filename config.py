# Конфигурационные данные в одном месте

DATABASE = {
    'drivername': 'postgresql',
    'host': 'localhost',
    'port': '5432',
    'username': 'admin',
    'password': '1234',
    'database': 'meowpunk_db'
}

client_file = 'client.csv'
server_file = 'server.csv'
cheaters_db = 'cheaters.db'

"""
SQL запрос, который решает следующую задачу

1) Выгрузит данные из client.csv и server.scv за определенную дату.
2) Объединит данные из этих таблиц по error_id.
3) Исключит из выборки записи с player_id, которые есть в таблице  cheaters,
   но только в том случае если:
   у player_id ban_time - это предыдущие сутки или раньше относительно timestamp из server.scv
4) Выгрузит данные в таблицу, созданную в задаче 1. В ней должны бать следующие данные:
"""
SQL_QUERY = """SELECT s."timestamp", c.player_id, s.event_id, 
                    c.error_id, s."description", c."description"
               FROM client AS c
               INNER JOIN server AS s
               ON c.error_id = s.error_id
               WHERE c.player_id NOT IN
               (SELECT player_id
                FROM cheaters AS t
                WHERE CAST(t.ban_time AS timestamp) < c."timestamp" - interval '1 day'
                                            )"""