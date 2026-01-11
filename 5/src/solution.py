import psycopg2
from psycopg2.extras import DictCursor


conn = psycopg2.connect('postgresql://postgres:@localhost:5432/test_db')


# BEGIN (write your solution here)
def create_post(conn, post_data):
    with conn.cursor(cursor_factory=DictCursor) as cur:
        cur.execute("""
            INSERT INTO posts (title, content, author_id)
            VALUES (%(title)s, %(content)s, %(author_id)s)
            RETURNING id
        """, post_data)
        conn.commit()
        return cur.fetchone()['id']


def add_comment(conn, comment_data):
    with conn.cursor(cursor_factory=DictCursor) as cur:
        cur.execute("""
            INSERT INTO comments (post_id, author_id, content)
            VALUES (%(post_id)s, %(author_id)s, %(content)s)
            RETURNING id
        """, comment_data)
        conn.commit()
        return cur.fetchone()['id']


def get_latest_posts(conn, limit):
    with conn.cursor(cursor_factory=DictCursor) as cur:
        cur.execute("""
            SELECT id, title, content, author_id, created_at
            FROM posts
            ORDER BY created_at DESC
            LIMIT %s
        """, (limit,))
        posts = cur.fetchall()

        result = []
        for post in posts:
            cur.execute("""
                SELECT id, author_id, content, created_at
                FROM comments
                WHERE post_id = %s
                ORDER BY created_at ASC
            """, (post['id'],))
            comments = cur.fetchall()

            post_dict = dict(post)
            post_dict['comments'] = comments
            result.append(post_dict)

        return result
# END
