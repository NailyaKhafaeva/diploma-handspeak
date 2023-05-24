import psycopg2

# Параметры подключения к базе данных
conn = psycopg2.connect(
    dbname="database_name",
    user="postgres",
    password="password",
    host="localhost",
    port="5432"
)

cur = conn.cursor()

# Данные для заполнения таблицы lessons
lessons_data = [
    {"name": "Урок 1", "description": "Описание урока 1", "level_id": 1},
    {"name": "Урок 2", "description": "Описание урока 2", "level_id": 1},
    {"name": "Урок 3", "description": "Описание урока 3", "level_id": 2},
    {"name": "Урок 4", "description": "Описание урока 4", "level_id": 2},
    {"name": "Урок 5", "description": "Описание урока 5", "level_id": 3},
    {"name": "Урок 6", "description": "Описание урока 6", "level_id": 3},
]

# Вставляем данные в таблицу lessons
for lesson in lessons_data:
    cur.execute("""
        INSERT INTO lessons (name, description, level_id)
        VALUES (%s, %s, %s)""",
        (lesson["name"], lesson["description"], lesson["level_id"])
    )

conn.commit()  # Фиксируем изменения

# Закрываем соединение с базой данных
cur.close()
conn.close()