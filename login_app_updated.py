
from flask import Flask, render_template_string, request, redirect, url_for

app = Flask(__name__)

# قاعدة بيانات وهمية للمستخدمين
users = {
    "admin": "123456",
    "ghadeer": "logistics2025",
    "admin": "Star1996",
    "muhanad": "Muhanad1996"
}

# HTML الخاص بواجهة تسجيل الدخول (نفس تصميم index_modern.html)
login_page = """<!DOCTYPE html>
<html lang="ar" dir="rtl">
<head>
  <meta charset="UTF-8">
  <title>تسجيل الدخول | Ghadeer</title>
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <link href="https://fonts.googleapis.com/css2?family=Cairo:wght@400;700&display=swap" rel="stylesheet">
  <style>
    * {{
      box-sizing: border-box;
    }}
    body {{
      font-family: 'Cairo', sans-serif;
      margin: 0;
      background: linear-gradient(to left, #e0f2fe, #f1f5f9);
      display: flex;
      justify-content: center;
      align-items: center;
      min-height: 100vh;
      padding: 16px;
    }}
    .login-container {{
      background: white;
      border-radius: 20px;
      box-shadow: 0 4px 20px rgba(0,0,0,0.1);
      padding: 40px 30px;
      max-width: 400px;
      width: 100%;
    }}
    h2 {{
      text-align: center;
      margin-bottom: 24px;
      color: #1e3a8a;
    }}
    label {{
      display: block;
      margin-bottom: 8px;
      color: #475569;
    }}
    input[type="text"], input[type="password"] {{
      width: 100%;
      padding: 12px;
      border: 1px solid #cbd5e1;
      border-radius: 8px;
      margin-bottom: 16px;
      font-size: 1rem;
    }}
    button {{
      width: 100%;
      padding: 12px;
      background-color: #3b82f6;
      color: white;
      font-size: 1rem;
      border: none;
      border-radius: 8px;
      cursor: pointer;
      transition: background-color 0.3s ease;
    }}
    button:hover {{
      background-color: #2563eb;
    }}
    .footer-text {{
      margin-top: 20px;
      text-align: center;
      font-size: 0.9rem;
      color: #64748b;
    }}
    .error {{
      color: red;
      text-align: center;
      margin-bottom: 10px;
    }}
  </style>
</head>
<body>
  <div class="login-container">
    <h2>تسجيل الدخول</h2>
    {% if error %}
      <div class="error">{{{{ error }}}}</div>
    {% endif %}
    <form method="post">
      <label for="username">اسم المستخدم</label>
      <input type="text" id="username" name="username" placeholder="أدخل اسم المستخدم">

      <label for="password">كلمة المرور</label>
      <input type="password" id="password" name="password" placeholder="••••••••">

      <button type="submit">دخول</button>
    </form>
    <div class="footer-text">© 2025 Ghadeer Logistics</div>
  </div>
</body>
</html>"""

success_page = """
<!DOCTYPE html>
<html lang="ar" dir="rtl">
<head>
  <meta charset="UTF-8">
  <title>مرحباً بك</title>
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <style>
    body {{
      font-family: 'Cairo', sans-serif;
      background: #f1f5f9;
      display: flex;
      justify-content: center;
      align-items: center;
      height: 100vh;
      color: #1e293b;
    }}
  </style>
</head>
<body>
  <h1>مرحباً بك {{ user }} في نظام غدير ✅</h1>
</body>
</html>
"""

@app.route('/', methods=['GET', 'POST'])
def login():
    error = None
    if request.method == 'POST':
        user = request.form['username']
        pw = request.form['password']
        if user in users and users[user] == pw:
            return redirect(url_for('success', user=user))
        else:
            error = "اسم المستخدم أو كلمة المرور غير صحيحة"
    return render_template_string(login_page, error=error)

@app.route('/success/<user>')
def success(user):
    return render_template_string(success_page, user=user)

if __name__ == '__main__':
    app.run(debug=True)
