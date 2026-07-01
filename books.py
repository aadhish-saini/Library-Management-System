def add_new_book():
    title = input("Enter the book title: ")
    author = input("Enter the author of book: ")
    category = input("Enter the category of the book: ")
    isbn = input("Enter the international standard book number: ")
    publisher = input("Enter the publisher of the book: ")
    quantity = int(input("Enter the quantity of the book: "))
    available_quantity = int(input("Enter the available quantity of the book: "))
    query = "INSERT INTO books(title,author,category,isbn,publisher,quantity,available_quantity) VALUES('{}','{}','{}','{}','{}',{},{})".format(title,author,category,isbn,publisher,quantity,available_quantity)
    return query

def view_all_books():
    query = "SELECT * FROM books"
    return query

def search_book():
    book_id = int(input("Enter the book_id: "))
    query = "SELECT * FROM books WHERE book_id ={}".format(book_id)
    return query

def update_book():
    book_id = int(input("Enter the book_id: "))
    while True:
        print("1. Change title")
        print("2. Change author")
        print("3. Change category")
        print("4. Change publisher")
        print("5. Change Quantity ")
        print("6. Change available quantity")    
        print("7. Back")
        choice = int(input("Enter your choice: "))
        if choice==1:
            title= input("Enter new title: ")
            query = """UPDATE books
            SET title='{}'
            WHERE book_id={}""".format(title,book_id)
            return query
        elif choice==2:
            author= input("Enter new author: ")
            query = """UPDATE books
            SET author='{}'
            WHERE book_id={}""".format(author,book_id)
            return query
        elif choice==3:
            category= input("Enter new category: ")
            query = """UPDATE books
            SET category='{}'
            WHERE book_id={}""".format(category,book_id)
            return query
        elif choice==4:
            publisher= input("Enter new publisher: ")
            query = """UPDATE books
            SET publisher='{}'
            WHERE book_id={}""".format(publisher,book_id)
            return query
        elif choice==5:
            quantity= int(input("Enter new quantity: "))
            query = """UPDATE books
            SET quantity={}
            WHERE book_id={}""".format(quantity,book_id)
            return query
        elif choice==6:
            available_quantity= int(input("Enter new available_quantity: "))
            query = """UPDATE books
            SET available_quantity={}
            WHERE book_id={}""".format(available_quantity,book_id)
            return query
        elif choice==7:
            break
        else:
            print("!!!!!!! Invalid INPUT !!!!!!!")

def delete_book():
    book_id = int(input("Enter book_id: "))
    query="DELETE FROM books WHERE book_id={}".format(book_id)
    return query

def check_book_availability():
    book_id = int(input("Enter book_id: "))
    query = "SELECT (available_quantity) FROM books WHERE book_id = {}".format(book_id)
    return query







