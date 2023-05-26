import psycopg2
from config import host, user, password, db_name

try:
    connection = psycopg2.connect(
        host=host,
        user=user,
        password=password,
        database=db_name
    )
    connection.autocommit = True

    with connection.cursor() as cursor:
        cursor.execute(
            "SELECT version();"
        )

        print(f"Server version: {cursor.fetchone()}")

    # создание таблицы user
    with connection.cursor() as cursor:
        cursor.execute(
            """CREATE TABLE users(
                id SERIAL PRIMARY KEY,
                email VARCHAR(100) UNIQUE NOT NULL,
                password VARCHAR(100) NOT NULL,
                name VARCHAR(100) NOT NULL);"""
        )

        print("[INFO] Table created successfully")

    # создание таблицы levels
    with connection.cursor() as cursor:
        cursor.execute(
            """CREATE TABLE levels(
                id SERIAL PRIMARY KEY,
                name VARCHAR(100) not null NOT NULL,
                description VARCHAR(200) NOT NULL);"""
        )

        print("[INFO] Table created successfully")

    # создание таблицы lessons
    with connection.cursor() as cursor:
        cursor.execute(
            """CREATE TABLE lessons(
                id SERIAL PRIMARY KEY,
                name VARCHAR(100) NOT NULL ,
                description VARCHAR(200) NOT NULL ,
                level_id INTEGER REFERENCES levels(id) NOT NULL,
                content TEXT);"""
        )

        print("[INFO] Table created successfully")

    # создание таблицы progress
    with connection.cursor() as cursor:
        cursor.execute(
            """CREATE TABLE progress(
                id SERIAL PRIMARY KEY,
                user_id INTEGER REFERENCES users(id) NOT NULL,
                lesson_id INTEGER REFERENCES lessons(id) NOT NULL,
                value INTEGER NOT NULL,
                last_gesture INTEGER NOT NULL);"""
        )

        print("[INFO] Table created successfully")

    # вставка данных в levels
    with connection.cursor() as cursor:
        cursor.execute(
            """INSERT INTO levels (id, name, description) VALUES
            (1, 'Уровень 1', 'Цифры'),
            (2, 'Уровень 2', 'Алфавит');"""
        )

        print("[INFO] Data was succefully inserted")

    #вставка данных в lessons
    with connection.cursor() as cursor:
        cursor.execute(
            """INSERT INTO lessons (id, name, description, level_id, content) VALUES
            (1, 'Урок 1', 'Цифры от 0 до 4', 1, 'В данном уроке будут рассмотрены цифры от 0 до 4.
                Ноль - показывают ладонью вверх и прижимают к ладони другой руки. Этот жест символизирует пустоту или отсутствие чего-либо.
                Один - показывают указательный палец.
                Три - показывают три поднятых пальца (указательный, средний и большой).
                Четыре - показывают четыре поднятых пальца (все, кроме большого).'),
            (2, 'Урок 2', 'Цифры от 5 до 9', 1, 'В данном уроке будут рассмотрены цифры от 5 до 9.
                Пять - показывают ладонью вверх, раскрыв все пальцы.
                Шесть - показывают указательный, средний и безымянный пальцы. Остальные сжимают.
                Семь - показывают три поднятых пальца (указательный, средний и мизинец).
                Восемь - показывают три поднятых пальца (указательный, безымянный и мизинец).
                Девять - показывают три поднятых пальцы (средний, безымянный и мизинец).'),
            (3, 'Урок 1', 'Буквы: А, В, Г, Е, Ж', 2, 'В данном уроке будут рассмотрены буквы А, В, Г, Е, Ж.
                Для буквы А необходимо боком показать сжатый кулак.
                Для буквы В необходимо показать раскрытую ладонь.
                Для буквы Г необходимо вытянуть большой и указательный пальцы формой L и направить вниз указательным пальцем.
                Для буквы Е необходимо сжать пальцы, чтобы между ними оставался небольшой круг.
                Для буквы Ж необходимо свести все пальцы кроме большого, а большим коснуться среднего.'),
            (4, 'Урок 2', 'Буквы: И, Л, М, Н, О', 2, 'В данном уроке будут рассмотрены буквы И, Л, М, Н, О.
                Для буквы И нужно сложить указательный и средний пальцы, остальные пальцы разжать.
                Буква Л образуется при сведении среднего и указательного пальцев, а остальные пальцы разжимаются.
                Буква М образуется при сведении среднего, безымянного и указательного пальцев, а остальные пальцы разжимаются.
                Буква Н образуется при сведении безымянного пальца, а затем прикладывании к нему большого, остальные пальцы разжимаются.
                Буква О образуется при сведении указательного и большого пальцев.'),
            (5, 'Урок 3', 'Буквы П, Р, С, Т, У', 2, 'В данном уроке будут рассмотрены буквы П, Р, С, Т, У.
                Для буквы П необходимо свести указательный и средний пальцы, остальные сжать.
                Для буквы Р необходимо свести средний и большой пальцы, а остальные пальцы оставить раскрытыми.
                Для буквы С необходимо всести все пальцы в округленной форме.Для буквы Т необходимо свести указательный, средний и безымянный пальцы.
                Для буквы У  необходимо вытянуть мизинец и указательный палец, остальные пальцы сжать в кулак.'),
            (6, 'Урок 4', 'Буквы Ф, Х, Ч, Ш, Ы', 2, 'В данном уроке будут рассмотрены буквы Ф, Х, Ч, Ш, Ы.
                Для буквы Ф необходимо свести все пальцы кроме большого в округленную форму, а большой палец приложить к указательному.
                Для буквы Х необходимо округлить указательный палец, а большой палец зажать в кулак остальными пальцами.
                Для буквы Ч необходимо согнуть указательный палец, который находится на уровне большого пальца, а остальные пальцы согнуты в кулак.
                Для буквы Ш необходимо вытянуть указательный, средний и безымянный пальцы.
                Для буквы Ы необходимо сжать средный, безымянный и большой пальцы, остальные вытянуть.'),
            (7, 'Урок 5', 'Буквы Э, Ю, Я', 2, 'В данном уроке будут рассмотрены буквы Э, Ю, Я.
                Для буквы Э необходимо округлить указательный и большой пальцы, остальные сжать в кулак.
                Для буквы Ю необходимо вытянуть мизинец, остальные пальцы сжать в кулак.
                Для буквы Я необходимо вытянуть указательный и средний пальцы, средний положить на указательный, а остальные пальцы сжать в кулак.');"""
        )

        print("[INFO] Data was succefully inserted")


except Exception as _ex:
    print("[INFO] Error while working with PostgreSQL", _ex)
finally:
    if connection:
        # cursor.close()
        connection.close()
        print("[INFO] PostgreSQL connection closed")