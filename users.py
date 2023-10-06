import sqlite3

def main(username, password):
    connection = sqlite3.connect('users.db')
    cursor = connection.cursor()
    #cursor.execute("CREATE TABLE users (id INTEGER PRIMARY KEY AUTOINCREMENT, username TEXT, password TEXT)")

    cursor.execute('''INSERT INTO users (username, password) VALUES(?,?)''', (username, password))
    connection.commit()

