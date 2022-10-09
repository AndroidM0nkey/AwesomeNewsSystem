import psycopg2

conn = psycopg2.connect(dbname='db', user='postgres', 
                password='postgres', host='localhost')
cur = conn.cursor()

query = '''SELECT * FROM newsdata'''
cur.execute(query)
for row in cur.fetchall():
    print(row)
print("ENDS")