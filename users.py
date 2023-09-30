import sqlite3

def main(username, password):
    connection = sqlite3.connect('users.db')
    cursor = connection.cursor()

    cursor.execute('''INSERT INTO users VALUES(?,?,?)''', (1, username, password))
    connection.commit()
