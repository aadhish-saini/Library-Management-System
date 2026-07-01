"""Library Management System — Flask Backend"""

from flask import Flask, request, jsonify, send_from_directory
import mysql.connector as mc
from datetime import datetime, date

app = Flask(__name__, static_folder=".")


DB_CONFIG = dict(host="localhost", user="root", password="Aadhish20070", database="lib")


def get_db():
    """Open a fresh connection for every request (simple & safe)."""
    return mc.connect(**DB_CONFIG)


def row_to_dict(cursor, row):
    """Convert a DB row tuple → dict using cursor column names."""
    cols = [d[0] for d in cursor.description]
    return dict(zip(cols, [str(v) if isinstance(v, (datetime, date)) else v for v in row]))


def rows_to_list(cursor, rows):
    return [row_to_dict(cursor, r) for r in rows]



@app.after_request
def add_cors(response):
    response.headers["Access-Control-Allow-Origin"]  = "*"
    response.headers["Access-Control-Allow-Headers"] = "Content-Type"
    response.headers["Access-Control-Allow-Methods"] = "GET,POST,PUT,DELETE,OPTIONS"
    return response

@app.route("/<path:p>", methods=["OPTIONS"])
@app.route("/", methods=["OPTIONS"])
def options_handler(*args, **kwargs):
    return jsonify({}), 200


@app.route("/")
def index():
    return send_from_directory(".", "index.html")


@app.route("/api/login", methods=["POST"])
def api_login():
    data = request.json
    username = data.get("username", "")
    password = data.get("password", "")
    con = get_db(); cur = con.cursor()
    try:
        
        cur.execute(
            "SELECT full_name, role FROM admin WHERE username=%s AND password=%s",
            (username, password)
        )
        row = cur.fetchone()
        if not row:
            return jsonify({"error": "Invalid username or password"}), 401
        now = datetime.now()
        cur.execute(
            "UPDATE admin SET status='Active', last_login=%s WHERE username=%s AND password=%s",
            (now, username, password)
        )
        con.commit()
        return jsonify({"full_name": row[0], "role": row[1]})
    finally:
        cur.close(); con.close()


@app.route("/api/logout", methods=["POST"])
def api_logout():
    data = request.json
    username = data.get("username", "")
    password = data.get("password", "")
    con = get_db(); cur = con.cursor()
    try:
        cur.execute(
            "UPDATE admin SET status='Inactive' WHERE username=%s AND password=%s",
            (username, password)
        )
        con.commit()
        return jsonify({"ok": True})
    finally:
        cur.close(); con.close()



@app.route("/api/books", methods=["GET"])
def api_books_list():
    con = get_db(); cur = con.cursor()
    try:
        cur.execute("SELECT * FROM books")
        return jsonify(rows_to_list(cur, cur.fetchall()))
    finally:
        cur.close(); con.close()


@app.route("/api/books", methods=["POST"])
def api_books_add():
    d = request.json
    con = get_db(); cur = con.cursor()
    try:
        cur.execute(
            "INSERT INTO books(title,author,category,isbn,publisher,quantity,available_quantity) "
            "VALUES(%s,%s,%s,%s,%s,%s,%s)",
            (d["title"], d["author"], d["category"], d["isbn"],
             d["publisher"], d["quantity"], d["available_quantity"])
        )
        con.commit()
        return jsonify({"id": cur.lastrowid, "ok": True})
    finally:
        cur.close(); con.close()


@app.route("/api/books/<int:book_id>", methods=["PUT"])
def api_books_update(book_id):
    d = request.json
    con = get_db(); cur = con.cursor()
    try:
        cur.execute(
            "UPDATE books SET title=%s, author=%s, category=%s, isbn=%s, "
            "publisher=%s, quantity=%s, available_quantity=%s WHERE book_id=%s",
            (d["title"], d["author"], d["category"], d["isbn"],
             d["publisher"], d["quantity"], d["available_quantity"], book_id)
        )
        con.commit()
        return jsonify({"ok": True})
    finally:
        cur.close(); con.close()


@app.route("/api/books/<int:book_id>", methods=["DELETE"])
def api_books_delete(book_id):
    con = get_db(); cur = con.cursor()
    try:
        cur.execute("DELETE FROM books WHERE book_id=%s", (book_id,))
        con.commit()
        return jsonify({"ok": True})
    finally:
        cur.close(); con.close()



@app.route("/api/members", methods=["GET"])
def api_members_list():
    con = get_db(); cur = con.cursor()
    try:
        cur.execute("SELECT * FROM members")
        return jsonify(rows_to_list(cur, cur.fetchall()))
    finally:
        cur.close(); con.close()


@app.route("/api/members", methods=["POST"])
def api_members_add():
    d = request.json
    con = get_db(); cur = con.cursor()
    try:
        cur.execute(
            "INSERT INTO members(name,email,phone,course) VALUES(%s,%s,%s,%s)",
            (d["name"], d["email"], d["phone"], d["course"])
        )
        con.commit()
        return jsonify({"id": cur.lastrowid, "ok": True})
    finally:
        cur.close(); con.close()


@app.route("/api/members/<int:member_id>", methods=["PUT"])
def api_members_update(member_id):
    d = request.json
    con = get_db(); cur = con.cursor()
    try:
        cur.execute(
            "UPDATE members SET name=%s, email=%s, phone=%s, course=%s WHERE member_id=%s",
            (d["name"], d["email"], d["phone"], d["course"], member_id)
        )
        con.commit()
        return jsonify({"ok": True})
    finally:
        cur.close(); con.close()


@app.route("/api/members/<int:member_id>", methods=["DELETE"])
def api_members_delete(member_id):
    con = get_db(); cur = con.cursor()
    try:
        cur.execute("DELETE FROM members WHERE member_id=%s", (member_id,))
        con.commit()
        return jsonify({"ok": True})
    finally:
        cur.close(); con.close()



@app.route("/api/issues", methods=["GET"])
def api_issues_list():
    con = get_db(); cur = con.cursor()
    try:
        cur.execute("""
            SELECT i.issue_id, i.book_id, i.member_id,
                   m.name  AS member_name,
                   b.title AS book_title,
                   i.issue_date, i.due_date, i.return_date,
                   i.status, i.fine
            FROM issue_records i
            JOIN members m ON i.member_id = m.member_id
            JOIN books   b ON i.book_id   = b.book_id
            ORDER BY i.issue_id DESC
        """)
        return jsonify(rows_to_list(cur, cur.fetchall()))
    finally:
        cur.close(); con.close()


@app.route("/api/issues", methods=["POST"])
def api_issues_add():
    """Issue a book — mirrors issue_return.py::issue_book()"""
    d = request.json
    book_id   = int(d["book_id"])
    member_id = int(d["member_id"])
    issue_date = d.get("issue_date") or str(date.today())
    con = get_db(); cur = con.cursor()
    try:
        # Check availability
        cur.execute("SELECT available_quantity FROM books WHERE book_id=%s", (book_id,))
        row = cur.fetchone()
        if not row or row[0] < 1:
            return jsonify({"error": "Book not available"}), 400
        # Insert issue record
        cur.execute(
            "INSERT INTO issue_records(book_id, member_id, issue_date, status) VALUES(%s,%s,%s,'Issued')",
            (book_id, member_id, issue_date)
        )
        issue_id = cur.lastrowid

        cur.execute(
            "UPDATE issue_records SET due_date=DATE_ADD(issue_date, INTERVAL 14 DAY) WHERE issue_id=%s",
            (issue_id,)
        )

        cur.execute(
            "UPDATE books SET available_quantity=available_quantity-1 WHERE book_id=%s",
            (book_id,)
        )
        con.commit()
        return jsonify({"id": issue_id, "ok": True})
    finally:
        cur.close(); con.close()


@app.route("/api/issues/<int:issue_id>/return", methods=["POST"])
def api_issues_return(issue_id):
    """Return a book — mirrors management_systems.py return logic"""
    d = request.json
    return_date = d.get("return_date") or str(date.today())
    con = get_db(); cur = con.cursor()
    try:
        cur.execute("SELECT book_id, due_date FROM issue_records WHERE issue_id=%s", (issue_id,))
        row = cur.fetchone()
        if not row:
            return jsonify({"error": "Record not found"}), 404
        book_id, due_date = row[0], row[1]


        cur.execute(
            "UPDATE issue_records SET return_date=%s, status='Returned' WHERE issue_id=%s",
            (return_date, issue_id)
        )
        cur.execute(
            "SELECT DATEDIFF(return_date, due_date) FROM issue_records WHERE issue_id=%s",
            (issue_id,)
        )
        diff = cur.fetchone()[0] or 0
        fine  = max(0, diff * 5)
        cur.execute("UPDATE issue_records SET fine=%s WHERE issue_id=%s", (fine, issue_id))

        cur.execute(
            "UPDATE books SET available_quantity=available_quantity+1 WHERE book_id=%s",
            (book_id,)
        )
        con.commit()
        return jsonify({"ok": True, "fine": fine})
    finally:
        cur.close(); con.close()



@app.route("/api/dashboard", methods=["GET"])
def api_dashboard():
    con = get_db(); cur = con.cursor()
    try:
        def scalar(q):
            cur.execute(q); r = cur.fetchone(); return r[0] if r else 0

        total_books     = scalar("SELECT COUNT(book_id) FROM books")
        available_books = scalar("SELECT COUNT(book_id) FROM books WHERE quantity>0")
        issued_books    = scalar("SELECT COUNT(*) FROM issue_records WHERE status='Issued'")
        total_members   = scalar("SELECT COUNT(member_id) FROM members")
        overdue_books   = scalar("SELECT COUNT(*) FROM issue_records WHERE status='Overdue'")
        total_fines     = scalar("SELECT COALESCE(SUM(fine),0) FROM issue_records")

    
        cur.execute("""
            SELECT m.name, b.title, i.status, i.issue_date
            FROM issue_records i
            JOIN members m ON i.member_id=m.member_id
            JOIN books   b ON i.book_id=b.book_id
            ORDER BY i.issue_id DESC LIMIT 6
        """)
        activity = rows_to_list(cur, cur.fetchall())


        cur.execute("""
            SELECT m.name, b.title, i.due_date
            FROM issue_records i
            JOIN members m ON i.member_id=m.member_id
            JOIN books   b ON i.book_id=b.book_id
            WHERE i.status='Overdue'
        """)
        overdues = rows_to_list(cur, cur.fetchall())

        return jsonify({
            "total_books": total_books,
            "available_books": available_books,
            "issued_books": issued_books,
            "total_members": total_members,
            "overdue_books": overdue_books,
            "total_fines": float(total_fines) if total_fines else 0,
            "activity": activity,
            "overdues": overdues,
        })
    finally:
        cur.close(); con.close()



@app.route("/api/reports/most-borrowed", methods=["GET"])
def api_most_borrowed():
    con = get_db(); cur = con.cursor()
    try:
        cur.execute("""
            SELECT b.book_id, b.title, COUNT(i.book_id) AS times_borrowed
            FROM books b
            JOIN issue_records i ON b.book_id=i.book_id
            GROUP BY b.book_id, b.title
            ORDER BY times_borrowed DESC
        """)
        return jsonify(rows_to_list(cur, cur.fetchall()))
    finally:
        cur.close(); con.close()


@app.route("/api/reports/fines", methods=["GET"])
def api_fines():
    con = get_db(); cur = con.cursor()
    try:
        cur.execute("""
            SELECT i.issue_id, m.name, i.fine
            FROM issue_records i
            JOIN members m ON i.member_id=m.member_id
            WHERE i.fine > 0
        """)
        return jsonify(rows_to_list(cur, cur.fetchall()))
    finally:
        cur.close(); con.close()


@app.route("/api/reports/member-summary", methods=["GET"])
def api_member_summary():
    con = get_db(); cur = con.cursor()
    try:
        cur.execute("""
            SELECT m.member_id, m.name, m.email, m.phone, m.course,
                   COUNT(i.issue_id) AS books_issued
            FROM members m
            LEFT JOIN issue_records i ON m.member_id=i.member_id
            GROUP BY m.member_id, m.name, m.email, m.phone, m.course
        """)
        return jsonify(rows_to_list(cur, cur.fetchall()))
    finally:
        cur.close(); con.close()


@app.route("/api/admins", methods=["GET"])
def api_admins_list():
    con = get_db(); cur = con.cursor()
    try:
        cur.execute("SELECT admin_id, username, full_name, email, role, status, last_login FROM admin")
        return jsonify(rows_to_list(cur, cur.fetchall()))
    finally:
        cur.close(); con.close()


@app.route("/api/admins", methods=["POST"])
def api_admins_add():
    d = request.json
    con = get_db(); cur = con.cursor()
    try:
        cur.execute(
            "INSERT INTO admin(username,password,full_name,email,role) VALUES(%s,%s,%s,%s,%s)",
            (d["username"], d["password"], d["full_name"], d["email"], d["role"])
        )
        con.commit()
        return jsonify({"id": cur.lastrowid, "ok": True})
    finally:
        cur.close(); con.close()


@app.route("/api/admins/<int:admin_id>", methods=["DELETE"])
def api_admins_delete(admin_id):
    con = get_db(); cur = con.cursor()
    try:
        cur.execute("DELETE FROM admin WHERE admin_id=%s", (admin_id,))
        con.commit()
        return jsonify({"ok": True})
    finally:
        cur.close(); con.close()




app.run(debug=True, port=5000)
