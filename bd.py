import sqlite3

conn = sqlite3.connect('database.db')
print("Opened database successfully")

conn.execute('CREATE TABLE tweets_list (label TEXT, tweet TEXT)')
print("your table created")
conn.close()
