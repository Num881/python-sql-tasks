import psycopg2
from psycopg2.extras import execute_values

conn = psycopg2.connect('postgresql://postgres:@localhost:5432/test_db')


# BEGIN (write your solution here)
def batch_insert(conn, products):
    with conn.cursor() as cur:
        execute_values(
            cur,
            """
            INSERT INTO products (name, price, quantity)
            VALUES %s
            """,
            [(p['name'], p['price'], p['quantity']) for p in products]
        )
    conn.commit()


def get_all_products(conn):
    with conn.cursor() as cur:
        cur.execute("""
            SELECT id, name, price, quantity
            FROM products
            ORDER BY price DESC
        """)
        return cur.fetchall()
# END
