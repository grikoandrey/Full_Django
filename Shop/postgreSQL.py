import psycopg2

conn = psycopg2.connect('dbname=postgres user=postgres',
                        # password="......",
                        # host="/var/run/postgresql/",
                        # port="5432"
                        )

cur = conn.cursor()

# cur.execute("CREATE TABLE test (id serial PRIMARY KEY, num integer, data varchar);")

cur.execute("INSERT INTO test (num, data) VALUES (%s, %s)", (200, "opr'stu"))

cur.execute("SELECT * FROM test;")

print(cur.fetchall())

conn.commit()  # Завершить транзакцию
cur.close()  # Закрыть курсор
conn.close()  # Закрыть подключение
