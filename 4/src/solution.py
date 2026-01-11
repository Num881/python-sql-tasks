import psycopg2
from psycopg2.extras import DictCursor


conn = psycopg2.connect('postgresql://postgres:@localhost:5432/test_db')


# BEGIN (write your solution here)
def get_order_sum(conn, month):
    with conn.cursor(cursor_factory=DictCursor) as cur:
        cur.execute("""
            SELECT
                c.customer_name,
                COALESCE(SUM(o.total_amount), 0) AS total
            FROM customers c
            LEFT JOIN orders o ON c.customer_id = o.customer_id
            WHERE EXTRACT(MONTH FROM o.order_date) = %s
               OR o.order_date IS NULL
            GROUP BY c.customer_id, c.customer_name
            ORDER BY c.customer_name
        """, (month,))

        result = []
        for row in cur:
            name = row['customer_name']
            amount = int(row['total'])
            result.append(f"Покупатель {name} совершил покупок на сумму {amount}")

        return "\n".join(result)
# END
