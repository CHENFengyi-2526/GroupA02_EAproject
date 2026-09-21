import sqlite3

def create_table_consent_records():
    conn = sqlite3.connect("digital_human.db")
    cursor = conn.cursor()
    sql = '''
    CREATE TABLE IF NOT EXISTS consent_records (
        consent_id INTEGER PRIMARY KEY AUTOINCREMENT,
        user_id INTEGER,
        consent_type TEXT,
        consent_status TEXT,
        signed_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        FOREIGN KEY(user_id) REFERENCES users(user_id)
    );
    '''
    cursor.execute(sql)
    conn.commit()
    conn.close()
    print("Table: consent_records created")

if __name__ == "__main__":
    create_table_consent_records()
