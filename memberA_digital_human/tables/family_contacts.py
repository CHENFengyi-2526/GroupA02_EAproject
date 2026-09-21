import sqlite3

def create_table_family_contacts():
    conn = sqlite3.connect("digital_human.db")
    cursor = conn.cursor()
    sql = '''
    CREATE TABLE IF NOT EXISTS family_contacts (
        contact_id INTEGER PRIMARY KEY AUTOINCREMENT,
        user_id INTEGER,
        contact_name TEXT,
        phone TEXT,
        relationship TEXT,
        is_emergency INTEGER DEFAULT 0,
        FOREIGN KEY(user_id) REFERENCES users(user_id)
    );
    '''
    cursor.execute(sql)
    conn.commit()
    conn.close()
    print("Table: family_contacts created")

if __name__ == "__main__":
    create_table_family_contacts()
