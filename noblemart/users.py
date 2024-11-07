import sqlite3

def createTables():
    conn = sqlite3.connect('users.db')
    cursor = conn.cursor()
    cursor.execute('''CREATE TABLE IF NOT EXISTS users(
            id integer primary key AUTOINCREMENT,
            firstname VARCHAR(255) NOT NULL,
            lastname VARCHAR(255) NOT NULL,
            email INTEGER NOT NULL,
            username INTEGER NOT NULL,
            password VARCHAR(255) NOT NULL,
            admin INTEGER NOT NULL
    )''')
    conn.commit()
    conn.close

def insertUser(data):
    conn = sqlite3.connect('users.db')
    cursor = conn.cursor()
    cursor.execute('''INSERT into users (firstname, lastname, email, username, password, admin) VALUES (?, ?, ?, ?, ?, ?)''', data)
    conn.commit()
    conn.close()

def getUsers(data):
    conn = sqlite3.connect('users.db')
    cursor = conn.cursor()
    cursor.execute('SELECT username, password, admin FROM users WHERE username = ? AND password = ?', (data[0], data[1]))
    user = cursor.fetchone() 
    conn.close()
    return user

