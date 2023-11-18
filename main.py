from flask import Flask, jsonify, request, session
from flask_bcrypt import Bcrypt
from flask_cors import CORS
from flask_session import Session 
import sqlite3

app = Flask(__name__)
app.secret_key = 'testesttest222'  
bcrypt = Bcrypt(app)


app.config["SESSION_TYPE"] = "filesystem"
Session(app)

CORS(app, supports_credentials=True)  

conn = sqlite3.connect("komodoHub.db", check_same_thread=False)
cursor = conn.cursor()

cursor.execute('''
    CREATE TABLE IF NOT EXISTS passwords (
        passID INTEGER PRIMARY KEY AUTOINCREMENT,
        passHash TEXT NOT NULL
    )''')
cursor.execute('''
    CREATE TABLE IF NOT EXISTS users (
        userID INTEGER PRIMARY KEY AUTOINCREMENT,
        fName TEXT,
        lName TEXT,
        email TEXT,
        passID INTEGER,
        username TEXT,
        roleID INTEGER,
        visualID INTEGER,
        dob TEXT,
        FOREIGN KEY (visualID) REFERENCES visPreset (visID),
        FOREIGN KEY (roleID) REFERENCES role (roleID),
        FOREIGN KEY (passID) REFERENCES passwords (passID)
    )''')

@app.route('/register', methods=['POST'])
def register():
    data = request.get_json()
    fName = data.get('fName')
    lName = data.get('lName')
    email = data.get('email')
    password = data.get('password')
    DOB = data.get('DOB')

    if email and password and fName and lName and DOB:
        cursor.execute('SELECT email FROM users WHERE email=?', [email])
        if cursor.fetchone():
            return jsonify({"success": False, "message": "Email already exists"}), 400
        else:
            hashed_password = bcrypt.generate_password_hash(password).decode('utf-8')
            cursor.execute('INSERT INTO passwords (passHash) VALUES (?)', [hashed_password])
            passID = cursor.lastrowid
            cursor.execute('INSERT INTO users (fName, lName, email, passID, dob) VALUES (?, ?, ?, ?, ?)', [fName, lName, email, passID, DOB])
            conn.commit()
            return jsonify({"success": True, "message": "Registration successful"}), 201
    else:
        return jsonify({"success": False, "message": "Missing data"}), 400

@app.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    email = data.get('email')
    password = data.get('password')

    if email and password:
        cursor.execute('''
            SELECT users.userID, passwords.passHash, users.roleID
            FROM users
            JOIN passwords ON users.passID = passwords.passID
            WHERE users.email = ?
        ''', (email,))
        result = cursor.fetchone()

        if result:
            user_id, passHash, role_id = result
            if bcrypt.check_password_hash(passHash, password):
                session['user_id'] = user_id
                print("Logged in user ID:", user_id)
                return jsonify({"success": True, "message": "Login successful", "roleID": role_id}), 200
            else:
                return jsonify({"success": False, "message": "Invalid password"}), 401
        else:
            return jsonify({"success": False, "message": "Invalid email"}), 401
    else:
        return jsonify({"success": False, "message": "Missing data"}), 400

    
@app.route('/get-user-info')
def get_user_info():
    user_id = session.get('user_id')
    print("Session user ID:", user_id) 

    if not user_id:
        return jsonify({"error": "Not logged in"}), 401

    query = """
    SELECT users.userID, users.fName, role.roleName, users.email, visPreset.visName
    FROM users
    LEFT JOIN role ON users.roleID = role.roleID
    LEFT JOIN visPreset ON users.VisualID = visPreset.visID
    WHERE users.userID = ?
    """

    cursor.execute(query, (user_id,))
    user = cursor.fetchone()
    if user:
        return jsonify({"userID": user[0], "username": user[1], "role": user[2], "email": user[3], "visual": user[4]})
    else:
        return jsonify({"error": "User not found"}), 404
    
@app.route('/get-allusers')
def get_allusers():
    user_id = session.get('user_id')
    if not user_id:
        return jsonify({"error": "Not logged in"}), 401

    cursor.execute("SELECT roleID FROM users WHERE userID = ?", (user_id,))
    user_role = cursor.fetchone()
    if user_role is None or user_role[0] not in [3, 4]:  
        return jsonify({"error": "Unauthorized access"}), 403

    query = """
        SELECT U.userID, U.fName, U.lName, U.email, U.username, U.roleID, U.dob, R.roleName
        FROM users U
        LEFT JOIN role R ON R.roleID = U.roleID
        """

    cursor.execute(query)
    users = cursor.fetchall()
    users_list = [
        {
            "userID": user[0], "fName": user[1], "lName": user[2],
            "email": user[3], "username": user[4], "roleID": user[5],
            "dob": user[6], "roleName": user[7]
        }
        for user in users
    ]
    
    return jsonify(users_list)

@app.route('/get-roles')
def get_roles():
    cursor.execute("SELECT roleID, roleName FROM role")  
    roles = cursor.fetchall()
    return jsonify([{"roleID": role[0], "roleName": role[1]} for role in roles])

@app.route('/update-role/<int:update_user_id>', methods=['POST'])
def update_role(update_user_id):
    logged_in_user_id = session.get('user_id')
    if not logged_in_user_id:
        return jsonify({"error": "Not logged in"}), 401

    cursor.execute("SELECT roleID FROM users WHERE userID = ?", (logged_in_user_id,))
    user_role = cursor.fetchone()
    if user_role is None or user_role[0] not in [3, 4]:  
        return jsonify({"error": "Unauthorized access"}), 403

    data = request.get_json()
    new_role_id = data.get('newRoleID')

    cursor.execute("UPDATE users SET roleID = ? WHERE userID = ?", (new_role_id, update_user_id))
    conn.commit()

    return jsonify({"success": True, "message": "Role updated successfully"})


@app.route('/update-theme/<int:user_id>', methods=['POST'])
def update_theme(user_id):
    logged_in_user_id = session.get('user_id')
    if not logged_in_user_id:
        return jsonify({"error": "Not logged in"}), 401
    data = request.get_json()
    new_visual_id = data.get('newVisualID')

    cursor.execute("UPDATE users SET visualID = ? WHERE userID = ?", (new_visual_id, user_id))
    conn.commit()

    return jsonify({"success": True, "message": "Theme updated successfully"})

    
if __name__ == '__main__':
    app.run(debug=True)
