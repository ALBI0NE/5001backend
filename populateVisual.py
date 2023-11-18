import sqlite3

def insert_visuals(db_file):
    try:
        conn = sqlite3.connect(db_file)
        cursor = conn.cursor()

        visuals = [
            ('Dark', "dark", "dark"),
            ('White', "white", "white"),
            ('Purple',"purple", "purple")
        ]

        for visName, bgColour, txtColour in visuals:
            cursor.execute("INSERT INTO visPreset (visName, bgColour, txtColour) VALUES (?, ?, ?)", (visName, bgColour, txtColour))

        conn.commit()
        print("Visuals have been inserted successfully.")
    except sqlite3.Error as e:
        print(f"An error occurred: {e}")
    finally:
        if conn:
            conn.close()

db_file = 'komodoHub.db' 
insert_visuals(db_file)
