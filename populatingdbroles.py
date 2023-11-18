import sqlite3

def insert_roles(db_file):
    try:
        conn = sqlite3.connect(db_file)
        cursor = conn.cursor()

        roles = [
            #('Outside User', '0'),  
            #('Student', '1'),       
            #('Teacher', '2')   
            ('HeadTeacher', '3')     
        ]

        for role_name, perms in roles:
            cursor.execute("INSERT INTO role (roleName, perms) VALUES (?, ?)", (role_name, perms))

        conn.commit()
        print("Roles have been inserted successfully.")
    except sqlite3.Error as e:
        print(f"An error occurred: {e}")
    finally:
        if conn:
            conn.close()


db_file = 'komodoHub.db' 

# Insert the roles
insert_roles(db_file)
