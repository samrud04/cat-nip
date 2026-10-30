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
    
    con = None
    cur = None
    try:
        con, cur = connect()

        # Check the username while using the same connection as the insert.
        cur.execute("SELECT id FROM user WHERE username = %s", (username,))
        if cur.fetchone() is not None:
            return False

        cur.execute(
            """
            INSERT INTO user
                (username, password, email, phone, address, gender, dob)
            VALUES (%s, %s, %s, %s, %s, %s, %s)
            """,
            (username, password, email, phone, address, gender, dob)
        )
        con.commit()
        return True
    except Exception:
        if con is not None:
            con.rollback()
        raise
    finally:
        if cur is not None:
            cur.close()
        if con is not None and con.is_connected():
            con.close()

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


# =====================================================
# PET ADOPTION (demo shelter listings + applications)
# =====================================================

def ensure_adoption_tables():
    """Create adoption tables on first use; leaves existing app data untouched."""
    con, cur = connect()
    try:
        cur.execute("""
            CREATE TABLE IF NOT EXISTS pets (
                id INT AUTO_INCREMENT PRIMARY KEY,
                name VARCHAR(100) NOT NULL,
                species VARCHAR(40) NOT NULL,
                age VARCHAR(40) NOT NULL,
                gender VARCHAR(20) NOT NULL,
                description VARCHAR(500) NOT NULL,
                emoji VARCHAR(32) NOT NULL DEFAULT 'paw',
                status VARCHAR(30) NOT NULL DEFAULT 'Available',
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            ) ENGINE=InnoDB
        """)
        cur.execute("""
            CREATE TABLE IF NOT EXISTS adoption_applications (
                id INT AUTO_INCREMENT PRIMARY KEY,
                pet_id INT NOT NULL,
                user_id INT NOT NULL,
                reason VARCHAR(1000) NOT NULL,
                status VARCHAR(30) NOT NULL DEFAULT 'Pending',
                collection_address VARCHAR(255) NULL,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                CONSTRAINT fk_adoption_pet FOREIGN KEY (pet_id) REFERENCES pets(id),
                CONSTRAINT fk_adoption_user FOREIGN KEY (user_id) REFERENCES `user`(id),
                UNIQUE KEY uq_user_pet_application (user_id, pet_id)
            ) ENGINE=InnoDB
        """)
        # Upgrade existing installations safely without dropping application data.
        cur.execute("SHOW COLUMNS FROM adoption_applications LIKE 'collection_address'")
        if not cur.fetchone():
            cur.execute("ALTER TABLE adoption_applications ADD COLUMN collection_address VARCHAR(255) NULL AFTER status")
        cur.execute("SELECT COUNT(*) FROM pets")
        if cur.fetchone()[0] == 0:
            demo_pets = [
                ('Milo', 'Cat', '8 months', 'Male', 'A curious, playful kitten who loves toys and sunny windows.', 'cat'),
                ('Luna', 'Cat', '2 years', 'Female', 'A gentle, affectionate cat who enjoys quiet company.', 'cat'),
                ('Buddy', 'Dog', '1 year', 'Male', 'A cheerful, energetic dog who loves walks and learning tricks.', 'dog'),
                ('Daisy', 'Dog', '3 years', 'Female', 'A friendly, calm companion who would love a caring home.', 'dog'),
                ('Peanut', 'Rabbit', '6 months', 'Female', 'A soft-natured bunny who enjoys fresh greens and a calm space.', 'rabbit'),
                ('Oreo', 'Cat', '1 year', 'Male', 'A sociable cat with a big personality and lots of curiosity.', 'paw'),
            ]
            cur.executemany(
                "INSERT INTO pets (name, species, age, gender, description, emoji) VALUES (%s,%s,%s,%s,%s,%s)",
                demo_pets
            )
        con.commit()
    finally:
        cur.close()
        con.close()

def get_available_pets(species='All'):
    ensure_adoption_tables()
    con, cur = connect()
    try:
        if species and species != 'All':
            cur.execute("SELECT id, name, species, age, gender, description, emoji, status FROM pets WHERE status='Available' AND species=%s ORDER BY id", (species,))
        else:
            cur.execute("SELECT id, name, species, age, gender, description, emoji, status FROM pets WHERE status='Available' ORDER BY id")
        return cur.fetchall()
    finally:
        cur.close(); con.close()

def submit_adoption_application(user_id, pet_id, reason):
    ensure_adoption_tables()
    con, cur = connect()
    try:
        cur.execute("SELECT status FROM pets WHERE id=%s", (pet_id,))
        pet = cur.fetchone()
        if not pet or pet[0] != 'Available':
            return 'unavailable'
        cur.execute("SELECT id FROM adoption_applications WHERE user_id=%s AND pet_id=%s", (user_id, pet_id))
        if cur.fetchone():
            return 'exists'
        cur.execute("INSERT INTO adoption_applications (pet_id, user_id, reason) VALUES (%s,%s,%s)", (pet_id, user_id, reason))
        con.commit()
        return 'submitted'
    finally:
        cur.close(); con.close()

def get_user_adoption_applications(user_id):
    ensure_adoption_tables()
    con, cur = connect()
    try:
        cur.execute("""SELECT a.id, p.name, p.species, a.status, a.created_at, a.reason, a.collection_address
                       FROM adoption_applications a JOIN pets p ON p.id=a.pet_id
                       WHERE a.user_id=%s ORDER BY a.created_at DESC, a.id DESC""", (user_id,))
        return cur.fetchall()
    finally:
        cur.close(); con.close()

def get_all_adoption_applications():
    ensure_adoption_tables()
    con, cur = connect()
    try:
        cur.execute("""SELECT a.id, p.name, p.species, u.username, u.email, u.phone, a.reason, a.status, a.created_at, a.pet_id, a.user_id
                       FROM adoption_applications a JOIN pets p ON p.id=a.pet_id
                       JOIN `user` u ON u.id=a.user_id ORDER BY a.created_at DESC, a.id DESC""")
        return cur.fetchall()
    finally:
        cur.close(); con.close()

def update_adoption_application(application_id, status):
    allowed = {'Pending', 'Approved', 'Rejected'}
    if status not in allowed:
        raise ValueError('Invalid adoption application status')
    ensure_adoption_tables()
    con, cur = connect()
    try:
        cur.execute("SELECT pet_id, user_id, status, collection_address FROM adoption_applications WHERE id=%s", (application_id,))
        app = cur.fetchone()
        if not app:
            return False
        pet_id, user_id, old_status, collection_address = app
        if status == 'Approved':
            cur.execute("SELECT status FROM pets WHERE id=%s FOR UPDATE", (pet_id,))
            pet = cur.fetchone()
            if not pet or (pet[0] != 'Available' and old_status != 'Approved'):
                con.rollback()
                return False
            cur.execute("UPDATE pets SET status='Adopted' WHERE id=%s", (pet_id,))
            cur.execute("UPDATE adoption_applications SET status='Rejected' WHERE pet_id=%s AND id<>%s AND status='Pending'", (pet_id, application_id))
            if not collection_address:
                import random
                # Fictional demonstration addresses only; not real collection centres.
                demo_addresses = [
                    'Demo Adoption Centre, 14 Coral Garden Road, Adyar, Chennai 600020',
                    'Cat Nip Collection Hub, 27 Mango Grove Avenue, Velachery, Chennai 600042',
                    'Demo Pet Welcome Centre, 8 Lakeview Cross Street, Anna Nagar, Chennai 600040',
                    'Cat Nip Adoption Point, 35 Jasmine Park Road, Thoraipakkam, Chennai 600097',
                    'Demo Animal Care Centre, 19 Banyan Lane, Mylapore, Chennai 600004',
                    'Cat Nip Pet Collection Desk, 6 Rainbow Nagar Main Road, Porur, Chennai 600116',
                ]
                collection_address = random.choice(demo_addresses)
        elif old_status == 'Approved':
            cur.execute("UPDATE pets SET status='Available' WHERE id=%s", (pet_id,))
        cur.execute("UPDATE adoption_applications SET status=%s, collection_address=%s WHERE id=%s", (status, collection_address, application_id))
        con.commit()
        return True
    finally:
        cur.close(); con.close()

# =====================================================
# PLAYDATES (admin-created events and automatic bookings)
# =====================================================

def ensure_playdate_tables():
    """Create playdate tables safely without touching existing Cat Nip data."""
    con, cur = connect()
    try:
        cur.execute("""
            CREATE TABLE IF NOT EXISTS playdate_events (
                id INT AUTO_INCREMENT PRIMARY KEY,
                title VARCHAR(120) NOT NULL,
                description VARCHAR(500) NULL,
                pet_type VARCHAR(30) NOT NULL DEFAULT 'All',
                event_date DATE NOT NULL,
                start_time TIME NOT NULL,
                end_time TIME NOT NULL,
                location VARCHAR(255) NOT NULL,
                capacity INT NOT NULL,
                allow_own_pets TINYINT(1) NOT NULL DEFAULT 0,
                allowed_pet_types VARCHAR(100) NOT NULL DEFAULT 'Dog,Cat,Rabbit',
                status VARCHAR(20) NOT NULL DEFAULT 'Open',
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            ) ENGINE=InnoDB
        """)
        cur.execute("""
            CREATE TABLE IF NOT EXISTS playdate_bookings (
                id INT AUTO_INCREMENT PRIMARY KEY,
                event_id INT NOT NULL,
                user_id INT NOT NULL,
                pet_name VARCHAR(100) NULL,
                pet_type VARCHAR(30) NULL,
                pets_details TEXT NULL,
                status VARCHAR(20) NOT NULL DEFAULT 'Confirmed',
                booked_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                CONSTRAINT fk_playdate_event FOREIGN KEY (event_id) REFERENCES playdate_events(id),
                CONSTRAINT fk_playdate_user FOREIGN KEY (user_id) REFERENCES `user`(id),
                UNIQUE KEY uq_playdate_user_event (event_id, user_id)
            ) ENGINE=InnoDB
        """)
        # Safe migration for installations created before multi-pet support.
        cur.execute("SHOW COLUMNS FROM playdate_bookings LIKE 'pets_details'")
        if not cur.fetchone():
            cur.execute("ALTER TABLE playdate_bookings ADD COLUMN pets_details TEXT NULL AFTER pet_type")
        con.commit()
    finally:
        cur.close(); con.close()


def create_playdate_event(title, description, pet_type, event_date, start_time, end_time,
                          location, capacity, allow_own_pets, allowed_pet_types):
    from datetime import date, time
    ensure_playdate_tables()
    title = str(title).strip()
    location = str(location).strip()
    if not title or not location:
        raise ValueError('Event title and location are required.')
    if int(capacity) < 1:
        raise ValueError('Capacity must be at least 1 participant.')
    d = date.fromisoformat(str(event_date).strip())
    start = time.fromisoformat(str(start_time).strip())
    end = time.fromisoformat(str(end_time).strip())
    if d < date.today():
        raise ValueError('Playdate must be today or in the future.')
    if end <= start:
        raise ValueError('End time must be later than start time.')
    con, cur = connect()
    try:
        cur.execute("""INSERT INTO playdate_events
            (title, description, pet_type, event_date, start_time, end_time, location,
             capacity, allow_own_pets, allowed_pet_types)
            VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)""",
            (title, str(description).strip(), pet_type, d, start, end, location,
             int(capacity), int(bool(allow_own_pets)), str(allowed_pet_types)))
        con.commit()
        return cur.lastrowid
    finally:
        cur.close(); con.close()


def get_playdate_events(include_past=False):
    ensure_playdate_tables()
    con, cur = connect()
    try:
        where = "" if include_past else "WHERE e.event_date >= CURDATE() AND e.status='Open'"
        cur.execute(f"""SELECT e.id, e.title, e.description, e.pet_type, e.event_date,
                    e.start_time, e.end_time, e.location, e.capacity, e.allow_own_pets,
                    e.allowed_pet_types, e.status,
                    (SELECT COUNT(*) FROM playdate_bookings b WHERE b.event_id=e.id AND b.status='Confirmed') AS booked
                    FROM playdate_events e {where} ORDER BY e.event_date, e.start_time, e.id""")
        return cur.fetchall()
    finally:
        cur.close(); con.close()


def get_user_playdate_bookings(user_id):
    ensure_playdate_tables()
    con, cur = connect()
    try:
        cur.execute("""SELECT b.id, e.id, e.title, e.event_date, e.start_time, e.end_time,
                    e.location, b.pet_name, b.pet_type, b.status, e.status, b.pets_details
                    FROM playdate_bookings b JOIN playdate_events e ON e.id=b.event_id
                    WHERE b.user_id=%s ORDER BY e.event_date DESC, e.start_time DESC, b.id DESC""", (user_id,))
        return cur.fetchall()
    finally:
        cur.close(); con.close()


def _playdate_datetime(day_value, time_value):
    from datetime import datetime, time, timedelta
    if isinstance(time_value, timedelta):
        seconds = int(time_value.total_seconds()) % 86400
        time_value = time(seconds // 3600, (seconds % 3600) // 60, seconds % 60)
    elif isinstance(time_value, str):
        time_value = time.fromisoformat(time_value)
    return datetime.combine(day_value, time_value)


def book_playdate(event_id, user_id, pet_name=None, pet_type=None, pets=None):
    from datetime import datetime
    import json
    ensure_playdate_tables()
    # Accept the older single-pet arguments as well as the new list of up to 3 pets.
    if pets is None:
        pets = ([{"name": str(pet_name).strip(), "type": str(pet_type).strip()}]
                if pet_name and pet_type else [])
    cleaned_pets = []
    for pet in pets:
        name = str(pet.get("name", "")).strip()
        ptype = str(pet.get("type", "")).strip()
        if not name or not ptype:
            raise ValueError("Enter both a name and type for every pet, or set the pet count to zero.")
        cleaned_pets.append({"name": name[:100], "type": ptype[:30]})
    if len(cleaned_pets) > 3:
        raise ValueError("You can register up to 3 pets for one playdate booking.")
    con, cur = connect()
    try:
        cur.execute("SELECT event_date, start_time, capacity, allow_own_pets, allowed_pet_types, status FROM playdate_events WHERE id=%s FOR UPDATE", (event_id,))
        event = cur.fetchone()
        if not event or event[5] != 'Open':
            return 'closed'
        event_date, start_time, capacity, allow_own, allowed_types, _ = event
        if _playdate_datetime(event_date, start_time) <= datetime.now():
            return 'started'
        cur.execute("SELECT id, status FROM playdate_bookings WHERE event_id=%s AND user_id=%s", (event_id, user_id))
        existing = cur.fetchone()
        if existing and existing[1] == 'Confirmed':
            return 'exists'
        if cleaned_pets:
            if not allow_own:
                return 'pets_not_allowed'
            permitted = [x.strip() for x in (allowed_types or '').split(',') if x.strip()]
            if any(pet["type"] not in permitted for pet in cleaned_pets):
                return 'pet_type_not_allowed'
        cur.execute("SELECT COUNT(*) FROM playdate_bookings WHERE event_id=%s AND status='Confirmed'", (event_id,))
        if cur.fetchone()[0] >= capacity:
            return 'full'
        first_pet = cleaned_pets[0] if cleaned_pets else None
        first_name = first_pet["name"] if first_pet else None
        first_type = first_pet["type"] if first_pet else None
        pets_json = json.dumps(cleaned_pets, ensure_ascii=True) if cleaned_pets else None
        if existing:
            cur.execute("UPDATE playdate_bookings SET pet_name=%s, pet_type=%s, pets_details=%s, status='Confirmed', booked_at=CURRENT_TIMESTAMP WHERE id=%s",
                        (first_name, first_type, pets_json, existing[0]))
        else:
            cur.execute("INSERT INTO playdate_bookings (event_id,user_id,pet_name,pet_type,pets_details) VALUES (%s,%s,%s,%s,%s)",
                        (event_id, user_id, first_name, first_type, pets_json))
        con.commit()
        return 'confirmed'
    finally:
        cur.close(); con.close()


def cancel_playdate_booking(booking_id, user_id):
    from datetime import datetime
    ensure_playdate_tables()
    con, cur = connect()
    try:
        cur.execute("""SELECT b.status, e.event_date, e.start_time FROM playdate_bookings b
                       JOIN playdate_events e ON e.id=b.event_id WHERE b.id=%s AND b.user_id=%s""", (booking_id, user_id))
        row = cur.fetchone()
        if not row or row[0] != 'Confirmed':
            return False
        if _playdate_datetime(row[1], row[2]) <= datetime.now():
            return False
        cur.execute("UPDATE playdate_bookings SET status='Cancelled' WHERE id=%s", (booking_id,))
        con.commit()
        return True
    finally:
        cur.close(); con.close()


def get_admin_playdate_bookings(event_id=None):
    ensure_playdate_tables()
    con, cur = connect()
    try:
        if event_id is None:
            cur.execute("""SELECT b.id, e.id, e.title, u.username, u.email, e.event_date, e.start_time,
                         b.pet_name, b.pet_type, b.status, b.pets_details FROM playdate_bookings b
                         JOIN playdate_events e ON e.id=b.event_id JOIN `user` u ON u.id=b.user_id
                         ORDER BY e.event_date DESC, b.id DESC""")
        else:
            cur.execute("""SELECT b.id, e.id, e.title, u.username, u.email, e.event_date, e.start_time,
                         b.pet_name, b.pet_type, b.status, b.pets_details FROM playdate_bookings b
                         JOIN playdate_events e ON e.id=b.event_id JOIN `user` u ON u.id=b.user_id
                         WHERE e.id=%s ORDER BY b.id""", (event_id,))
        return cur.fetchall()
    finally:
        cur.close(); con.close()


def update_playdate_event_status(event_id, status):
    if status not in ('Open', 'Cancelled', 'Completed'):
        raise ValueError('Invalid playdate status.')
    ensure_playdate_tables()
    con, cur = connect()
    try:
        cur.execute("UPDATE playdate_events SET status=%s WHERE id=%s", (status, event_id))
        if status == 'Cancelled':
            cur.execute("UPDATE playdate_bookings SET status='Cancelled' WHERE event_id=%s AND status='Confirmed'", (event_id,))
        con.commit()
        return cur.rowcount > 0
    finally:
        cur.close(); con.close()
