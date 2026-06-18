def issue_book(book,member):
    query = "INSERT INTO issue_records (book_id,status,member_id) VALUES({},'Issued',{})".format(book,member)
    return query

def return_book(date,book,member):
    query = """UPDATE issue_records
    SET return_date='{}'
    WHERE book_id={} and member_id={}""".format(date,book,member)
    return query
    
def view_issued_records():
    query = """SELECT
    m.member_id,
    m.name,
    b.title,
    i.status
FROM issue_records i
JOIN members m
ON i.member_id = m.member_id
JOIN books b
ON i.book_id = b.book_id
WHERE i.status = 'Issued'"""
    return query

def view_overdue_records():
    query = """SELECT
    m.member_id,
    m.name,
    b.title,
    i.status
FROM issue_records i
JOIN members m
ON i.member_id = m.member_id
JOIN books b
ON i.book_id = b.book_id
WHERE i.status = 'Overdue'"""
    return query

def member_issue_history():
    member_id = int(input("Enter member_id: "))
    query = """SELECT
    m.member_id,
    m.name,
    b.title,
    i.status
FROM issue_records i
JOIN members m
    ON i.member_id = m.member_id
JOIN books b
    ON i.book_id = b.book_id
WHERE m.member_id ={}""".format(member_id)
    return query

def book_issue_history():
    book_id = int(input("Enter book_id: "))
    query = """
    SELECT
        b.book_id,
        b.title,
        m.member_id,
        m.name,
        i.issue_date,
        i.return_date,
        i.status
    FROM issue_records i
    JOIN books b
        ON i.book_id = b.book_id
    JOIN members m
        ON i.member_id = m.member_id
    WHERE b.book_id = {}
    """.format(book_id)
    return query


    

        

    
