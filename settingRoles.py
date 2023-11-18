import sqlite3

def update_user_roles(db_file):
    try:
        conn = sqlite3.connect(db_file)
        cursor = conn.cursor()

        user_role_updates = [
            (1, 1), 
            (2, 2), 
            (3, 3),
            (4, 4)   
        ]
        for user_id, role_id in user_role_updates:
            cursor.execute("UPDATE users SET roleID = ? WHERE userID = ?", (role_id, user_id))
        conn.commit()
        print("User roles have been updated successfully.")
    except sqlite3.Error as e:
        print(f"An error occurred: {e}")
    finally:
        if conn:
            conn.close()

db_file = 'komodoHub.db'  

update_user_roles(db_file)
