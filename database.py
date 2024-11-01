import sqlite3


class Database:
    def __init__(self, db):
        self.conn = sqlite3.connect(db)  # Creates a connection to the Database
        self.cur = self.conn.cursor()
        self.cur.execute("""
                         CREATE TABLE IF NOT EXISTS clients (
                                id INTEGER PRIMARY KEY,
                                username TEXT,
                                hashpassword TEXT)
                         """)
        self.conn.commit()

    # Gets list of users in the Database
    def get_users(self):
        self.cur.execute("SELECT username FROM clients")
        user_list = self.cur.fetchall()
        return user_list

    # Adds user to the Database
    def add_user(self, username, hashpassword):
        self.cur.execute("INSERT INTO clients VALUES (NULL, ?, ?)",
                         (username, hashpassword))
        self.conn.commit()

    # Gets username and hashpassword
    def get_user_pwhash(self, username):
        self.cur.execute("SELECT username, hashpassword FROM clients WHERE username=?",
                         [username])
        user_pwhash = self.cur.fetchall()
        return user_pwhash
        # self.conn.commit()

    # Deletes user account
    def delete_user(self, username):
        self.cur.execute("DELETE FROM clients WHERE username=?",
                         (username,))
        self.conn.commit()

    # Close the connection
    def __del__(self):
        self.conn.close()
