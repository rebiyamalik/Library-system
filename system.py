
class Book:
    def __init__(self, title, author, isbn, accession_number):
        self.title = title
        self.author = author
        self.isbn = isbn
        self.accession_number = accession_number
        self.is_borrowed = False

    def borrow(self):
        if not self.is_borrowed:
            self.is_borrowed = True
            return True
        return False

    def return_book(self):
        if self.is_borrowed:
            self.is_borrowed = False
            return True
        return False

class User:
    def __init__(self, name, user_id):
        self.name = name
        self.user_id = user_id
        self.borrowed_books = []
        self.max_borrowed_books = 5

    def borrow_book(self, book):
        if len(self.borrowed_books) < self.max_borrowed_books:
            if book.borrow():
                self.borrowed_books.append(book)
                return True
        return False

    def return_book(self, book):
        if book in self.borrowed_books and book.return_book():
            self.borrowed_books.remove(book)
            return True
        return False

class Librarian:
    def __init__(self, name, employee_id):
        self.name = name
        self.employee_id = employee_id

    def search_book(self, books, title):
        return [book for book in books if title.lower() in book.title.lower()]

    def calculate_fine(self, overdue_days):
        return overdue_days * 1.0  # Sample: $1 fine per overdue day

# Books ki list banai
books = [
    Book("Python Programming", "John Smith", "1234567890", "ACC12345"),
    Book("Data Structures and Algorithms", "Jane Doe", "9876543210", "ACC67890"),
    Book("Computer Networks", "Bob Johnson", "5432109876", "ACC34567")
]

# User banaya
user = User("John Doe", "12345")

# Librarian banaya
librarian = Librarian("Jane Smith", "67890")

# User ne book borrow ki
if user.borrow_book(books[0]):
    print("Book borrowed successfully.")
else:
    print("Book cannot be borrowed.")

# User ki borrowed books ki list dekhi
print("User's borrowed books:")
for book in user.borrowed_books:
    print(book.title, book.accession_number)

# Librarian ne book search ki
search_results = librarian.search_book(books, "Python")
print("Search results:")
for book in search_results:
    print(book.title, book.accession_number)

# User ne book return ki
if user.return_book(books[0]):
    print("Book returned successfully.")
else:
    print("Book cannot be returned.")

# User ki borrowed books ki list phir se dekhi
print("User's borrowed books after return:")
for book in user.borrowed_books:
    print(book.title, book.accession_number)
    