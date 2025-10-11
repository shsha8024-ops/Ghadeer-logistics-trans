
from flask import Flask, render_template, request, redirect, url_for, render_template_string

app = Flask(__name__)

# بيانات دخول بسيطة
users = {
    "admin": "Star1996",
    "muhanad": "Muhanad1996",
    "ghadeer": "logistics2025"
}

@app.route("/")
def home():
    return render_template("home_modern.html")

@app.route("/login", methods=["GET", "POST"])
def login():
    error = None
    if request.method == "POST":
        user = request.form["username"]
        pw = request.form["password"]
        if user in users and users[user] == pw:
            return redirect(url_for("dashboard", user=user))
        else:
            error = "اسم المستخدم أو كلمة المرور غير صحيحة"
    return render_template("index_modern.html", error=error)

@app.route("/signup")
def signup():
    return render_template("signup_modern.html")

@app.route("/dashboard/<user>")
def dashboard(user):
    return f"<h1 style='font-family:Cairo,sans-serif;text-align:center'>مرحباً {user} 👋</h1>"

@app.route("/about")
def about():
    return render_template("about_modern.html")

@app.route("/clients")
def clients():
    return render_template("client_modern.html")

@app.route("/contact")
def contact():
    return render_template("contact_modern.html")

@app.route("/track")
def track():
    return render_template("track_modern.html")

if __name__ == "__main__":
    app.run(debug=True)
