import sqlite3

# Create connection to SQLite database
conn = sqlite3.connect("fitness.db", check_same_thread=False)
cursor = conn.cursor()

# Create 'classes' table
cursor.execute('''
CREATE TABLE IF NOT EXISTS classes (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    datetime TEXT NOT NULL,
    instructor TEXT NOT NULL,
    slots INTEGER NOT NULL
)
''')

# Create 'bookings' table
cursor.execute('''
CREATE TABLE IF NOT EXISTS bookings (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    class_id INTEGER NOT NULL,
    client_name TEXT NOT NULL,
    client_email TEXT NOT NULL,
    FOREIGN KEY (class_id) REFERENCES classes(id)
)
''')

conn.commit()
