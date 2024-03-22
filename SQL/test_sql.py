import sqlite3

connection = sqlite3.Connection('test_db.db')
connection.close()
