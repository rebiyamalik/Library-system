import hashlib

# Person class as the base for User and Admin
class Person:
    def __init__(self, username, password, role='user'):
        self.username = username
        self.password = hashlib.sha256(password.encode()).hexdigest()  # Storing hashed password
        self.role = role

    def check_password(self, password):
        # Check if the entered password matches the stored hash
        return self.password == hashlib.sha256(password.encode()).hexdigest()

# User class extends Person
class User(Person):
    def __init__(self, username, password):
        super().__init__(username, password, role="user")
        self.borrowed_books = []

    def borrow(self, book):
        if len(self.borrowed_books) >= 5:
            print("❗ Borrowing limit reached.")
            return False
        if book.borrow():
            self.borrowed_books.append(book)
            print(f"✅ {book.title} borrowed.")
            return True
        print("❌ Book is already borrowed.")
        return False

    def return_book(self, book):
        if book in self.borrowed_books and book.return_book():
            self.borrowed_books.remove(book)
            print(f"📘 {book.title} returned.")
            return True
        print("❌ Book not in your borrowed list.")
        return False

    def view_borrowed_books(self):
        if not self.borrowed_books:
            print("You haven't borrowed any books.")
        for book in self.borrowed_books:
            print(book)

# Admin class extends Person
class Admin(Person):
    def __init__(self, username, password):
        super().__init__(username, password, role="admin")

    def add_book(self, library, title, author, isbn, accession_number):
        book = Book(title, author, isbn, accession_number)
        library.add_book(book)
        print(f"✅ {title} added to the library.")

    def remove_book(self, library, title):
        books_to_remove = library.search_by_title(title)
        if books_to_remove:
            for idx, book in enumerate(books_to_remove):
                print(f"{idx + 1}. {book}")
            try:
                book_id = int(input("Select book number to remove: ")) - 1
                library.books.remove(books_to_remove[book_id])
                print("📚 Book removed.")
            except:
                print("Invalid choice.")
        else:
            print("❌ No books found.")

    def view_all_users(self, library):
        print("All users:")
        for user in library.users.values():
            print(f"{user.username} - Role: {user.role}")

# Book class
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

    def __str__(self):
        status = "Borrowed" if self.is_borrowed else "Available"
        return f"{self.title} by {self.author} [{status}]"

# Library class
class Library:
    def __init__(self):
        self.books = []
        self.users = {}
        self.admins = {}

    def add_book(self, book):
        self.books.append(book)

    def search_by_title(self, title):
        return [book for book in self.books if title.lower() in book.title.lower()]

    def list_available_books(self):
        available = [book for book in self.books if not book.is_borrowed]
        if not available:
            print("No available books.")
        for book in available:
            print(book)

    def register_user(self, username, password, role='user'):
        if role == 'admin':
            self.admins[username] = Admin(username, password)
        else:
            self.users[username] = User(username, password)

    def login(self, username, password):
        user = self.users.get(username) or self.admins.get(username)
        if user and user.check_password(password):
            print(f"Welcome, {username}!")
            return user
        print("Invalid username or password.")
        return None

# Main execution
def main():
    # Initialize the library system
    library = Library()

    # Register users and admins
    library.register_user("admin", "adminpass", role="admin")
    library.register_user("user1", "userpass", role="user")
    library.register_user("user2", "user2pass", role="user")

    # Add books to the library
    library.add_book(Book("Python Crash Course", "Eric Matthes", "123", "A001"))
    library.add_book(Book("Automate the Boring Stuff", "Al Sweigart", "124", "A002"))
    library.add_book(Book("Learning JavaScript", "John Doe", "125", "A003"))

    # Login process
    logged_in_user = None
    while not logged_in_user:
        username = input("Enter username: ")
        password = input("Enter password: ")
        logged_in_user = library.login(username, password)

    # Admin or user menu based on the role
    if isinstance(logged_in_user, Admin):
        print("\nWelcome, Admin. You can manage books and users.")
    else:
        print("\nWelcome, User. You can borrow and return books.")

    # Main menu loop
    while True:
        if isinstance(logged_in_user, Admin):
            print("\n1. View All Books\n2. Add Book\n3. Remove Book\n4. View All Users\n5. Exit")
            choice = input("Choose an option: ")

            if choice == "1":
                library.list_available_books()

            elif choice == "2":
                title = input("Enter book title: ")
                author = input("Enter book author: ")
                isbn = input("Enter book ISBN: ")
                accession_number = input("Enter accession number: ")
                logged_in_user.add_book(library, title, author, isbn, accession_number)

            elif choice == "3":
                title = input("Enter book title to remove: ")
                logged_in_user.remove_book(library, title)

            elif choice == "4":
                logged_in_user.view_all_users(library)

            elif choice == "5":
                print("Goodbye!")
                break

        else:  # User menu
            print("\n1. View Books\n2. Borrow Book\n3. Return Book\n4. My Borrowed Books\n5. Exit")
            choice = input("Choose an option: ")

            if choice == "1":
                library.list_available_books()

            elif choice == "2":
                title = input("Enter book title to borrow: ")
                results = library.search_by_title(title)
                if results:
                    for idx, book in enumerate(results):
                        print(f"{idx + 1}. {book}")
                    try:
                        index = int(input("Select book number: ")) - 1
                        logged_in_user.borrow(results[index])
                    except:
                        print("Invalid choice.")
                else:
                    print("No books found.")

            elif choice == "3":
                logged_in_user.view_borrowed_books()
                if logged_in_user.borrowed_books:
                    try:
                        index = int(input("Select book number to return: ")) - 1
                        logged_in_user.return_book(logged_in_user.borrowed_books[index])
                    except:
                        print("Invalid choice.")

            elif choice == "4":
                logged_in_user.view_borrowed_books()

            elif choice == "5":
                print("Goodbye!")
                break

            else:
                print("Invalid option.")

if __name__ == "__main__":
    main()

    