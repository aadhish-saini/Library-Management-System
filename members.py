def add_new():
    name = input("Enter name: ")
    email = input("Enter email: ")
    phone = int(input("Enter Phone number: "))
    course = input("Enter course: ")
    query = "INSERT INTO members (name, email, phone, course) VALUES ('{}','{}',{},'{}')".format(name,email,phone,course)
    return query

def view_all_member():
    query = "Select * from members"
    return query

def search_member():
    member_id = int(input("Enter the member_id: "))
    query = "SELECT * FROM members WHERE member_id={}".format(member_id)
    return query

def update_member():
    while True:
        print("1. Change Name")
        print("2. Change Email")
        print("3. Change Phone")
        print("4. Change course")
        print("5. Back")
        
        choice = int(input("Enter the details number you want to change: "))
        member_id = int(input("Enter member_id: "))
        if choice==1:
            name = input("Enter new name: ")
            query = """UPDATE members
            SET name='{}'
            where member_id={}""".format(name,member_id)
            return query
        elif choice==2:
            email = input("Enter new email: ")
            query = """UPDATE members
            SET email='{}'
            where member_id={}""".format(email,member_id)
            return query
        elif choice==3:
            phone = input("Enter new phone: ")
            query = """UPDATE members
            SET phone={}
            where member_id={}""".format(phone,member_id)
            return query
        elif choice==4:
            course = input("Enter new course: ")
            query = """UPDATE members
            SET course='{}'
            where member_id={}""".format(course,member_id)
            return query
        elif choice==5:
            break
        else:
            print("!!!!!!! Invalid INPUT !!!!!!!")

def delete_member():
    member_id = int(input("Enter member_id: "))
    query = "DELETE FROM members where member_id={}".format(member_id)
    return query

def view_issued_book():
    member_id = int(input("Enter member_id: "))
    query = """SELECT b.book_id,
       b.title
FROM books b
JOIN issue_records i
ON b.book_id = i.book_id
WHERE i.member_id = {}
AND i.status = 'Issued'""".format(member_id)
    return query
