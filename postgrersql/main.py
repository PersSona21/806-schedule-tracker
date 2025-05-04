import psycopg2

conn = psycopg2.connect(dbname='database', user='db_user', password='mypassword', host='localhost')
cursor = conn.cursor()

cursor.execute("SELECT * FROM airport LIMIT 10")
records = cursor.fetchall()


cursor.close()
conn.close()