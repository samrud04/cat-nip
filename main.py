from flask import Flask, render_template, request, redirect
from db import add_data

app = Flask(__name__)

# ---------------- HOME ----------------
@app.route("/")
def home():
    return render_template("home.html")

# ---------------- LOGIN ----------------
@app.route("/login")
def login():
    return render_template("login.html")

# ---------------- REGISTER ----------------
@app.route("/register")
def register():
    return render_template("register.html")

# ---------------- USER LOGIN ----------------
@app.route("/user", methods=["GET", "POST"])
def user_login():
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]

        add_data("login_det", (username, password))
        return redirect("/")

    return render_template("user_login.html")

# ---------------- EMPLOYEE ----------------
@app.route("/employee")
def employee_login():
    return render_template("employee_login.html")

# ---------------- ADMIN ----------------
@app.route("/admin")
def admin_login():
    return render_template("admin_login.html")


if __name__ == "__main__":
    app.run(debug=True)