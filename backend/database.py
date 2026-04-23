import mysql.connector as sql
import random


con = sql.connect(
    host="localhost",
    user="root",
    password="admin",
    database="catnip"
)
cur = con.cursor()
l=[]

def add_food(name, qty=20, price=0, type=None):
    Global l
    while True:
        f_id = random.randint(1000, 9999)
        if f_id not in l:
            l.append(f_id)
            cur.execute("insert into food (f_id, name, quantity, price, type) values (%s, %s, %s, %s, %s)", (f_id, name, qty, price,type))
            con.commit()
            break
    

def delete_food(f_id):
    cur.execute("delete from food where f_id = %s", (f_id,))
    con.commit()

def update_food(f_id, name=None, qty=None, price=None, type=None):
    if name:
        cur.execute("update food set name = %s where f_id = %s", (name, f_id))
    if qty:
        cur.execute("update food set quantity = %s where f_id = %s", (qty, f_id))
    if price:
        cur.execute("update food set price = %s where f_id = %s", (price, f_id))
    if type:
        cur.execute("update food set type = %s where f_id = %s", (type, f_id))
    con.commit()

def get_food(f_id=None):
    if f_id:
        cur.execute("select * from food where f_id = %s", (f_id,))
        return cur.fetchone()
    else:
        cur.execute("select * from food")
        return cur.fetchall()

con.close()