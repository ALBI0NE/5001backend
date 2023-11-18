import sqlite3

def insert_schools(db_file):
    try:
        conn = sqlite3.connect(db_file)
        cursor = conn.cursor()

        schools = [
            (4, 'Komodo School International University', 'Indonesia')
        ]

        for headteacher, school_type, location in schools:
            cursor.execute("INSERT INTO schools (headteacher, schoolType, location) VALUES (?, ?, ?)", (headteacher, school_type, location))

        conn.commit()
        print("Schools have been inserted successfully.")
    except sqlite3.Error as e:
        print(f"An error occurred: {e}")
    finally:
        if conn:
            conn.close()

db_file = 'komodoHub.db'
insert_schools(db_file)
