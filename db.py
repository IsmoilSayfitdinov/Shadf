import psycopg2 as db
from datetime import datetime

class Database:
    def __init__(self, config):
        self.conn = db.connect(
            database=config['DB_NAME'],
            user=config['DB_USER'],
            password=config['DB_PASS'],
            host=config['DB_HOST'],
            port=config['DB_PORT']
        )
        self.cursor = self.conn.cursor()
        self.conn.commit()

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.conn.close()

    def create_tables(self):
        users_table = """
        CREATE TABLE IF NOT EXISTS users(
            id SERIAL PRIMARY KEY,
            username VARCHAR(100) UNIQUE NOT NULL,
            password VARCHAR(100) NOT NULL,
            created_at TIMESTAMP DEFAULT NOW()
        )
        """
        self.cursor.execute(users_table)
        self.conn.commit()

    def add_user(self, username, password):
        query = """
        INSERT INTO users (username, password)
        VALUES (%s, %s, %s, %s)
        ON CONFLICT (username) DO NOTHING
        """
        self.cursor.execute(query, (username, password))
        self.conn.commit()

    def get_all_users(self):
        query = "SELECT id, username, created_at FROM users"
        self.cursor.execute(query)
        return self.cursor.fetchall()

    def deactivate_user(self, username):
        query = "UPDATE users SET is_active = FALSE WHERE username = %s"
        self.cursor.execute(query, (username,))
        self.conn.commit()

    def find_user(self, username):
        query = "SELECT id, username, password, FROM users WHERE username = %s"
        self.cursor.execute(query, (username,))
        return self.cursor.fetchone()
