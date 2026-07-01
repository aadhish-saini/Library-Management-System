import mysql.connector as c

con = c.connect(
    host = "localhost",
    user = "root",
    password = "Aadhish20070",
    database = "lib"
)

cursor = con.cursor()


def main_login(username,password):
    query = "SELECT full_name,role FROM admin WHERE username='{}' and password = '{}'".format(username,password)
    return query
def add_admin():
    username = input("Enter username: ")
    password = input("Enter password: ")
    full_name = input("Enter full_name: ")
    email = input("Enter email: ")
    role = input("Enter role: ")
    query = "INSERT INTO admin(username,password,full_name,email,role) VALUES('{}','{}','{}','{}','{}')".format(username,password,full_name,email,role)
    return query
def view_all_admins():
    query= "SELECT admin_id,username,full_name,role FROM admin"
    return query
def search_admin():
    username = input("Enter username: ")
    query = "SELECT admin_id,full_name,role FROM admin WHERE username='{}'".format(username)
    return query
def update_admin():
    admin_id = int(input("Enter admin_id: "))
    password = input("Enter your Password: ")
    while True:
        print("1. Change Username")
        print("2. Change Name")
        print("3. Change Email")
        print("4. Change Role")
        print("5. Change Password")
        print("6. Back")
        try:
            choice = int(input("Enter your choice: "))
            if choice==1:
                username= input("Enter new username: ")
                query = """UPDATE admin
                SET username='{}'
                WHERE admin_id={} and password='{}'""".format(username,admin_id,password)
                return query
            elif choice==2:
                name= input("Enter new name: ")
                query = """UPDATE admin
                SET full_name='{}'
                WHERE admin_id={} and password='{}'""".format(name,admin_id,password)
                return query
            elif choice==3:
                email= input("Enter new email: ")
                query = """UPDATE admin
                SET email='{}'
                WHERE admin_id={} and password='{}'""".format(email,admin_id,password)
                return query
            elif choice==4:
                role= input("Enter new role: ")
                query = """UPDATE admin
                SET role='{}'
                WHERE admin_id={} and password='{}'""".format(role,admin_id,password)
                return query
            elif choice==5:
                new_password= input("Enter new password: ")
                query = """UPDATE admin
                SET password='{}'
                WHERE admin_id={} and password='{}'""".format(new_password,admin_id,password)
                return query
            elif choice==6:
                break
            else:
                print("!!!!!!! Invalid INPUT !!!!!!!")
        except ValueError:
            print("!!!!!!! Invalid INPUT !!!!!!!")

def delete_admin():
    admin_id = int(input("Enter admin_id: "))
    query = "DELETE FROM admin WHERE admin_id = {}".format(admin_id)
    return query

def view_last_login():
    query = "SELECT admin_id,username,role,last_login FROM admin ORDER BY last_login DESC LIMIT 1"
    return query
