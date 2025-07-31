from flask import Flask, render_template, request, redirect, url_for, session, flash
import sqlite3

app = Flask(__name__)
app.secret_key = "USA" # Must change later


# ROUTES
@app.route("/")
def home():
    return render_template("index.html")

@app.route("/about")
def about():
    return render_template("about.html")

@app.route("/admissions", methods=["GET", "POST"])
def admissions():
    if request.method == "POST":
        student_name = request.form["student_name"]
        age = request.form["age"]
        grade = request.form["grade"]
        guardian_contact = request.form["guardian_contact"]

        conn = sqlite3.connect("database.db")
        cursor = conn.cursor()
        cursor.execute("INSERT INTO admissions (student_name, age, grade, guardian_contact) VALUES(?, ?, ?, ?)", (student_name, age, grade, guardian_contact))
        conn.commit()
        conn.close()
        
        flash("application")
        return redirect(url_for("thank_you"))
    return render_template("admissions.html")

@app.route("/contact", methods=["GET", "POST"])
def contact():
    if request.method == "POST":
        name = request.form["name"]
        email = request.form["email"]
        message = request.form["message"]

        # Add data to database  
        conn = sqlite3.connect("database.db")
        cursor = conn.cursor()
        cursor.execute("INSERT INTO messages (name, email, message) VALUES (?, ?, ?)", (name, email, message))
        conn.commit()
        conn.close()

        flash("message")
        return redirect("/thankyou") 
    return render_template("contact.html")

@app.route("/thankyou")
def thank_you():
    return render_template("thankyou.html")

@app.route("/admin")
def admin():
    if not session.get("admin_logged_in"):
        return redirect("/admin/login")
    
    return render_template("admin.html")

@app.route("/admin/messages")
def view_messages():
    if not session.get("admin_logged_in"):
        return redirect(url_for("login"))
    
    conn = sqlite3.connect("database.db")
    cursor = conn.cursor()
    cursor.execute("SELECT id, name, email, message FROM messages")
    messages = cursor.fetchall()
    conn.close()

    return render_template("messages.html", messages=messages)

@app.route("/admin/applications")
def view_applications():
    if not session.get("admin_logged_in"):
        return redirect(url_for("login"))
    
    conn = sqlite3.connect("database.db")
    cursor = conn.cursor()
    cursor.execute("""SELECT id, student_name, age, grade, guardian_contact 
                   FROM admissions
                   """)
    applications =cursor.fetchall()
    conn.close()

    return render_template("applications.html", applications=applications)

@app.route("/admin/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]

        conn = sqlite3.connect("database.db")
        cursor = conn.cursor()
        cursor.execute("""SELECT * FROM users 
                       WHERE username=? 
                       AND password=?""", (username, password))
        user = cursor.fetchone()
        conn.close()
        
        if user:
            session["admin_logged_in"] = True
            return (redirect(url_for("admin")))
        else:
            flash('Invalid credentials')
            # return redirect(url_for("login"))
        
    return render_template("login.html")

@app.route("/admin/logout")
def logout():
    session.pop("admin_logged_in", None)
    return redirect(url_for("login"))

# DATABASE SETUP FUNCTION
def init_db():
    conn = sqlite3.connect("database.db")
    cursor = conn.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS messages (
        id INTEGER PRIMARY KEY AUTOINCREMENT, 
        name TEXT NOT NULL, 
        email TEXT NOT NULL, 
        message TEXT NOT NULL)
    """)

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS users (
        id INTEGER PRIMARY KEY AUTOINCREMENT, 
        username TEXT UNIQUE NOT NULL, 
        password TEXT NOT NULL)
    """)

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS admissions (
        id INTEGER PRIMARY KEY AUTOINCREMENT, 
        student_name TEXT NOT NULL,
        age INTEGER NOT NULL,
        grade TEXT NOT NULL,
        guardian_contact TEXT NOT NULL)    
    """)

    conn.commit()
    conn.close()

# MUST RUN BEFORE THE START OF APP TO INITIALIZE THE DATABASE
init_db()

if __name__ == "__main__":
    app.run(debug=True)