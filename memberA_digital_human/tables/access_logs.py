import sqlite3

def create_table_access_logs():
    conn = sqlite3.connect("digital_human.db")
    cursor = conn.cursor()
    sql = '''
    CREATE TABLE IF NOT EXISTS access_logs (
        log_id INTEGER PRIMARY KEY AUTOINCREMENT,
        user_id INTEGER,
        action TEXT,
        ip_address TEXT,
        accessed_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        FOREIGN KEY(user_id) REFERENCES users(user_id)
    );
    '''
    cursor.execute(sql)
    conn.commit()
    conn.close()
    print("Table: access_logs created")

if __name__ == "__main__":
    create_table_access_logs()
