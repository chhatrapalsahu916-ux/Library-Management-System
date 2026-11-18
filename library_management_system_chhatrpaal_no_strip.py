# Library Management System

import json
from datetime import date

BOOKS_FILE = "books.json"
STUDENTS_FILE = "students.json"
ISSUED_FILE = "issued_books.json"


def load_data(file_name):
    try:
        with open(file_name, "r") as file:
            data = json.load(file)
            return data
    except FileNotFoundError:
        return []


def save_books():
    with open(BOOKS_FILE, "w") as file:
        json.dump(books, file, indent=4)


def save_students():
    with open(STUDENTS_FILE, "w") as file:
        json.dump(students, file, indent=4)


def save_issued_books():
    with open(ISSUED_FILE, "w") as file:
        json.dump(issued_books, file, indent=4)


def add_book():
    book_id = input("Enter Book ID: ")

    for book in books:
        if book["book_id"] == book_id:
            print("Book ID already exists!")
            return

    book_name = input("Enter Book Name: ")
    author = input("Enter Author Name: ")
    category = input("Enter Category: ")

    while True:
        try:
            copies = int(input("Enter Number of Copies: "))
            if copies > 0:
                break
            print("Number of copies must be greater than zero.")
        except ValueError:
            print("Please enter a whole number.")

    book = {
        "book_id": book_id,
        "book_name": book_name,
        "author": author,
        "category": category,
        "available_copies": copies
    }

    books.append(book)
    save_books()
    print("Book added successfully!")


def display_books():
    if len(books) == 0:
        print("No books are available.")
        return

    sorted_books = books.copy()
    for i in range(len(sorted_books)):
        for j in range(i + 1, len(sorted_books)):
            if sorted_books[i]["book_name"].lower() > sorted_books[j]["book_name"].lower():
                temporary_book = sorted_books[i]
                sorted_books[i] = sorted_books[j]
                sorted_books[j] = temporary_book
    print("\n===== ALL BOOKS =====")
    for book in sorted_books:
        print("Book ID:", book["book_id"])
        print("Book Name:", book["book_name"])
        print("Author:", book["author"])
        print("Category:", book["category"])
        print("Available Copies:", book["available_copies"])
        print("-----------------------------")


def search_book():
    search_text = input("Enter Book ID, Book Name, or Author Name: ").lower()
    found = False

    for book in books:
        if (search_text in book["book_id"].lower()
                or search_text in book["book_name"].lower()
                or search_text in book["author"].lower()):
            print("\nBook Found!")
            print("Book ID:", book["book_id"])
            print("Book Name:", book["book_name"])
            print("Author:", book["author"])
            print("Category:", book["category"])
            print("Available Copies:", book["available_copies"])
            found = True

    if found == False:
        print("Book not found.")


def register_student():
    student_id = input("Enter Student ID: ")

    for student in students:
        if student["student_id"] == student_id:
            print("Student ID already exists!")
            return

    student_name = input("Enter Student Name: ")
    department = input("Enter Department: ")
    contact_number = input("Enter Contact Number: ")

    student = {
        "student_id": student_id,
        "student_name": student_name,
        "department": department,
        "contact_number": contact_number
    }

    students.append(student)
    save_students()
    print("Student registered successfully!")


def issue_book():
    student_id = input("Enter Student ID: ")
    student_found = False

    for student in students:
        if student["student_id"] == student_id:
            student_found = True

    if student_found == False:
        print("Student is not registered!")
        return

    student_book_count = 0
    for record in issued_books:
        if record["student_id"] == student_id and record["status"] == "issued":
            student_book_count = student_book_count + 1

    if student_book_count >= 3:
        print("A student cannot issue more than three books at a time.")
        return

    book_id = input("Enter Book ID: ")
    selected_book = None

    for book in books:
        if book["book_id"] == book_id:
            selected_book = book

    if selected_book == None:
        print("Book not found!")
        return

    if selected_book["available_copies"] <= 0:
        print("No copies are available.")
        return

    selected_book["available_copies"] = selected_book["available_copies"] - 1

    issue_record = {
        "student_id": student_id,
        "book_id": book_id,
        "issue_date": str(date.today()),
        "status": "issued",
        "returned_date": ""
    }

    issued_books.append(issue_record)
    save_books()
    save_issued_books()
    print("Book issued successfully!")


def return_book():
    student_id = input("Enter Student ID: ")
    book_id = input("Enter Book ID to Return: ")
    issue_found = False

    for record in issued_books:
        if (record["student_id"] == student_id and record["book_id"] == book_id
                and record["status"] == "issued"):
            record["status"] = "returned"
            record["returned_date"] = str(date.today())
            issue_found = True
            break

    if issue_found == False:
        print("Active issue record not found!")
        return

    for book in books:
        if book["book_id"] == book_id:
            book["available_copies"] = book["available_copies"] + 1

    save_books()
    save_issued_books()
    print("Book returned successfully!")


def display_issued_books():
    found = False
    print("\n===== CURRENTLY ISSUED BOOKS =====")

    for record in issued_books:
        if record["status"] == "issued":
            print("Student ID:", record["student_id"])
            print("Book ID:", record["book_id"])
            print("Issue Date:", record["issue_date"])
            print("-----------------------------")
            found = True

    if found == False:
        print("No books are currently issued.")


def delete_book():
    book_id = input("Enter Book ID to Delete: ")
    book_to_delete = None

    for record in issued_books:
        if record["book_id"] == book_id and record["status"] == "issued":
            print("This book is currently issued and cannot be deleted.")
            return

    for book in books:
        if book["book_id"] == book_id:
            book_to_delete = book

    if book_to_delete == None:
        print("Book not found!")
        return

    confirmation = input("Are you sure you want to delete this book? (yes/no): ").lower()
    if confirmation == "yes":
        books.remove(book_to_delete)
        save_books()
        print("Book deleted successfully!")
    else:
        print("Delete cancelled.")


def display_summary():
    total_copies = 0
    for book in books:
        total_copies = total_copies + book["available_copies"]

    print("Book Titles:", len(books))
    print("Available Copies:", total_copies)
    print("Registered Students:", len(students))

    issue_counts = {}
    for record in issued_books:
        book_id = record["book_id"]
        if book_id in issue_counts:
            issue_counts[book_id] = issue_counts[book_id] + 1
        else:
            issue_counts[book_id] = 1

    if len(issue_counts) > 0:
        most_issued_id = ""
        highest_issue_count = 0
        for book_id in issue_counts:
            if issue_counts[book_id] > highest_issue_count:
                highest_issue_count = issue_counts[book_id]
                most_issued_id = book_id
        most_issued_name = most_issued_id
        for book in books:
            if book["book_id"] == most_issued_id:
                most_issued_name = book["book_name"]
        print("Most Frequently Issued Book:", most_issued_name)
    else:
        print("Most Frequently Issued Book: No issue records yet")


books = load_data(BOOKS_FILE)
students = load_data(STUDENTS_FILE)
issued_books = load_data(ISSUED_FILE)


def main():
    while True:
        print("\n===== LIBRARY MANAGEMENT SYSTEM =====")
        print("1. Add New Book")
        print("2. Display All Books")
        print("3. Search for a Book")
        print("4. Register a Student")
        print("5. Issue a Book")
        print("6. Return a Book")
        print("7. Display Issued Books")
        print("8. Delete a Book")
        print("9. Exit")
        

        choice = input("Enter your choice: ")

        if choice == "1":
            add_book()
        elif choice == "2":
            display_books()
        elif choice == "3":
            search_book()
        elif choice == "4":
            register_student()
        elif choice == "5":
            issue_book()
        elif choice == "6":
            return_book()
        elif choice == "7":
            display_issued_books()
        elif choice == "8":
            delete_book()
        elif choice == "9":
            print("Exiting program. Goodbye!")
            
        else:
            print("Invalid choice. Please try again.")


main()


