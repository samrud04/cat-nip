import mysql.connector as sql
import random

def connect():
    con = sql.connect(
        host="localhost",
        user="root",
        password="admin",
        database="catnip"
    )
    cur = con.cursor()
    return con, cur


def add_data(table, input_data):
    con, cur = connect()
    # generate a random id
    while True:
        new_id = random.randint(1000000, 9999999)
        cur.execute(f"SELECT * FROM {table} WHERE id = {new_id}")
        if cur.fetchone() is None:
            break

    # add input to database with that id
    input_data = (new_id, ) + input_data
    placeholders = ", ".join(["%s"] * len(input_data))
    query = f"INSERT INTO {table} VALUES ({placeholders})"
    cur.execute(query, input_data)
    con.commit()

def login(username, password):
    con, cur = connect()
    cur.execute("SELECT * FROM login_det WHERE username = %s AND password = %s", (username, password))
    if cur.fetchone() is not None:
        return True
    return False




