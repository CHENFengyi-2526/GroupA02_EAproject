import sqlite3

def create_table_family_elderly_links():
    conn = sqlite3.connect("digital_human.db")
    cursor = conn.cursor()
    sql = '''
    CREATE TABLE IF NOT EXISTS family_elderly_links (
        link_id INTEGER PRIMARY KEY AUTOINCREMENT,
        family_user_id INTEGER,
        elderly_profile_id INTEGER,
        relationship TEXT,
        linked_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        FOREIGN KEY(family_user_id) REFERENCES users(user_id),
        FOREIGN KEY(elderly_profile_id) REFERENCES elderly_profiles(profile_id)
    );
    '''
    cursor.execute(sql)
    conn.commit()
    conn.close()
    print("Table: family_elderly_links created")

if __name__ == "__main__":
    create_table_family_elderly_links()
