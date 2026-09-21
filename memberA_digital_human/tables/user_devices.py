import sqlite3

def create_table_user_devices():
    conn = sqlite3.connect("digital_human.db")
    cursor = conn.cursor()
    sql = '''
    CREATE TABLE IF NOT EXISTS user_devices (
        device_id INTEGER PRIMARY KEY AUTOINCREMENT,
        user_id INTEGER,
        device_name TEXT,
        device_type TEXT,
        device_uuid TEXT UNIQUE,
        last_active TIMESTAMP,
        FOREIGN KEY(user_id) REFERENCES users(user_id)
    );
    '''
    cursor.execute(sql)
    conn.commit()
    conn.close()
    print("Table: user_devices created")

if __name__ == "__main__":
    create_table_user_devices()
