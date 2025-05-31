import psycopg2
import random
from datetime import datetime, timedelta, time

# Подключение к базе
conn = psycopg2.connect(
    host="postgrepro.dc-edu.ru",
    port=5432,
    dbname="dbstud",
    user="bk_465304_2025",
    password="bk_465304"
)
cur = conn.cursor()

# Получим все ID маршрутов и станций
cur.execute("SELECT route_id FROM routes;")
routes = [r[0] for r in cur.fetchall()]

cur.execute("SELECT station_id FROM stations;")
stations = [s[0] for s in cur.fetchall()]

print(f"Маршрутов найдено: {len(routes)}")
print(f"Станций найдено: {len(stations)}")

def random_time(start_hour=5, end_hour=23):
    hour = random.randint(start_hour, end_hour - 1)
    minute = random.choice(range(0, 60, 5))
    return time(hour, minute)

added = 0

for route_id in routes:
    stop_stations = random.sample(stations, k=random.randint(5, 10))
    current_time = timedelta(hours=random.randint(5, 9))  # стартовое время между 5 и 9 утра

    for order, station_id in enumerate(stop_stations, start=1):
        arrival = (datetime.min + current_time).time()
        departure = (datetime.min + current_time + timedelta(minutes=random.randint(2, 5))).time()

        try:
            cur.execute("""
                INSERT INTO route_stations (route_id, station_id, station_order, arrival_time, departure_time)
                VALUES (%s, %s, %s, %s, %s);
            """, (route_id, station_id, order, arrival, departure))
            conn.commit()
            added += 1
        except psycopg2.IntegrityError as e:
            print(f"⚠️ Ошибка при вставке: {e}")
            conn.rollback()

        current_time += timedelta(minutes=random.randint(15, 45))  # переход к следующей станции

print(f"✅ Добавлено {added} остановок по маршрутам.")
cur.close()
conn.close()
