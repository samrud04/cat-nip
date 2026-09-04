import mysql.connector as sql
import random

def connect():
    con = sql.connect(
        host="localhost",
        user="root",
        password="admin",
        database="catnip",
        auth_plugin="mysql_native_password"
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

def add_product(input_data):
    con, cur = connect()
    cur.execute("INSERT INTO products (name, price, brand, category, stock) VALUES (%s, %s, %s, %s, %s)", input_data)
    con.commit()

def get_products():
    con, cur = connect()

    cur.execute("""
        SELECT id, name, price, brand, category, stock
        FROM products
        ORDER BY id
    """)

    products = cur.fetchall()

    con.close()

    return products

def login(user_type, username, password):
    con, cur = connect()
    cur.execute(f"SELECT * FROM {user_type} WHERE username = %s AND password = %s", (username, password))
    if cur.fetchone() is not None:
        return True
    return False

def register(username, password, email, phone, address, gender, dob):
    con, cur = connect()
    cur.execute("SELECT * FROM user WHERE username = %s", (username,))
    if cur.fetchone() is not None:
        return False
    add_data("user", (username, password, email, phone, address, gender, dob))
    return True

def get_user_id(username):
    """Get user_id from username"""
    con, cur = connect()
    cur.execute("SELECT id FROM user WHERE username = %s", (username,))
    result = cur.fetchone()
    con.close()
    return result[0] if result else None

def delete_product(product_id):
    con, cur = connect()

    cur.execute(
        "DELETE FROM products WHERE id = %s",
        (product_id,)
    )

    con.commit()
    con.close()


def update_stock(product_id, new_stock):
    con, cur = connect()

    cur.execute(
        "UPDATE products SET stock = %s WHERE id = %s",
        (new_stock, product_id)
    )

    con.commit()
    con.close()


def get_product(product_id):
    con, cur = connect()

    cur.execute(
        "SELECT * FROM products WHERE id = %s",
        (product_id,)
    )

    product = cur.fetchone()

    con.close()

    return product