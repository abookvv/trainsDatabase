import psycopg2
import random
from faker import Faker

fake = Faker("ru_RU")
random.seed(42)

# Подключение к базе
conn = psycopg2.connect(
    host="postgrepro.dc-edu.ru",
    port=5432,
    dbname="dbstud",
    user="bk_465304_2025",
    password="bk_465304"
)
cur = conn.cursor()

# Хранение уникальных названий маршрутов
used_route_names = set()

NUM_ROUTES = 100
added = 0

while added < NUM_ROUTES:
    # Придумываем уникальное название маршрута (например, "Маршрут СПб-Выборг")
    start = fake.city()
    end = fake.city()
    if start == end:
        continue

    route_name = f"Маршрут {start} – {end}"
    if route_name in used_route_names:
        continue
    used_route_names.add(route_name)

    # Случайные параметры расписания
    weekday_only = random.choice([True, False])
    weekend_only = not weekday_only if random.random() < 0.8 else random.choice([True, False])  # чаще или-или

    try:
        cur.execute(
            "INSERT INTO routes (name, weekday_only, weekend_only) VALUES (%s, %s, %s);",
            (route_name, weekday_only, weekend_only)
        )
        conn.commit()
        added += 1
    except psycopg2.IntegrityError:
        conn.rollback()

print(f"✅ Добавлено маршрутов: {added}")
cur.close()
conn.close()
