from datetime import datetime, timedelta
from functools import wraps
import io
import os
import sqlite3

from flask import (
    Flask,
    flash,
    redirect,
    render_template,
    request,
    send_file,
    session,
    url_for,
)
app = Flask(__name__)
import openpyxl
from openpyxl.styles import Alignment, Font, PatternFill
from werkzeug.security import check_password_hash, generate_password_hash

def admin_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if session.get('role') != 'admin':
            flash('غير مصرح لك بالوصول إلى هذه الصفحة', 'danger')
            return redirect(url_for('staff_dashboard'))
        return f(*args, **kwargs)
    return decorated_function


@app.route("/admin/staff/create", methods=["POST"])
@admin_required
def create_staff():
    full_name = request.form.get("full_name", "").strip()
    username = request.form.get("username", "").strip()
    password = request.form.get("password", "").strip()
    role = request.form.get("role", "staff").strip()

    if not all([full_name, username, password]) or role not in ("admin", "staff"):
        flash("يرجى ملء جميع الحقول بشكل صحيح", "danger")
        return redirect(url_for("staff_dashboard"))

    password_hash = generate_password_hash(password, method="scrypt")
    conn = get_db()
    try:
        conn.execute(
            """
            INSERT INTO staff (full_name, username, password_hash, role, is_active)
            VALUES (?, ?, ?, ?, 1)
            """,
            (full_name, username, password_hash, role)
        )
        conn.commit()
        flash(f"تم إنشاء حساب {full_name} بنجاح", "success")
    except sqlite3.IntegrityError:
        flash("اسم المستخدم موجود مسبقاً، اختر اسماً آخر", "danger")
    finally:
        conn.close()

    return redirect(url_for("staff_dashboard"))


@app.route("/admin/staff/update/<int:staff_id>", methods=["POST"])
@admin_required
def update_staff_credentials(staff_id):
    new_username = request.form.get("username", "").strip()
    new_password = request.form.get("password", "").strip()
    new_full_name = request.form.get("full_name", "").strip()

    if not new_username:
        flash("اسم المستخدم لا يمكن أن يكون فارغاً", "danger")
        return redirect(url_for("staff_dashboard"))

    conn = get_db()
    try:
        if new_password:
            password_hash = generate_password_hash(new_password, method="scrypt")
            if new_full_name:
                conn.execute("""
                    UPDATE staff
                    SET full_name = ?, username = ?, password_hash = ?
                    WHERE id = ?
                """, (new_full_name, new_username, password_hash, staff_id))
            else:
                conn.execute("""
                    UPDATE staff
                    SET username = ?, password_hash = ?
                    WHERE id = ?
                """, (new_username, password_hash, staff_id))
        else:
            if new_full_name:
                conn.execute("""
                    UPDATE staff
                    SET full_name = ?, username = ?
                    WHERE id = ?
                """, (new_full_name, new_username, staff_id))
            else:
                conn.execute("""
                    UPDATE staff
                    SET username = ?
                    WHERE id = ?
                """, (new_username, staff_id))
        conn.commit()

        if session.get("staff_id") == staff_id:
            session["username"] = new_username

        flash("تم تحديث بيانات الحساب بنجاح", "success")
    except sqlite3.IntegrityError:
        flash("اسم المستخدم مستخدم لحساب آخر", "danger")
    finally:
        conn.close()

    return redirect(url_for("staff_dashboard"))

    new_username = request.form.get("username", "").strip()
    new_password = request.form.get("password", "").strip()
    new_full_name = request.form.get("full_name", "").strip()

    if not new_username:
        flash("اسم المستخدم لا يمكن أن يكون فارغاً", "danger")
        return redirect(url_for("staff_dashboard"))

    conn = get_db()
    try:
        if new_password:
            password_hash = generate_password_hash(new_password, method="scrypt")
            if new_full_name:
                conn.execute("""
                    UPDATE staff
                    SET full_name = ?, username = ?, password_hash = ?
                    WHERE id = ?
                """, (new_full_name, new_username, password_hash, staff_id))
            else:
                conn.execute("""
                    UPDATE staff
                    SET username = ?, password_hash = ?
                    WHERE id = ?
                """, (new_username, password_hash, staff_id))
        else:
            if new_full_name:
                conn.execute("""
                    UPDATE staff
                    SET full_name = ?, username = ?
                    WHERE id = ?
                """, (new_full_name, new_username, staff_id))
            else:
                conn.execute("""
                    UPDATE staff
                    SET username = ?
                    WHERE id = ?
                """, (new_username, staff_id))
        conn.commit()

        if session.get("staff_id") == staff_id:
            session["username"] = new_username

        flash("تم تحديث بيانات الحساب بنجاح", "success")
    except sqlite3.IntegrityError:
        flash("اسم المستخدم مستخدم لحساب آخر", "danger")
    finally:
        conn.close()

    return redirect(url_for("staff_dashboard"))
    full_name = request.form.get("full_name", "").strip()
    username = request.form.get("username", "").strip()
    password = request.form.get("password", "").strip()
    role = request.form.get("role", "staff").strip()

    if not all([full_name, username, password]) or role not in ("admin", "staff"):
        flash("يرجى ملء جميع الحقول بشكل صحيح", "danger")
        return redirect(url_for("staff_dashboard"))

    password_hash = generate_password_hash(password, method="scrypt")
    conn = get_db()
    try:
        conn.execute(
            """
            INSERT INTO staff (full_name, username, password_hash, role, is_active)
            VALUES (?, ?, ?, ?, 1)
            """,
            (full_name, username, password_hash, role)
        )
        conn.commit()
        flash(f"تم إنشاء حساب {full_name} بنجاح", "success")
    except sqlite3.IntegrityError:
        flash("اسم المستخدم موجود مسبقاً، اختر اسماً آخر", "danger")
    finally:
        conn.close()

    return redirect(url_for("staff_dashboard"))

def admin_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if session.get('role') != 'admin':
            flash('غير مصرح لك بالوصول إلى هذه الصفحة', 'danger')
            return redirect(url_for('staff_dashboard'))
        return f(*args, **kwargs)
    return decorated_function

app = Flask(__name__)
app.secret_key = os.environ.get("SECRET_KEY", "dorm-secret-key-2026")
app.config['PERMANENT_SESSION_LIFETIME'] = timedelta(days=210)

DB_PATH = "dorm_system.db"

MOVEMENT_TYPES = ["نزول للأسواق", "للأهل", "للمدينة"]
STUDENT_STATUSES = ["نشط", "موقوف", "مغادر"]


def get_db():
  conn = sqlite3.connect(DB_PATH)
  conn.row_factory = sqlite3.Row
  conn.execute("PRAGMA foreign_keys = ON")
  return conn

@app.route('/scan_rfid', methods=['POST'])
def scan_rfid():
    card_uid = request.form.get('card_uid')
    conn = get_db()
    cur = conn.cursor()
    student = cur.execute('SELECT id FROM students WHERE card_uid = ?', (card_uid,)).fetchone()
    
    if student:
        student_id = student['id']
        last_move = cur.execute('SELECT movement_type FROM movements WHERE student_id = ? ORDER BY id DESC LIMIT 1', (student_id,)).fetchone()
        new_type = 'خروج' if last_move and last_move['movement_type'] == 'دخول' else 'دخول'
        
        cur.execute('INSERT INTO movements (student_id, movement_type) VALUES (?, ?)', (student_id, new_type))
        conn.commit()
        return {'status': 'success', 'message': f'تم تسجيل {new_type}'}
    return {'status': 'error', 'message': 'الطالب غير موجود'}, 404

def init_db():
  conn = get_db()
  cur = conn.cursor()

  cur.executescript("""
        -- 1. جدول الطلاب
        CREATE TABLE IF NOT EXISTS students (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            full_name TEXT NOT NULL,
            card_uid TEXT UNIQUE NOT NULL,
            phone TEXT NOT NULL,
            department TEXT NOT NULL,
            status TEXT NOT NULL DEFAULT 'نشط' CHECK(status IN ('نشط', 'موقوف', 'مغادر'))
        );

        -- 2. جدول الموظفين لإدارة الصلاحيات
        CREATE TABLE IF NOT EXISTS staff (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            full_name TEXT NOT NULL,
            username TEXT UNIQUE NOT NULL,
            password_hash TEXT NOT NULL,
            role TEXT NOT NULL DEFAULT 'staff' CHECK(role IN ('admin', 'staff')),
            is_active INTEGER NOT NULL DEFAULT 1
        );

        -- 3. جدول الحركات
        CREATE TABLE IF NOT EXISTS movements (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            student_id INTEGER NOT NULL,
            staff_id INTEGER NOT NULL,
            staff_name TEXT NOT NULL,
            movement_type TEXT NOT NULL CHECK(movement_type IN ('نزول للأسواق', 'للأهل', 'للمدينة')),
            movement_date TEXT NOT NULL,
            movement_time TEXT NOT NULL,
            notes TEXT,
            updated_at TEXT,
            FOREIGN KEY (student_id) REFERENCES students(id) ON DELETE CASCADE,
            FOREIGN KEY (staff_id) REFERENCES staff(id) ON DELETE RESTRICT
        );
        """)

  # حسابات أولية تجريبية إذا كانت الجداول فارغة
  if cur.execute("SELECT COUNT(*) FROM staff").fetchone()[0] == 0:
    cur.executemany(
        """
            INSERT INTO staff (full_name, username, password_hash, role, is_active)
            VALUES (?, ?, ?, ?, ?)
            """,
        [
            (
                "أحمد المسؤول",
                "admin",
                generate_password_hash("Admin@123"),
                "admin",
                1,
            ),
            (
                "علي مشرف الحركة",
                "staff1",
                generate_password_hash("Staff@123"),
                "staff",
                1,
            ),
        ],
    )

  if cur.execute("SELECT COUNT(*) FROM students").fetchone()[0] == 0:
    cur.executemany(
        """
            INSERT INTO students (full_name, card_uid, phone, department, status)
            VALUES (?, ?, ?, ?, ?)
            """,
        [
            (
                "مصطفى كريم",
                "CARD-1001",
                "07700000001",
                "تقنيات الأمن السيبراني",
                "نشط",
            ),
            (
                "زينب حسن",
                "CARD-1002",
                "07800000002",
                "هندسة تقنيات الحاسوب",
                "نشط",
            ),
            (
                "كرار محمد",
                "CARD-1003",
                "07500000003",
                "علوم الحاسوب",
                "نشط",
            ),
        ],
    )

  conn.commit()
  conn.close()


# --- صلاحيات الوصول ---
def staff_required(role=None):

  def decorator(fn):

    @wraps(fn)
    def wrapper(*args, **kwargs):
      if "staff_id" not in session:
        flash("يرجى تسجيل الدخول بحساب موظف أولاً.", "warning")
        return redirect(url_for("staff_login"))
      if (
          role
          and session.get("staff_role") != role
          and session.get("staff_role") != "admin"
      ):
        flash("تحتاج إلى صلاحية مدير للوصول إلى هذا القسم.", "danger")
        return redirect(url_for("staff_dashboard"))
      return fn(*args, **kwargs)

    return wrapper

  return decorator


def student_required(fn):

  @wraps(fn)
  def wrapper(*args, **kwargs):
    if "student_id" not in session:
      flash("يرجى إدخال المعرف الفريد للبطاقة للدخول.", "warning")
      return redirect(url_for("student_login"))
    return fn(*args, **kwargs)

  return wrapper


# --- الصفحة الرئيسية ---
@app.route("/")
def index():
  return render_template("index.html")


# --- بوابة دخول الطالب وعرض حركاته ---
@app.route("/student/login", methods=["GET", "POST"])
def student_login():
  if request.method == "POST":
    card_uid = request.form.get("card_uid", "").strip().upper()
    conn = get_db()
    student = conn.execute(
        "SELECT * FROM students WHERE UPPER(card_uid) = ?", (card_uid,)
    ).fetchone()
    conn.close()

    if not student:
      flash("المعرف الفريد للبطاقة غير مسجل في النظام.", "danger")
      return render_template("student_login.html")

    if student["status"] != "نشط":
      flash(
          f"حالة البطاقة الحالية: ({student['status']}) — لا يُسمح بالدخول.",
          "warning",
      )
      return render_template("student_login.html")

    session.clear()
    session["student_id"] = student["id"]
    session["student_name"] = student["full_name"]
    session["card_uid"] = student["card_uid"]
    flash(f"أهلاً بك {student['full_name']}", "success")
    session.permanent = True
    return redirect(url_for("student_portal"))

  return render_template("student_login.html")


@app.route("/student/portal")
@student_required
def student_portal():
  conn = get_db()
  student = conn.execute(
      "SELECT * FROM students WHERE id = ?", (session["student_id"],)
  ).fetchone()
  movements = conn.execute(
      """
        SELECT * FROM movements
        WHERE student_id = ?
        ORDER BY movement_date DESC, movement_time DESC, id DESC
        """,
      (session["student_id"],),
  ).fetchall()
  conn.close()
  return render_template(
      "student_portal.html", student=student, movements=movements
  )


# --- بوابة دخول الموظف ولوحة التحكم ---
@app.route("/staff/login", methods=["GET", "POST"])
def staff_login():
  if request.method == "POST":
    username = request.form.get("username", "").strip()
    password = request.form.get("password", "")

    conn = get_db()
    user = conn.execute(
        "SELECT * FROM staff WHERE username = ? AND is_active = 1", (username,)
    ).fetchone()
    conn.close()

    if user and check_password_hash(user["password_hash"], password):
      session.clear()
      session["staff_id"] = user["id"]
      session["staff_name"] = user["full_name"]
      session["staff_role"] = user["role"]
      flash(
          f"مرحباً {user['full_name']} ({'مدير' if user['role'] == 'admin' else 'موظف'})",
          "success",
      )
      return redirect(url_for("staff_dashboard"))

    flash("بيانات الدخول غير صحيحة أو الحساب معطّل.", "danger")

  return render_template("staff_login.html")


@app.route("/staff/dashboard", methods=["GET", "POST"])
@staff_required()
def staff_dashboard():
  conn = get_db()

  # تسجيل حركة جديدة من لوحة تحكم الموظف
  if request.method == "POST":
    card_uid = request.form.get("card_uid", "").strip().upper()
    movement_type = request.form.get("movement_type", "").strip()
    notes = request.form.get("notes", "").strip()

    # التاريخ والوقت المضبوطان تلقائياً وقت التسجيل (أو مخصص إذا أُدخل)
    now = datetime.now()
    movement_date = (
        request.form.get("movement_date") or now.strftime("%Y-%m-%d")
    ).strip()
    movement_time = (
        request.form.get("movement_time") or now.strftime("%H:%M:%S")
    ).strip()

    student = conn.execute(
        "SELECT id, full_name, status FROM students WHERE UPPER(card_uid) = ?",
        (card_uid,),
    ).fetchone()

    if not student:
      flash("لم يتم العثور على طالب بهذا المعرف الفريد للبطاقة.", "danger")
    elif student["status"] != "نشط":
      flash(
          f"لا يمكن تسجيل حركة للطالب لأن حالته ({student['status']}).",
          "warning",
      )
    elif movement_type not in MOVEMENT_TYPES:
      flash("نوع الحركة غير صحيح.", "danger")
    else:
      conn.execute(
          """
                INSERT INTO movements
                    (student_id, staff_id, staff_name, movement_type, movement_date, movement_time, notes)
                VALUES (?, ?, ?, ?, ?, ?, ?)
                """,
          (
              student["id"],
              session["staff_id"],
              session["staff_name"],
              movement_type,
              movement_date,
              movement_time,
              notes,
          ),
      )
      conn.commit()
      flash(
          f"تم تسجيل حركة ({movement_type}) للطالب {student['full_name']} الساعة"
          f" {movement_time}.",
          "success",
      )
    return redirect(url_for("staff_dashboard"))

  selected_date = request.args.get("date", datetime.now().strftime("%Y-%m-%d"))
  movements = conn.execute(
      """
        SELECT m.*, s.full_name AS student_name, s.card_uid, s.department, s.phone
        FROM movements m
        JOIN students s ON m.student_id = s.id
        WHERE m.movement_date = ?
        ORDER BY m.movement_time DESC, m.id DESC
        """,
      (selected_date,),
  ).fetchall()

  students = conn.execute(
      "SELECT * FROM students ORDER BY full_name ASC"
  ).fetchall()
  staff_list = (
      conn.execute(
          "SELECT id, full_name, username, role, is_active FROM staff ORDER BY"
          " id ASC"
      ).fetchall()
      if session.get("staff_role") == "admin"
      else []
  )

  conn.close()
  return render_template(
      "staff_dashboard.html",
      movements=movements,
      movement_types=MOVEMENT_TYPES,
      selected_date=selected_date,
      students=students,
      staff_list=staff_list,
  )


# --- تعديل حركة قائمة ---
@app.route("/staff/movements/<int:movement_id>/edit", methods=["POST"])
@staff_required()
def edit_movement(movement_id):
  movement_type = request.form.get("movement_type", "").strip()
  movement_date = request.form.get("movement_date", "").strip()
  movement_time = request.form.get("movement_time", "").strip()
  notes = request.form.get("notes", "").strip()

  if movement_type not in MOVEMENT_TYPES:
    flash("نوع الحركة غير صالح.", "danger")
    return redirect(url_for("staff_dashboard", date=movement_date))

  conn = get_db()
  existing = conn.execute(
      "SELECT * FROM movements WHERE id = ?", (movement_id,)
  ).fetchone()
  if not existing:
    conn.close()
    flash("الحركة غير موجودة.", "danger")
    return redirect(url_for("staff_dashboard"))

  # الموظف العادي يعدّل حركاته أو أي حركة حسب سياسة القسم؛ هنا نحدّث اسم الموظف المعدِّل وتاريخ التعديل
  updated_at = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
  conn.execute(
      """
        UPDATE movements
        SET movement_type = ?,
            movement_date = ?,
            movement_time = ?,
            notes = ?,
            staff_id = ?,
            staff_name = ?,
            updated_at = ?
        WHERE id = ?
        """,
      (
          movement_type,
          movement_date,
          movement_time,
          notes,
          session["staff_id"],
          session["staff_name"],
          updated_at,
          movement_id,
      ),
  )
  conn.commit()
  conn.close()
  flash("تم تعديل بيانات الحركة بنجاح.", "success")
  return redirect(url_for("staff_dashboard", date=movement_date))


# --- إضافة طالب جديد (للموظفين/المدير) ---
@app.route("/staff/students/add", methods=["POST"])
@staff_required()
def add_student():
    full_name = request.form.get("full_name", "").strip()
    card_uid = request.form.get("card_uid", "").strip().upper()
    phone = request.form.get("phone", "").strip()
    department = request.form.get("department", "").strip()
    status = request.form.get("status", "").strip()
    username = request.form.get("username", "").strip()
    password = request.form.get("password", "").strip()

    if (
        not all([full_name, card_uid, phone, department, username, password])
        or status not in STUDENT_STATUSES
    ):
        flash("يرجى ملء جميع حقول الطالب بشكل صحيح", "danger")
        return redirect(url_for("staff_dashboard"))

    conn = get_db()
    try:
        conn.execute(
            """
            INSERT INTO students (full_name, card_uid, phone, department, status, username, password)
            VALUES (?, ?, ?, ?, ?, ?, ?)
        """,
            (full_name, card_uid, phone, department, status, username, password),
        )
        conn.commit()
    except Exception as e:
        flash("خطأ في إضافة الطالب", "danger")
    finally:
        conn.close()

    return redirect(url_for("staff_dashboard"))
# --- إضافة موظف وإدارة الصلاحيات (للمدير فقط) ---
@app.route("/staff/users/add", methods=["POST"])
@staff_required(role="admin")
def add_staff():
  full_name = request.form.get("full_name", "").strip()
  username = request.form.get("username", "").strip()
  password = request.form.get("password", "").strip()
  role = request.form.get("role", "staff").strip()

  if (
      not all([full_name, username, password])
      or len(password) < 6
      or role not in ("admin", "staff")
  ):
    flash(
        "بيانات الموظف غير مكتملة أو كلمة المرور أقل من 6 أحرف.", "danger"
    )
    return redirect(url_for("staff_dashboard"))

  conn = get_db()
  try:
    conn.execute(
        """
            INSERT INTO staff (full_name, username, password_hash, role, is_active)
            VALUES (?, ?, ?, ?, 1)
            """,
        (full_name, username, generate_password_hash(password), role),
    )
    conn.commit()
    flash(f"تم إنشاء حساب الموظف ({full_name}) بصلاحية ({role}).", "success")
  except sqlite3.IntegrityError:
    flash("اسم المستخدم موجود مسبقاً.", "danger")
  finally:
    conn.close()

  return redirect(url_for("staff_dashboard"))


# --- تصدير التقرير اليومي بصيغة Excel (.xlsx) ---
@app.route("/staff/export/daily-excel")
@staff_required()
def export_daily_excel():
  selected_date = request.args.get("date", datetime.now().strftime("%Y-%m-%d"))

  conn = get_db()
  rows = conn.execute(
      """
        SELECT
            m.id,
            s.full_name AS student_name,
            s.card_uid,
            s.department,
            s.phone,
            m.movement_type,
            m.movement_date,
            m.movement_time,
            m.staff_name,
            COALESCE(m.notes, '') AS notes
        FROM movements m
        JOIN students s ON m.student_id = s.id
        WHERE m.movement_date = ?
        ORDER BY m.movement_time ASC, m.id ASC
        """,
      (selected_date,),
  ).fetchall()
  conn.close()

  wb = openpyxl.Workbook()
  ws = wb.active
  ws.title = f"حركات {selected_date}"
  ws.sheet_view.rightToLeft = True

  headers = [
      "ت",
      "اسم الطالب",
      "المعرف الفريد للبطاقة",
      "القسم العلمي",
      "رقم الهاتف",
      "نوع الحركة",
      "التاريخ",
      "الوقت المضبوط",
      "الموظف المسؤول",
      "ملاحظات",
  ]
  ws.append(headers)

  header_fill = PatternFill(
      start_color="1F4E78", end_color="1F4E78", fill_type="solid"
  )
  header_font = Font(color="FFFFFF", bold=True, size=11)

  for col_idx in range(1, len(headers) + 1):
    cell = ws.cell(row=1, column=col_idx)
    cell.fill = header_fill
    cell.font = header_font
    cell.alignment = Alignment(horizontal="center", vertical="center")

  for idx, r in enumerate(rows, start=1):
    ws.append([
        idx,
        r["student_name"],
        r["card_uid"],
        r["department"],
        r["phone"],
        r["movement_type"],
        r["movement_date"],
        r["movement_time"],
        r["staff_name"],
        r["notes"],
    ])

  # ضبط عرض الأعمدة تلقائياً
  for col in ws.columns:
    max_len = max(
        len(str(cell.value or "")) for cell in col
    )
    col_letter = openpyxl.utils.get_column_letter(col[0].column)
    ws.column_dimensions[col_letter].width = max(max_len + 5, 14)

  output = io.BytesIO()
  wb.save(output)
  output.seek(0)

  filename = f"daily_movements_{selected_date}.xlsx"
  return send_file(
      output,
      as_attachment=True,
      download_name=filename,
      mimetype=(
          "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
      ),
  )


@app.route("/logout")
def logout():
  session.clear()
  flash("تم تسجيل الخروج بنجاح.", "info")
  return redirect(url_for("index"))


if __name__ == "__main__":
  init_db()
  app.run(debug=True)