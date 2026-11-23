
from flask import Flask, request, render_template, redirect, url_for
import mysql.connector
from werkzeug.security import generate_password_hash, check_password_hash

app = Flask(__name__)

# -----------------------------------------
# XAMPP MySQL Connection
# -----------------------------------------

db = mysql.connector.connect(
    host="localhost",
    user="root",
    password="",
    database="details",
    port=3306
)

cursor = db.cursor()

print("Database Connected Successfully!")


# -----------------------------------------
# HOME PAGE
# -----------------------------------------

@app.route("/")
def home():
    return redirect(url_for("signup"))


# -----------------------------------------
# SIGNUP PAGE
# -----------------------------------------

@app.route("/signup", methods=["GET", "POST"])
def signup():

    message = ""

    if request.method == "POST":

        name = request.form.get("name")
        roll_no = request.form.get("roll_no")
        address = request.form.get("address")
        phone_number = request.form.get("phone_number")
        username = request.form.get("username")
        password = request.form.get("password")

        # Check whether username already exists
        cursor.execute(
            "SELECT id FROM student_list WHERE username = %s",
            (username,)
        )

        existing_user = cursor.fetchone()

        if existing_user:
            message = "Username already exists!"

        else:
            # Hash password
            hashed_password = generate_password_hash(password)

            query = """
                INSERT INTO student_list
                (name, roll_no, address, phone_number, username, password)
                VALUES (%s, %s, %s, %s, %s, %s)
            """

            values = (
                name,
                roll_no,
                address,
                phone_number,
                username,
                hashed_password
            )

            cursor.execute(query, values)
            db.commit()

            print("New Student Registered:", username)

            return redirect(url_for("login"))

    return render_template("signup.html", message=message)


# -----------------------------------------
# LOGIN PAGE
# -----------------------------------------

@app.route("/login", methods=["GET", "POST"])
def login():

    message = ""

    if request.method == "POST":

        username = request.form.get("username")
        password = request.form.get("password")

        query = """
            SELECT id, name, password
            FROM student_list
            WHERE username = %s
        """

        cursor.execute(query, (username,))
        user = cursor.fetchone()

        if user and check_password_hash(user[2], password):

            print("Login Successful:", username)

            message = "Login Successful! Welcome " + user[1]

        else:
            message = "Invalid Username or Password!"

    return render_template("login.html", message=message)


# -----------------------------------------
# RUN FLASK APPLICATION
# -----------------------------------------

if __name__ == "__main__":
    app.run(
        host="127.0.0.1",
        port=5000,
        debug=True,
        use_reloader=False
    )
