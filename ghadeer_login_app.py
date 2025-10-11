
from flask import Flask, render_template_string, request

app = Flask(__name__)

# قاعدة بيانات وهمية للمستخدمين
users = {
    "admin": "gak123",
    "ghadeer": "logistics2025"
}

# نموذج HTML مدمج
login_template = '''
<!DOCTYPE html>
<html lang="ar" dir="rtl">
<head>
  <meta charset="utf-8"/>
  <meta name="viewport" content="width=device-width, initial-scale=1"/>
  <title>تسجيل الدخول | شركة الغدير</title>
  <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.2/dist/css/bootstrap.rtl.min.css" rel="stylesheet">
  <link href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.5.2/css/all.min.css" rel="stylesheet">
  <link href="https://fonts.googleapis.com/css2?family=Almarai:wght@300;400;700&display=swap" rel="stylesheet">
  <style>
    body {
      font-family: 'Almarai', sans-serif;
      background: linear-gradient(to left, #f1f5f9, #e0f7fa);
      min-height: 100vh;
      display: flex;
      align-items: center;
      justify-content: center;
      padding: 30px 15px;
    }
    .login-box {
      width: 100%;
      max-width: 500px;
      background: white;
      border-radius: 16px;
      box-shadow: 0 8px 24px rgba(0,0,0,0.05);
      padding: 30px;
    }
    .small-muted {
      color: #6c757d;
      font-size: 0.9rem;
    }
    .form-label {
      color: #1e293b;
    }
    footer {
      text-align: center;
      margin-top: 20px;
      font-size: 0.85rem;
      color: #94a3b8;
    }
  </style>
</head>
<body>

  <div class="login-box">
    <div class="text-center mb-4">
      <h3 class="mt-3">تسجيل الدخول</h3>
      <div class="small-muted">أدخل بياناتك للوصول إلى نظام شركة الغدير</div>
    </div>

    {% if error %}
      <div class="alert alert-danger text-center">{{ error }}</div>
    {% endif %}

    <form method="post">
      <div class="mb-3">
        <label class="form-label">اسم المستخدم</label>
        <input type="text" name="username" class="form-control" required>
      </div>
      <div class="mb-3">
        <label class="form-label">كلمة المرور</label>
        <input type="password" name="password" class="form-control" required>
      </div>
      <div class="d-grid gap-2">
        <button class="btn btn-primary">
          <i class="fa-solid fa-right-to-bracket"></i> دخول
        </button>
      </div>
    </form>

    <footer class="mt-4">© 2025 شركة الغدير للخدمات اللوجستية</footer>
  </div>

</body>
</html>
'''

@app.route("/", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        user = request.form.get("username")
        pw = request.form.get("password")
        if user in users and users[user] == pw:
            return f"<h1 style='font-family:Almarai;text-align:center'>✅ أهلاً {user}، تم تسجيل الدخول بنجاح.</h1>"
        else:
            return render_template_string(login_template, error="❌ اسم المستخدم أو كلمة المرور غير صحيحة.")
    return render_template_string(login_template)

if __name__ == "__main__":
    app.run(debug=True)
