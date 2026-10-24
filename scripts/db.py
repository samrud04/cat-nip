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
    con.close()

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

    cur.execute(
        f"SELECT * FROM {user_type} WHERE username = %s AND password = %s",
        (username, password)
    )

    result = cur.fetchone()

    con.close()

    return result is not None
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
def update_product(product_id, name, price, brand, category, stock):
    con, cur = connect()

    cur.execute(
        """
        UPDATE products
        SET name = %s,
            price = %s,
            brand = %s,
            category = %s,
            stock = %s
        WHERE id = %s
        """,
        (name, price, brand, category, stock, product_id)
    )

    con.commit()
    con.close()
# =====================================================
# USER CART FUNCTIONS
# =====================================================

def get_cart(user_id):

    con, cur = connect()

    cur.execute(
        """
        SELECT
            cart.product_id,
            cart.quantity,
            products.name,
            products.price,
            products.stock
        FROM cart
        JOIN products
        ON cart.product_id = products.id
        WHERE cart.user_id = %s
        """,
        (user_id,)
    )

    cart_items = cur.fetchall()

    con.close()

    return cart_items


def add_to_cart(user_id, product_id):

    con, cur = connect()

    # Check if product already exists in this user's cart
    cur.execute(
        """
        SELECT quantity
        FROM cart
        WHERE user_id = %s
        AND product_id = %s
        """,
        (user_id, product_id)
    )

    result = cur.fetchone()


    if result:

        # Increase quantity
        cur.execute(
            """
            UPDATE cart
            SET quantity = quantity + 1
            WHERE user_id = %s
            AND product_id = %s
            """,
            (user_id, product_id)
        )

    else:

        # Add new product to cart
        cur.execute(
            """
            INSERT INTO cart
            (user_id, product_id, quantity)
            VALUES (%s, %s, 1)
            """,
            (user_id, product_id)
        )


    con.commit()

    con.close()


def remove_from_cart(user_id, product_id):

    con, cur = connect()

    cur.execute(
        """
        SELECT quantity
        FROM cart
        WHERE user_id = %s
        AND product_id = %s
        """,
        (user_id, product_id)
    )

    result = cur.fetchone()


    if not result:

        con.close()
        return


    quantity = result[0]


    if quantity > 1:

        cur.execute(
            """
            UPDATE cart
            SET quantity = quantity - 1
            WHERE user_id = %s
            AND product_id = %s
            """,
            (user_id, product_id)
        )

    else:

        # Remove product if quantity becomes 0
        cur.execute(
            """
            DELETE FROM cart
            WHERE user_id = %s
            AND product_id = %s
            """,
            (user_id, product_id)
        )


    con.commit()

    con.close()


def clear_cart(user_id):

    con, cur = connect()

    cur.execute(
        """
        DELETE FROM cart
        WHERE user_id = %s
        """,
        (user_id,)
    )

    con.commit()

    con.close()
def get_user(user_id):

    con, cur = connect()

    cur.execute(
        """
        SELECT id, username, email, phone, address, gender, dob
        FROM user
        WHERE id = %s
        """,
        (user_id,)
    )

    user_data = cur.fetchone()

    con.close()

    return user_data


def get_current_user_id():

    try:
        with open("session.txt", "r") as f:
            return int(f.read().strip())

    except:
        return None
def create_order(user_id, total):

    con, cur = connect()

    cur.execute(
        """
        INSERT INTO orders (user_id, total)
        VALUES (%s, %s)
        """,
        (user_id, total)
    )

    order_id = cur.lastrowid

    con.commit()
    con.close()

    return order_id


def add_order_item(order_id, product_id, quantity, price):

    con, cur = connect()

    cur.execute(
        """
        INSERT INTO order_items
        (order_id, product_id, quantity, price)
        VALUES (%s, %s, %s, %s)
        """,
        (
            order_id,
            product_id,
            quantity,
            price
        )
    )

    con.commit()
    con.close()


def checkout(user_id):

    con, cur = connect()

    try:

        # Get cart items with current stock
        cur.execute(
            """
            SELECT
                cart.product_id,
                cart.quantity,
                products.price,
                products.stock
            FROM cart
            JOIN products
            ON cart.product_id = products.id
            WHERE cart.user_id = %s
            """,
            (user_id,)
        )

        cart_items = cur.fetchall()


        # Check if cart is empty
        if not cart_items:

            con.close()
            return False


        total = 0


        # Check stock and calculate total
        for item in cart_items:

            product_id = item[0]
            quantity = item[1]
            price = float(item[2])
            stock = int(item[3])


            # Prevent buying more than available stock
            if quantity > stock:

                con.close()
                return False


            total += quantity * price


        # Create order
        cur.execute(
            """
            INSERT INTO orders (user_id, total)
            VALUES (%s, %s)
            """,
            (user_id, total)
        )

        order_id = cur.lastrowid


        # Add order items and reduce stock
        for item in cart_items:

            product_id = item[0]
            quantity = item[1]
            price = float(item[2])


            # Add item to order history
            cur.execute(
                """
                INSERT INTO order_items
                (order_id, product_id, quantity, price)
                VALUES (%s, %s, %s, %s)
                """,
                (
                    order_id,
                    product_id,
                    quantity,
                    price
                )
            )


            # Reduce product stock
            cur.execute(
                """
                UPDATE products
                SET stock = stock - %s
                WHERE id = %s
                """,
                (
                    quantity,
                    product_id
                )
            )


        # Clear cart
        cur.execute(
            """
            DELETE FROM cart
            WHERE user_id = %s
            """,
            (user_id,)
        )


        # Save everything
        con.commit()

        con.close()

        # Return the new order ID so the UI can generate its bill.
        return order_id


    except Exception as e:

        print("Checkout Error:", e)

        con.rollback()

        con.close()

        return False
def create_booking(user_id, service_name, pet_name, booking_date, notes=""):
    try:
        conn, cursor = connect()

        cursor.execute("""
            INSERT INTO bookings (user_id, service_name, pet_name, booking_date, notes)
            VALUES (%s, %s, %s, %s, %s)
        """, (user_id, service_name, pet_name, booking_date, notes))

        conn.commit()
        cursor.close()
        conn.close()
        return True
    except Exception as e:
        print("Booking error:", e)
        return False
def get_user_bookings(user_id):
    try:
        conn, cursor = connect()

        cursor.execute("""
            SELECT id, service_name, pet_name, booking_date, notes, status, created_at
            FROM bookings
            WHERE user_id = %s
            ORDER BY created_at DESC
        """, (user_id,))

        results = cursor.fetchall()
        cursor.close()
        conn.close()
        return results
    except Exception as e:
        print("Error fetching bookings:", e)
        return []
def reduce_stock(product_id, quantity):

    con, cur = connect()

    cur.execute(
        """
        UPDATE products
        SET stock = stock - %s
        WHERE id = %s
        AND stock >= %s
        """,
        (quantity, product_id, quantity)
    )

    con.commit()

    success = cur.rowcount > 0

    con.close()

    return success

def get_user_orders(user_id):
    """Return the signed-in user's orders, newest first, with item counts."""
    con, cur = connect()
    try:
        cur.execute(
            """
            SELECT o.id, o.total, o.order_date, o.status,
                   (SELECT COUNT(*) FROM order_items oi WHERE oi.order_id = o.id) AS item_count
            FROM orders o
            WHERE o.user_id = %s
            ORDER BY o.order_date DESC, o.id DESC
            """,
            (user_id,)
        )
        return cur.fetchall()
    finally:
        cur.close()
        con.close()


def get_order_invoice_data(order_id, user_id):
    """Return an order, its customer details, and line items for that user.

    LEFT JOIN keeps historical order lines visible even if a product was later
    deleted from the catalogue.
    """
    con, cur = connect()
    try:
        cur.execute(
            """
            SELECT o.id, o.total, o.order_date, o.status,
                   u.username, u.email, u.phone, u.address
            FROM orders o
            JOIN `user` u ON u.id = o.user_id
            WHERE o.id = %s AND o.user_id = %s
            """,
            (order_id, user_id)
        )
        order = cur.fetchone()
        if order is None:
            return None

        cur.execute(
            """
            SELECT oi.product_id,
                   COALESCE(p.name, CONCAT('Product #', oi.product_id)),
                   oi.quantity, oi.price
            FROM order_items oi
            LEFT JOIN products p ON p.id = oi.product_id
            WHERE oi.order_id = %s
            ORDER BY oi.id
            """,
            (order_id,)
        )
        items = cur.fetchall()
        return {"order": order, "items": items}
    finally:
        cur.close()
        con.close()


def get_all_orders():
    """Return all customer orders for the admin order-management screen."""
    con, cur = connect()
    try:
        cur.execute(
            """
            SELECT o.id, u.username, o.order_date, o.total, o.status,
                   (SELECT COUNT(*) FROM order_items oi WHERE oi.order_id = o.id) AS item_count
            FROM orders o
            LEFT JOIN `user` u ON u.id = o.user_id
            ORDER BY o.order_date DESC, o.id DESC
            """
        )
        return cur.fetchall()
    finally:
        cur.close()
        con.close()


def get_admin_order_details(order_id):
    """Return customer/order information and line items for an admin."""
    con, cur = connect()
    try:
        cur.execute(
            """
            SELECT o.id, o.user_id, u.username, u.email, u.phone, u.address,
                   o.total, o.order_date, o.status
            FROM orders o
            LEFT JOIN `user` u ON u.id = o.user_id
            WHERE o.id = %s
            """,
            (order_id,)
        )
        order = cur.fetchone()
        if order is None:
            return None

        cur.execute(
            """
            SELECT oi.product_id,
                   COALESCE(p.name, CONCAT('Product #', oi.product_id)),
                   oi.quantity, oi.price
            FROM order_items oi
            LEFT JOIN products p ON p.id = oi.product_id
            WHERE oi.order_id = %s
            ORDER BY oi.id
            """,
            (order_id,)
        )
        return {"order": order, "items": cur.fetchall()}
    finally:
        cur.close()
        con.close()


def update_order_status(order_id, status):
    """Update an order's tracking status."""
    allowed_statuses = {"Placed", "Processing", "Shipped", "Delivered", "Cancelled"}
    if status not in allowed_statuses:
        raise ValueError("Invalid order status")

    con, cur = connect()
    try:
        cur.execute(
            "UPDATE orders SET status = %s WHERE id = %s",
            (status, order_id)
        )
        con.commit()
        return cur.rowcount > 0
    finally:
        cur.close()
        con.close()



def get_all_bookings():
    """Return all service bookings with customer names for the admin screen."""
    con, cur = connect()
    try:
        cur.execute(
            """
            SELECT b.id, u.username, b.service_name, b.pet_name,
                   b.booking_date, b.status, b.created_at
            FROM bookings b
            LEFT JOIN `user` u ON u.id = b.user_id
            ORDER BY b.created_at DESC, b.id DESC
            """
        )
        return cur.fetchall()
    finally:
        cur.close()
        con.close()


def get_admin_booking_details(booking_id):
    """Return booking details and the customer's contact information."""
    con, cur = connect()
    try:
        cur.execute(
            """
            SELECT b.id, b.user_id, u.username, u.email, u.phone,
                   b.service_name, b.pet_name, b.booking_date, b.notes,
                   b.status, b.created_at
            FROM bookings b
            LEFT JOIN `user` u ON u.id = b.user_id
            WHERE b.id = %s
            """,
            (booking_id,)
        )
        return cur.fetchone()
    finally:
        cur.close()
        con.close()


def update_booking_status(booking_id, status):
    """Update the status of a service booking."""
    allowed_statuses = {"Pending", "Confirmed", "In Progress", "Completed", "Cancelled"}
    if status not in allowed_statuses:
        raise ValueError("Invalid booking status")

    con, cur = connect()
    try:
        cur.execute(
            "UPDATE bookings SET status = %s WHERE id = %s",
            (status, booking_id)
        )
        con.commit()
        return cur.rowcount > 0
    finally:
        cur.close()
        con.close()
