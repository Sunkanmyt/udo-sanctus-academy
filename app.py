from flask import Flask, render_template, request, redirect, url_for
import sqlite3

app = Flask(__name__)

# ROUTES
@app.route("/")
def home():
    return render_template("index.html")

@app.route("/about")
def about():
    return render_template("about.html")

@app.route("/admissions", methods=["GET", "POST"])
def admissions():
    if request == "POST":
        pass
    return render_template("admissions.html")

@app.route("/contact", methods=["GET", "POST"])
def contact():
    if request.method == "POST":
        name = request.form["name"]
        email = request.form["email"]
        message = request.form["message"]

        # Add data to database  
        conn = sqlite3.connect("contact.db")
        cursor = conn.cursor()
        cursor.execute("INSERT INTO messages (name, email, message) VALUES (?, ?, ?)", (name, email, message))
        conn.commit()
        conn.close()

        return redirect("/thankyou") 
    return render_template("contact.html")

@app.route("/thankyou")
def thank_you():
    return render_template("thankyou.html")
    
# DATABASE SETUP FUNCTION
def init_db():
    conn = sqlite3.connect("contact.db")
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS messages (
        id INTEGER PRIMARY KEY AUTOINCREMENT, 
        name TEXT NOT NULL, 
        email TEXT NOT NULL, 
        message TEXT NOT NULL)
    """)
    conn.commit()
    conn.close()

# MUST RUN BEFORE THE START OF APP TO INITIALIZE THE DATABASE
init_db()

if __name__ == "__main__":
    app.run(debug=True)