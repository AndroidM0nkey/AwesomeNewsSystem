import psycopg2

try:
    conn = psycopg2.connect(dbname='db', user='postgres', 
                    password='postgres', host='localhost')
    cur = conn.cursor()

    create_table_query = '''CREATE TABLE newsdata
                            (TIMESTAMP INT NOT NULL,
                            TITLE           TEXT NOT NULL,
                            BODY            TEXT NOT NULL,
                            ID              TEXT PRIMARY KEY NOT NULL,
                            ML              bytea NOT NULL); '''

    cur.execute(create_table_query)
    conn.commit()
except:
    print("Tables already exist")
print("Finished creatings tables")
