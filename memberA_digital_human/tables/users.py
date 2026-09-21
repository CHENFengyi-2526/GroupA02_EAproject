import sqlite3

def create_table_users():
    conn = sqlite3.connect("digital_human.db")
    cursor = conn.cursor()
    sql = '''
    CREATE TABLE IF NOT EXISTS users (
        user_id INTEGER PRIMARY KEY AUTOINCREMENT,
        username TEXT NOT NULL,
        password_hash TEXT NOT NULL,
        email TEXT,
        role TEXT,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    );
    '''
    cursor.execute(sql)
    conn.commit()
    conn.close()
    print("Table: users created")

if __name__ == "__main__":
    create_table_users()
