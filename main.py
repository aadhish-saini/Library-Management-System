from management_systems import login,admin_management,book_management,members_management,issue_return_manager,reports_manager,imports_manager,inactive_status
from books import view_all_books
from members import view_all_member


# ************************************************Login Details******************************************
print("===================================")
print("    Library MANAGEMENT SYSTEM      ")
print("===================================")
username = input("Username: ")
password = input("Password: ")
records = login(username,password)
break_point = 0
if records==None:
    break_point=1
else:
    print("===================================")
    print(f'''Welcome {records[0]}
Role: {records[1]}''')
    input("Press 'Enter' to continue.......")


# *******************************************Login BreakPoint****************************************************
while True:
    if break_point==1:
        print("Either username or password is incorrect")
        break


    systems = ["Admin Management System","Book Management System","Members Management System","Issue/Return Manager","Reports Manager","Importing Data"]   
    role=records[1]
    
    
# ************************************Admin Login**************************************************
    if role=="Super Admin":
        print("===================================")
        print("          Choose System            ")
        print("===================================")
        for i in range(len(systems)):
            print(f"{i+1}. {systems[i]}",end="\n")
        print("7. Exit")
        print("===================================")
        try:
            choice = int(input("Enter system number: "))
        except ValueError:
            print("Invalid Input")

        if choice==1:
            admin_management()
        elif choice==2:
            book_management()
        elif choice==3:
            members_management()
        elif choice==4:
            issue_return_manager()
        elif choice==5:
            reports_manager()
        elif choice==6:
            imports_manager()
        elif choice==7:
            print("TERMINATING THE PROGRAMMING")
            inactive_status(username,password)
            break
        else: 
            print("!!!!!!! INVALID INPUT !!!!!!!")

    elif role=="Librarian":
        print("===================================")
        print("          Choose System            ")
        print("===================================")
        for i in range(1,5):
            print(f"{i}. {systems[i]}",end='\n')
        print("5. Exit")
        print("===================================")
        try:
            choice = int(input("Enter system number: "))
        except ValueError:
            print("Invalid Input")
        if choice==1:
            book_management()
        elif choice==2:
            members_management()
        elif choice==3:
            issue_return_manager()
        elif choice==4:
            reports_manager()
        elif choice==5:
            print("TERMINATING THE PROGRAMMING")
            inactive_status(username,password)
            break
        else: 
            print("!!!!!!! INVALID INPUT !!!!!!!")
    
    elif role=="Assistant":
        reports_manager()
        print("TERMINATING THE PROGRAMMING")
        inactive_status(username,password)
        break

