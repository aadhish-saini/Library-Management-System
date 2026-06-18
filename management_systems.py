import mysql.connector as c
from datetime import datetime
from members import add_new,view_all_member,search_member,update_member,delete_member,view_issued_book
from books import add_new_book,view_all_books,search_book,update_book,delete_book,check_book_availability
from issue_return import issue_book,return_book,view_issued_records,view_overdue_records,member_issue_history,book_issue_history
from file_creator import write_txt
from admin import main_login,add_admin,view_all_admins,search_admin,update_admin,delete_admin,view_last_login

con = c.connect(
    host = 'localhost',
    user = 'root',
    password = 'Aadhish20070',
    database = 'lib'
)

cursor = con.cursor()


def issued_books_function():
    cursor.execute("""SELECT
    i.issue_id,
    m.name,
    b.title
    FROM issue_records i
    JOIN books b
    ON i.book_id = b.book_id
    JOIN members m
    ON i.member_id = m.member_id;""")
    records = cursor.fetchall()
    data = []
    for row in records:
        details = [row[0],row[1],row[2]]
        data.append(details)
    return data

def members():
    cursor.execute("SELECT * FROM members")
    records = cursor.fetchall()
    
    data = []
    for row in records:
        details=(row[0],row[1],row[2],row[3],row[4],str(row[5]))
        data.append(details)
    return data

def fine():
    cursor.execute("""SELECT
    i.issue_id,
    m.name,
    i.fine
    FROM issue_records i
    JOIN members m
    ON i.member_id = m.member_id""")
    records = cursor.fetchall()
    data = []
    for row in records:
        details = [row[0],row[1],row[2]]
        data.append(details)
    return data


def login(username,password):
    cursor.execute(main_login(username,password))
    records = cursor.fetchone()
    cursor.execute("UPDATE admin SET status='Active' where username='{}' and password='{}'".format(username,password))
    now = datetime.now()
    cursor.execute(
        "UPDATE admin SET last_login='{}' WHERE username='{}' AND password='{}'".format(now,username,password)
        )
    con.commit()
    return records

def inactive_status(username,password):
    cursor.execute("UPDATE admin SET status='Inactive' WHERE username='{}' and password='{}'".format(username,password))
    con.commit()


def admin_management():
    while True:
        print("***********************************")
        print("       ADMIN MANAGEMENT SYSTEM      ")
        print("***********************************")
        print("1. Add New Admin")
        print("2. View All Admins")
        print("3. Search Admin")
        print("4. Update Admin Details")
        print("5. Delete Admin")
        print("6. View Last Login")
        print("7. Back")
        print("***********************************")
        try:
            choice = int(input("Enter your choice: "))
        except ValueError:
            print("Invalid Input")
        if choice==1:
            cursor.execute(add_admin())
            con.commit()
            print("***** Admin Added *****")
            input("Press 'Enter' to continue.......")
        elif choice==2:
            cursor.execute(view_all_admins())
            records = cursor.fetchall()
            print(f"{'Admin ID':<20}{'Username':<30}{'Full Name':<30}{'Role':<30}")
            for row in records:
                print(f"{row[0]:<20}{row[1]:<30}{row[2]:<30}{row[3]:<30}")
            con.commit()
            input("Press 'Enter' to continue.......")
        elif choice==3:
            cursor.execute(search_admin())
            records = cursor.fetchall()
            print(f"{'Admin ID':<20}{'Full Name':<30}{'Role':<30}")
            for row in records:
                print(f"{row[0]:<20}{row[1]:<30}{row[2]:<30}")
            con.commit()
            input("Press 'Enter' to continue.......")
        elif choice==4:
            cursor.execute(update_admin())
            con.commit()
            print("***** Admin Updated *****")
            input("Press 'Enter' to continue.......")
        elif choice==5:
            cursor.execute(delete_admin())
            con.commit()
            print("***** Admin Deleted *****")
            input("Press 'Enter' to continue.......")
        elif choice==6:
            cursor.execute(view_last_login())
            records = cursor.fetchall()
            print(f"{'Admin ID':<20}{'Username':<30}{'Role':<30}{'Last Login':<30}")
            for row in records:
                print(f"{row[0]:<20}{row[1]:<30}{row[2]:<30}{str(row[3]):<30}")
            con.commit()
            input("Press 'Enter' to continue.......")
        elif choice==7:
            break
        else:
            print("!!!!!!! INVALID INPUT !!!!!!!")

def book_management():
    while True:
        print("***********************************")
        print("       BOOK MANAGEMENT SYSTEM      ")
        print("***********************************")
        print("1. Add New Book")
        print("2. View All Books")
        print("3. Search Book")
        print("4. Update Book Details")
        print("5. Delete Book")
        print("6. Check Book Availability")
        print("7. Back")
        print("***********************************")
        try:
            choice = int(input("Enter your choice: "))
        except ValueError:
            print("Invalid Input")
        if choice==1:
            cursor.execute(add_new_book())
            con.commit()
            print("****BOOK ADDED****")
            input("Press 'Enter' to continue.......")
        
        elif choice==2:
            cursor.execute(view_all_books())
            records = cursor.fetchall()
            for rows in records:
                print(rows)
            con.commit()
            input("Press 'Enter' to continue.......")
        
        elif choice==3:
            cursor.execute(search_book())
            records = cursor.fetchall()
            for rows in records:
                print(rows)
            con.commit()
            input("Press 'Enter' to continue.......")
        elif choice==4:
            cursor.execute(update_book())
            con.commit()
            print("****BOOK UPDATED****")
            input("Press 'Enter' to continue.......")
        elif choice==5:
            cursor.execute(delete_book())
            con.commit()
            print("****BOOK DELETED****")
            input("Press 'Enter' to continue.......")
        elif choice==6:
            cursor.execute(check_book_availability())
            records = cursor.fetchall()
            for row in records:
                a = row[0]
            if a>0:
                print("Book Available")
            else:
                print("Not Available")    
            con.commit()
            input("Press 'Enter' to continue.......")
        elif choice==7:
            break
        else:
            print("!!!!!!! INVALID INPUT !!!!!!!")

def members_management():
    while True:
        print("***********************************")
        print("    MEMBERS MANAGEMENT SYSTEM      ")
        print("***********************************")
        print("1. Add New Member")
        print("2. View All Member")
        print("3. Search Member")
        print("4. Update Member Details")
        print("5. Delete Member")
        print("6. View Issued Book of Member")
        print("7. Back")
        print("***********************************")
        try:
            choice = int(input("Enter your choice: "))
        except ValueError:
            print("Invalid Input")

        if choice==1:
            cursor.execute(add_new())
            con.commit()
            print("*****Member Added*****")
            input("Press 'Enter' to continue.......")
        elif choice==2:
            cursor.execute(view_all_member())
            records = cursor.fetchall()
            for row in records:
                print(row)
            con.commit()
            input("Press 'Enter' to continue.......")
        elif choice==3:
            cursor.execute(search_member())
            records = cursor.fetchall()
            for row in records:
                print(row)
            con.commit()
            input("Press 'Enter' to continue.......")
        elif choice==4:
            cursor.execute(update_member())
            con.commit()
            print("****MEMBER UPDATED****")
            input("Press 'Enter' to continue.......")
        elif choice==5:
            cursor.execute(delete_member())
            con.commit()
            print("****MEMBER DELETED****")
            input("Press 'Enter' to continue.......")
        elif choice==6:
            cursor.execute(view_issued_book())
            records = cursor.fetchall()
            for row in records:
                print(row)
            con.commit()
            input("Press 'Enter' to continue.......")
        elif choice==7:
            break
        else:
            print("!!!!!!! INVALID INPUT !!!!!!!")

def issue_return_manager():
    while True:
        print("***********************************")
        print("       Issue/Return Manager      ")
        print("***********************************")
        print("1. Issue Book")
        print("2. Return Books")
        print("3. View Issued Books")
        print("4. View Overdue Books")
        print("5. Member Issue History")
        print("6. Book Issue History")
        print("7. Back")
        print("***********************************")
        try:
            choice = int(input("Enter your choice: "))
        except ValueError:
            print("Invalid Input")
        if choice==1:
            book_id = int(input("Enter book_id: "))
            cursor.execute("SELECT (available_quantity) FROM books WHERE book_id={}".format(book_id))
            records = cursor.fetchall()
            for row in records:
                a=row
            if a==0:
                print("BOOK NOT AVAILABLE")
                input("Press 'Enter' to continue.......")
            else:
                member_id = int(input("Enter member_id: "))
                cursor.execute(issue_book(book_id,member_id))
                cursor.execute("""UPDATE issue_records
                    SET due_date=DATE_ADD(issue_date, INTERVAL 14 DAY)
                    WHERE book_id ={}""".format(book_id))
                print("*****BOOK ISSUED*****")
                cursor.execute("UPDATE books SET available_quantity=available_quantity-1 WHERE book_id={}".format(book_id))
                con.commit()
                input("Press 'Enter' to continue.......")
        
        elif choice==2:
            member_id = int(input("Enter member_id: "))
            book_id = int(input("Enter book_id: "))
            date = input("Enter return_date: ")

            cursor.execute(return_book(date, book_id, member_id))

            cursor.execute("""UPDATE issue_records
            SET status='Returned'
            WHERE member_id={} and book_id={}""".format(member_id, book_id))

            cursor.execute("""
            SELECT DATEDIFF(return_date, due_date)
            FROM issue_records
            WHERE member_id={} and book_id={}
            """.format(member_id, book_id))

            records = cursor.fetchall()

            if records:
                for row in records:
                    a = row[0]

                fine = max(0, a * 5)

                cursor.execute("""UPDATE issue_records
                SET fine={}
                WHERE member_id={} and book_id={}""".format(fine, member_id, book_id))

                cursor.execute("""UPDATE books
                SET available_quantity = available_quantity + 1
                WHERE book_id={}""".format(book_id))

                con.commit()

                print("Book returned successfully.")
                print("Fine:", fine)

            else:
                print("No matching issue record found.")

            input("Press 'Enter' to continue.......")

        elif choice==3:
            cursor.execute(view_issued_records())
            records = cursor.fetchall()
            print(f"{'Member ID':<20}{'Name':<30}{'Book Title':<30}{'Status':<30}")
            for row in records:
                a1 = row[0]
                a2 = row[1]
                a3 = row[2]
                a4 = row[3]
                print(f"{a1:<20}{a2:<30}{a3:<30}{a4:<30}")
            con.commit()
            input("Press 'Enter' to continue.......")
        
        elif choice==4:
            cursor.execute(view_overdue_records())
            records = cursor.fetchall()
            print(f"{'Member ID':<20}{'Name':<30}{'Book Title':<30}{'Status':<30}")
            for row in records:
                a1 = row[0]
                a2 = row[1]
                a3 = row[2]
                a4 = row[3]
                print(f"{a1:<20}{a2:<30}{a3:<30}{a4:<30}")
            con.commit()
            input("Press 'Enter' to continue.......")
        
        elif choice==5:
            cursor.execute(member_issue_history())
            records = cursor.fetchall()
            print(f"{'Member ID':<20}{'Name':<30}{'Book Title':<30}{'Status':<30}")
            for row in records:
                a1 = row[0]
                a2 = row[1]
                a3 = row[2]
                a4 = row[3]
                print(f"{a1:<20}{a2:<30}{a3:<30}{a4:<30}")
            con.commit()
            input("Press 'Enter' to continue.......")
        
        elif choice==6:
            cursor.execute(book_issue_history())
            records = cursor.fetchall()
            print(f"{'Book ID':<20}{'Title':<30}{'Member ID':<30}{'Name':<30}")
            for row in records:
                a1 = row[0]
                a2 = row[1]
                a3 = row[2]
                a4 = row[3]
                print(f"{a1:<20}{a2:<30}{a3:<30}{a4:<30}")
            con.commit()
            input("Press 'Enter' to continue.......")
        elif choice==7:
            break
        else:
            print("!!!!!!! INVALID INPUT !!!!!!!")

def reports_manager():
    while True:
        print("***********************************")
        print("       Reports Manager      ")
        print("***********************************")
        print("1. Library Dashboard")
        print("2. Available Books Report")
        print("3. Issued Books Reports")
        print("4. Overdue Books Reports")
        print("5. Member Reports")
        print("6. Most Borrowed Books")
        print("7. Fine Collection Reports")
        print("8. Back")
        print("***********************************")
        try:
            choice = int(input("Enter your choice: "))
        except ValueError:
            print("Invalid Input")
        if choice==1:
            cursor.execute("SELECT count(book_id) FROM books")
            records = cursor.fetchall()
            for row in records:
                for i in row:
                    a1=i
            cursor.execute("SELECT count(book_id) FROM books WHERE quantity>0")
            records = cursor.fetchall()
            for row in records:
                for i in row:
                    a2=i
            cursor.execute("SELECT count(book_id) FROM issue_records WHERE status='Issued'")
            records = cursor.fetchall()
            for row in records:
                for i in row:
                    a3=i
            cursor.execute("SELECT count(member_id) FROM members")
            records = cursor.fetchall()
            for row in records:
                for i in row:
                    a4=i
            cursor.execute("SELECT count(book_id) FROM issue_records WHERE status='Overdue'")
            records = cursor.fetchall()
            for row in records:
                for i in row:
                    a5=i
            cursor.execute("SELECT SUM(fine) FROM issue_records")
            records = cursor.fetchall()
            for row in records:
                for i in row:
                    a6=i
            
            print(f'''
================================
    LIBRARY DASHBOARD
================================
Total Books           : {a1}
Available Books       : {a2}
Issued Books          : {a3}
Total Members         : {a4}
Overdue Books         : {a5}
Total Fine Collected  : {a6}
================================''')
            con.commit()
            input("Press 'Enter' to continue.......")

        elif choice==2:
            cursor.execute("SELECT * FROM books WHERE quantity>0")
            records = cursor.fetchall()
            print(f"{'Book ID':<10}{'Title':<35}{'Available'}")
            for row in records:
                a1=row[0]
                a2=row[1]
                a3=row[7]
                print(f"{a1:<10}{a2:<35}{a3}")
            con.commit()
            input("Press 'Enter' to continue.......")
        
        elif choice==3:
            
            data = issued_books_function()
            print(f"{'Issue_ID':<10}{'Name':<35}{'Title'}")
            for i in range(len(data)):
                a1 = data[i][0]
                a2 = data[i][1]
                a3 = data[i][2]
                print(f"{a1:<10}{a2:<35}{a3}")
            con.commit()
            input("Press 'Enter' to continue.......")
        
        elif choice==4:
            cursor.execute("""SELECT
            m.name,
            b.title,
            i.due_date
            FROM issue_records i
            JOIN books b
            ON i.book_id = b.book_id
            JOIN members m
            ON i.member_id = m.member_id;""")
            records = cursor.fetchall()
            print(f"{'Name':<20}{'Title':<40}{'Due-Date'}")
            for row in records:
                a1=row[0]
                a2=row[1]
                a3=row[2]
                print(f"{a1:<20}{a2:<40}{a3}")
            con.commit()
            input("Press 'Enter' to continue.......")
        
        elif choice==5:
            data = members()
            print(f"{'Member ID':<10}{'Name':<25}{'Email':<35}{'Phone':<15}{'Course':<20}{'Join Date':<15}")
            for i in range(len(data)):
                a1 = data[i][0]
                a2 = data[i][1]
                a3 = data[i][2]
                a4 = data[i][3]
                a5 = data[i][4]
                a6 = data[i][5]
                print(f"{a1:<10}{a2:<25}{a3:<35}{a4:<15}{a5:<20}{a6:<15}")
            con.commit()
            input("Press 'Enter' to continue.......")
            
        elif choice==6:
            cursor.execute("""SELECT b.book_id,
            b.title,
            COUNT(i.book_id) AS times_borrowed
            FROM books b
            JOIN issue_records i
            ON b.book_id = i.book_id
            GROUP BY b.book_id, b.title
            ORDER BY times_borrowed DESC""")
            records = cursor.fetchall()
            print(f"{'Book ID':<20}{'Title':<40}{'Times Borrowed'}")
            for row in records:
                a1 = row[0]
                a2 = row[1]
                a3 = row[2]
                print(f"{a1:<20}{a2:<40}{a3}")
            
            con.commit()
            input("Press 'Enter' to continue.......")
        
        elif choice==7:
            data = fine()
            print(f"{'Issue ID':<20}{'Name':<40}{'Fine'}")
            for i in range(len(data)):
                a1 = data[i][0]
                a2 = data[i][1]
                a3 = data[i][2]
                print(f"{a1:<20}{a2:<40}{a3}")
            con.commit()
            input("Press 'Enter' to continue.......")  
        
        elif choice==8:
            break
        else: 
            print("!!!!!!! INVALID INPUT !!!!!!!")

def imports_manager():
    while True:
        print("***********************************")
        print("       IMPORT FILES      ")
        print("***********************************")
        print("1. Export Issued Books")
        print("2. Export Members")
        print("3. Export Fines")
        print("4. Back")
        print("***********************************")
        try:
            choice = int(input("Enter your choice: "))
        except ValueError:
            print("Invalid Input")
        if choice==1:
            file_name = input("Enter the file name: ")
            data = issued_books_function()
            headings = f"{'Issue_ID':<30}\t{'Name':<30}\t{'Title'}"
            write_txt(file_name,headings,data)
            print("***** FILE CREATED *****")
            input("Press 'Enter' to continue.......") 
        elif choice==2:
            file_name = input("Enter the file name: ")
            data = members()
            headings = f"{'Member ID':<30}\t{'Name':<30}\t{'Email':<30}\t{'Phone':<30}\t{'Course':<30}"
            write_txt(file_name,headings,data)
            print("***** FILE CREATED *****")
            input("Press 'Enter' to continue.......") 
        elif choice==3:
            file_name = input("Enter the file name: ")
            data = fine()
            headings = f"{'Issue ID':<30}\t{'Name':<30}\t{'Fine'}"
            write_txt(file_name,headings,data)
            print("***** FILE CREATED *****")
            input("Press 'Enter' to continue.......") 
        elif choice==4:
            break
        else:
            print("!!!!!!! INVALID INPUT !!!!!!!")

