import sqlite3

def create_table_user_settings():
    conn = sqlite3.connect("digital_human.db")
    cursor = conn.cursor()
    sql = '''
    CREATE TABLE IF NOT EXISTS user_settings (
        setting_id INTEGER PRIMARY KEY AUTOINCREMENT,
        user_id INTEGER UNIQUE,
        notification_enabled INTEGER DEFAULT 1,
        language TEXT DEFAULT 'en',
        theme TEXT DEFAULT 'light',
        updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        FOREIGN KEY(user_id) REFERENCES users(user_id)
    );
    '''
    cursor.execute(sql)
    conn.commit()
    conn.close()
    print("Table: user_settings created")

if __name__ == "__main__":
    create_table_user_settings()
