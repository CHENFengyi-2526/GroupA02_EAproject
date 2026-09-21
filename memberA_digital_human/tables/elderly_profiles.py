import sqlite3

def create_table_elderly_profiles():
    conn = sqlite3.connect("digital_human.db")
    cursor = conn.cursor()
    sql = '''
    CREATE TABLE IF NOT EXISTS elderly_profiles (
        profile_id INTEGER PRIMARY KEY AUTOINCREMENT,
        user_id INTEGER,
        full_name TEXT,
        age INTEGER,
        gender TEXT,
        medical_history TEXT,
        address TEXT,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        FOREIGN KEY(user_id) REFERENCES users(user_id)
    );
    '''
    cursor.execute(sql)
    conn.commit()
    conn.close()
    print("Table: elderly_profiles created")

if __name__ == "__main__":
    create_table_elderly_profiles()
