import sqlite3

def insert_classes(db_file):
    try:
        conn = sqlite3.connect(db_file)
        cursor = conn.cursor()

        classes = [
            ('Maths', 8, 1, 1),
            ('History', 9, 1, 2),
            ('Geography', 10, 1, 3)
        ]

        for class_name, teacher, school_id, games_id in classes:
            cursor.execute("INSERT INTO classes (className, teacher, schoolID, gamesID) VALUES (?, ?, ?, ?)", (class_name, teacher, school_id, games_id))

        conn.commit()
        print("Classes have been inserted successfully.")
    except sqlite3.Error as e:
        print(f"An error occurred: {e}")
    finally:
        if conn:
            conn.close()

db_file = 'komodoHub.db' 
insert_classes(db_file)
