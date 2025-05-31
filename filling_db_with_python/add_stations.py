import random
from faker import Faker
import psycopg2

fake = Faker("ru_RU")
random.seed(42)

conn = psycopg2.connect(
    host="postgrepro.dc-edu.ru",
    port=5432,
    dbname="dbstud",
    user="bk_465304_2025",
    password="bk_465304"
)

cur = conn.cursor()

# Получаем существующие коды из базы, чтобы не дублировать
cur.execute("SELECT code FROM stations;")
used_codes = set(code[0] for code in cur.fetchall())

NUM_STATIONS = 200
added = 0

while added < NUM_STATIONS:
    name = fake.city() + " станция"

    # Генерируем уникальный code
    while True:
        code = fake.lexify(text='???').upper()
        if code not in used_codes:
            used_codes.add(code)
            break

    # Получаем случайный vokzal_id
    cur.execute("SELECT vokzal_id FROM vokzals ORDER BY RANDOM() LIMIT 1;")
    vokzal_id = cur.fetchone()[0]

    try:
        cur.execute(
            "INSERT INTO stations (name, code, vokzal_id) VALUES (%s, %s, %s);",
            (name, code, vokzal_id)
        )
        added += 1
    except psycopg2.IntegrityError:
        conn.rollback()
    else:
        conn.commit()

cur.close()
conn.close()

print(f"✅ Успешно добавлено {added} уникальных станций!")
