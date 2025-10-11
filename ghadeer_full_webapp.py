
from flask import Flask, render_template_string, request, redirect, url_for, send_file
import psycopg2
import os
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer
from reportlab.lib.styles import getSampleStyleSheet

app = Flask(__name__)

DATABASE_URL = os.environ.get("DATABASE_URL", "dbname='ghadeer' user='postgres' password='postgres' host='localhost'")

def get_conn():
    return psycopg2.connect(DATABASE_URL)

def init_db():
    with get_conn() as conn:
        cur = conn.cursor()
        cur.execute("""
            CREATE TABLE IF NOT EXISTS users (
                id SERIAL PRIMARY KEY,
                username VARCHAR(255) UNIQUE NOT NULL,
                password VARCHAR(255) NOT NULL
            )
        """)
        cur.execute("INSERT INTO users (username, password) VALUES (%s, %s) ON CONFLICT DO NOTHING", ("admin", "gak123"))
        cur.execute("INSERT INTO users (username, password) VALUES (%s, %s) ON CONFLICT DO NOTHING", ("ghadeer", "logistics2025"))
        conn.commit()

init_db()

dashboard_html = """
<!DOCTYPE html>
<html lang="ar" dir="rtl">
<head>
  <meta charset="utf-8"/>
  <title>لوحة التحكم | الغدير</title>
  <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.2/dist/css/bootstrap.rtl.min.css" rel="stylesheet">
  <style>
    body {
      font-family: Almarai, sans-serif;
      background: #f8fafc;
      padding: 40px;
    }
    .dashboard-box {
      max-width: 800px;
      margin: auto;
      background: white;
      padding: 30px;
      border-radius: 12px;
      box-shadow: 0 4px 10px rgba(0,0,0,0.06);
    }
    .dashboard-box h1 {
      color: #1e3a8a;
    }
  </style>
</head>
<body>
  <div class="dashboard-box text-center">
    <h1>مرحباً {{ user }} 👋</h1>
    <p class="lead mt-3">مرحباً بك في لوحة تحكم الغدير</p>
    <hr>
    <div class="list-group text-start mt-4">
      <a href="#" class="list-group-item list-group-item-action">🚚 إدارة الشحنات</a>
      <a href="#" class="list-group-item list-group-item-action">👥 إدارة العملاء</a>
      <a href="#" class="list-group-item list-group-item-action">💳 الفواتير والسداد</a>
      <a href="#" class="list-group-item list-group-item-action">📊 تقارير الأداء</a>
      <a href="#" class="list-group-item list-group-item-action">⚙️ إعدادات النظام</a>
    </div>
    <a href="/" class="btn btn-outline-secondary mt-4">تسجيل الخروج</a>
  </div>
</body>
</html>
"""
login_html = """
<!DOCTYPE html>
<html lang="ar" dir="rtl">
<head>
  <meta charset="utf-8"/>
  <title>تسجيل الدخول | الغدير</title>
  <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.2/dist/css/bootstrap.rtl.min.css" rel="stylesheet">
</head>
<body style="background:#f1f5f9;padding:40px">
  <div class="container" style="max-width:500px;background:white;padding:30px;border-radius:12px">
    <h3 class="text-center mb-4">تسجيل الدخول</h3>
    {% if error %}
      <div class="alert alert-danger text-center">{{ error }}</div>
    {% endif %}
    <form method="post">
      <div class="mb-3">
        <label>اسم المستخدم</label>
        <input type="text" name="username" class="form-control" required>
      </div>
      <div class="mb-3">
        <label>كلمة المرور</label>
        <input type="password" name="password" class="form-control" required>
      </div>
      <button class="btn btn-primary w-100">دخول</button>
    </form>
    <div class="mt-3 text-center">
      <a href="/signup" class="btn btn-link">إنشاء حساب جديد</a>
    </div>
  </div>
</body>
</html>
"""
signup_html = """
<!DOCTYPE html>
<html lang="ar" dir="rtl">
<head>
  <meta charset="utf-8"/>
  <title>تسجيل حساب جديد | الغدير</title>
  <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.2/dist/css/bootstrap.rtl.min.css" rel="stylesheet">
</head>
<body style="background:#f1f5f9;padding:40px">
  <div class="container" style="max-width:500px;background:white;padding:30px;border-radius:12px">
    <h3 class="text-center mb-4">تسجيل حساب جديد</h3>
    {% if error %}
      <div class="alert alert-danger text-center">{{ error }}</div>
    {% endif %}
    {% if success %}
      <div class="alert alert-success text-center">{{ success }}</div>
    {% endif %}
    <form method="post">
      <div class="mb-3">
        <label>اسم المستخدم</label>
        <input type="text" name="username" class="form-control" required>
      </div>
      <div class="mb-3">
        <label>كلمة المرور</label>
        <input type="password" name="password" class="form-control" required>
      </div>
      <button class="btn btn-success w-100">تسجيل</button>
    </form>
    <div class="mt-3 text-center">
      <a href="/" class="btn btn-link">العودة لتسجيل الدخول</a>
    </div>
  </div>
</body>
</html>
"""
settings_html = """
<!DOCTYPE html>
<html lang="ar" dir="rtl">
<head>
  <meta charset="utf-8"/>
  <title>إعدادات النظام | الغدير</title>
  <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.2/dist/css/bootstrap.rtl.min.css" rel="stylesheet">
</head>
<body style="background:#f8fafc;padding:40px">
  <div class="container" style="max-width:600px;background:white;padding:30px;border-radius:12px">
    <h3 class="mb-4 text-center">⚙️ إعدادات المسؤول</h3>
    <form method="post">
      <div class="mb-3">
        <label>عنوان النظام</label>
        <input type="text" name="system_name" class="form-control" value="{{ system_name }}">
      </div>
      <div class="mb-3">
        <label>الوصف العام</label>
        <textarea name="description" class="form-control" rows="3">{{ description }}</textarea>
      </div>
      <button class="btn btn-primary w-100">💾 حفظ التعديلات</button>
    </form>
    <div class="mt-4 text-center">
      <a href="/generate-pdf" class="btn btn-outline-success">⬇️ تحميل تقرير PDF</a>
    </div>
  </div>
</body>
</html>
"""

@app.route("/", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        user = request.form["username"]
        pw = request.form["password"]
        with get_conn() as conn:
            cur = conn.cursor()
            cur.execute("SELECT * FROM users WHERE username = %s AND password = %s", (user, pw))
            account = cur.fetchone()
            if account:
                return render_template_string(dashboard_html, user=user)
            else:
                return render_template_string(login_html, error="❌ اسم المستخدم أو كلمة المرور غير صحيحة.")
    return render_template_string(login_html)

@app.route("/signup", methods=["GET", "POST"])
def signup():
    if request.method == "POST":
        user = request.form["username"]
        pw = request.form["password"]
        with get_conn() as conn:
            try:
                cur = conn.cursor()
                cur.execute("INSERT INTO users (username, password) VALUES (%s, %s)", (user, pw))
                conn.commit()
                return render_template_string(signup_html, success="✅ تم إنشاء الحساب بنجاح.")
            except psycopg2.errors.UniqueViolation:
                return render_template_string(signup_html, error="⚠️ اسم المستخدم مستخدم بالفعل.")
            except Exception:
                return render_template_string(signup_html, error="⚠️ حصل خطأ أثناء التسجيل.")
    return render_template_string(signup_html)

@app.route("/settings", methods=["GET", "POST"])
def settings():
    system_name = "نظام الغدير"
    description = "إدارة لوجستية ذكية"
    if request.method == "POST":
        system_name = request.form.get("system_name", system_name)
        description = request.form.get("description", description)
    return render_template_string(settings_html, system_name=system_name, description=description)

@app.route("/generate-pdf")
def generate_pdf():
    pdf_path = "/mnt/data/ghadeer_admin_report.pdf"
    doc = SimpleDocTemplate(pdf_path)
    styles = getSampleStyleSheet()
    content = [
        Paragraph("تقرير نظام الغدير", styles["Title"]),
        Spacer(1, 12),
        Paragraph("هذا تقرير إداري يوضح إمكانيات التصدير بصيغة PDF.", styles["Normal"]),
        Spacer(1, 24),
        Paragraph("✅ تم الإنشاء بنجاح!", styles["Normal"]),
    ]
    doc.build(content)
    return send_file(pdf_path, as_attachment=True)

if __name__ == "__main__":
    app.run(debug=True)
