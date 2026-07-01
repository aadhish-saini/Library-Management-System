# Library Management System — Web Setup Guide

## Files You Got
- `app.py`     — Flask backend (connects to your MySQL database)
- `index.html` — The website frontend

## Step 1: Put Files in Your Project Folder
Copy BOTH files into the SAME folder where your existing Python files are:

```
Library-Management-System-main/
├── app.py          ← NEW (paste here)
├── index.html      ← NEW (paste here)
├── admin.py
├── books.py
├── members.py
├── issue_return.py
├── management_systems.py
├── file_creator.py
└── main.py
```

## Step 2: Install Flask
Open a terminal and run:
```
pip install flask mysql-connector-python
```

## Step 3: Check Your DB Password
Open app.py and find this line near the top:

    DB_CONFIG = dict(host="localhost", user="root", password="Aadhish20070", database="lib")

Change the password if needed. The database name lib should already match your project.

## Step 4: Run the Backend
```
cd Library-Management-System-main
python app.py
```

You should see:
```
📚 Library Management System API
   Running at  http://localhost:5000
```

## Step 5: Open the Website
Open your browser and go to:
    http://localhost:5000

That's it! The website will load and connect to your real MySQL database.

---

## Troubleshooting

Connection refused in browser:
  Make sure python app.py is running in your terminal.

Access denied for user root:
  Check your MySQL password in app.py → DB_CONFIG.

Table doesn't exist error:
  Make sure your MySQL lib database has tables: admin, books, members, issue_records

The status dot in the bottom-left shows red:
  The backend is not running. Go back to Step 4.
