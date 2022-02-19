import psycopg2


class PostgreSQL:
    def __init__(self, db_uri):
        self.connection = psycopg2.connect(db_uri, sslmode='require')
        self.connection.autocommit = True

        self.cursor = self.connection.cursor()
        self.cursor.execute(
            """CREATE TABLE IF NOT EXISTS languages(
                id serial PRIMARY KEY,
                user_id integer NOT NULL,
                language text DEFAULT 'eng');"""
        )

    def load(self, user_id):
        self.cursor.execute(
            f"SELECT id FROM languages WHERE user_id = {user_id}"
        )

        return self.cursor.fetchone()

    def add_new_user(self, user_id):
        self.cursor.execute(
            f"INSERT INTO languages(user_id) VALUES(%s)", (user_id,)
        )

    def update_language(self, language, user_id):
        self.cursor.execute(
            f"UPDATE languages SET language = '{language}' WHERE user_id = {user_id}"
        )

    def get_language(self, user_id):
        self.cursor.execute(
            f"SELECT language FROM languages WHERE user_id = {user_id}"
        )

        return self.cursor.fetchone()