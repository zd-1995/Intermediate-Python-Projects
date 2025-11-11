# Library Management System

# Create user
class User:
    def __init__(self, first_name:str, last_name:str ,user_id:str, membership_status:str, national_code:str):
        self.first_name = first_name
        self.last_name = last_name
        self.user_id = user_id
        self.membership_status = membership_status
        self.national_code = national_code


    def check_membership(self):
        if self.membership_status == "employee":
            return "employee"
        elif self.membership_status == "member":
            return "member"
        else:
            return "Membership does not exist."

    def display_info(self):
        # User information
        return f"[{self.user_id}] {self.first_name} {self.last_name} - {self.check_membership()}"

# Create book
class Book:
    def __init__(self, title:str, author:str, book_id:str, is_available:bool, year_published:int):
        self.title = title
        self.author = author
        self.book_id = book_id
        self.is_available = is_available
        self.year_published = year_published


    def borrow(self):
        if not self.is_available:
            return False
        self.is_available = False
        return True

    def return_back(self):
        self.is_available = True

    def get_book_info(self):
        return f"{self.title} by {self.author} ({self.year_published})"

# Library Management
class LibraryManagement:
    def __init__(self, user_information, book_information):
        self.user_information = user_information
        self.book_information = book_information
        self.rent_book_list = []
        self.return_book_list = []

    def search_book(self,book_id=None , title=None , author=None, year_published=None):
        # Searching for book in books information
        for b_id,b_details in self.book_information.items():
            # Search with book id
            if book_id == b_id:
                return self.book_information[b_id]
            # Search with title and author and year published
            elif (title == b_details.title and
                  author == b_details.author and
                  year_published == b_details.year_published):
                return b_details

        return None

    def remove_book(self,book_id=None, title=None , author=None, year_published=None ):
        # Delete existing book from library
        check_book = (self.search_book(book_id=book_id) or
                      self.search_book(title=title, author=author, year_published=year_published))
        if check_book is None:
            return "Book not found."

        for b_id, b_details in list(self.book_information.items()):
            if b_details == check_book:
                print("\nBook information:",
                      f"Title: {b_details.title},"
                      f"Author: {b_details.author},"
                      f"Year Published: {b_details.year_published},"
                      f"Available: {b_details.is_available}")

                # Ask if the user wants to delete
                choice = input("\nDo you want to delete? (y/n): ").lower()
                if choice == 'y':
                    del self.book_information[b_id]
                    return "Book successfully removed."
                else:
                    return "Book was not deleted."

        return None

    def add_book(self,title,author,year_published):
        # Search for the latest book ID
        if not self.book_information:
            new_id = "B001"
        else:
            ids = [int(bid[1:]) for bid in self.book_information.keys()]
            last_id_num = max(ids) if ids else 0
            new_id = f"B{last_id_num + 1:03}"

        # Search for books in the library
        check_book = (self.search_book(title=title, author=author, year_published=year_published))

        if check_book is None:
            # Add new book
            self.book_information[new_id] = Book(title=title,
                                                 author=author,
                                                 year_published=year_published,
                                                 book_id=new_id,
                                                 is_available=True)
        else:
            return "Book already exists."

        info = self.book_information[new_id].get_book_info()

        return f"Book {info} successfully added."

    def rent_book(self,title,author,book_id,year_published,first_name,last_name,user_id,national_code,membership_status):
        # Search for book available
        check_book = (self.search_book(book_id=book_id) or
                      self.search_book(title=title, author=author, year_published=year_published))
        if check_book is None:
            return "Book not found."

        if not check_book.borrow():
            return "Book is not available for rent."

        # Search for user is a member
        if user_id not in self.user_information:
            user_id = self.register_user(first_name, last_name, national_code, membership_status)
        else:
            user_id = self.user_information[user_id]

        # Rent a book
        book_id = check_book.book_id
        self.rent_book_list.append({
            "book": self.book_information[book_id],
            "user": self.user_information[user_id]
        })

        self.book_information[book_id].is_available = False

        return f"Book '{title}' successfully rented to user {user_id}."

    def return_book(self,rent_book_id,rent_user_id):
        # Register the details of the person returning the book and change the status
        found = None
        for record in self.rent_book_list:
            if record["book"].book_id == rent_book_id and record["user"].user_id == rent_user_id:
                found = record
                break

        if not found:
            return "No matching rented book found for this user."

        # Update book status and record return
        self.book_information[rent_book_id].is_available = True
        self.return_book_list.append(found)
        self.rent_book_list.remove(found)

        return f"Book '{rent_book_id}' successfully returned to library."

    def register_user(self,first_name,last_name,national_code,role):
        # Search for the latest user ID
        if not self.user_information:
            new_id = "U001"
        else:
            ids = [int(uid[1:]) for uid in self.user_information.keys()]
            last_id_num = max(ids) if ids else 0
            new_id = f"U{last_id_num + 1:03}"

        # Check for duplicate national code
        if any(user.national_code == national_code for user in self.user_information.values()):
            return "A user with this national code already exists."

        # Add new user
        self.user_information[new_id] = User(first_name=first_name,
                                             last_name=last_name,
                                             national_code=national_code,
                                             membership_status=role,
                                             user_id=new_id)

        info_user = self.user_information[new_id].display_info()
        print(f"User {info_user} successfully registered.")
        return new_id

    def remove_user(self,user_id):
        # Delete existing user from library
        if user_id in self.user_information:
            u = self.user_information[user_id]
            print("\nUser information:",
                  f"First Name: {u.first_name},"
                  f"Last Name: {u.last_name},"
                  f"User ID: {u.user_id},"
                  f"Membership Status: {u.membership_status}, "
                  f"National Code: {u.national_code}")

            # Ask if the user wants to delete
            choice = input("\nDo you want to delete? (y/n): ").lower()
            if choice == 'y':
                del self.user_information[user_id]
                return "User deleted."
            else:
                return "User was not deleted."
        else:
            return "User does not exist."

if __name__ == "__main__":
    print("Welcome to the library management system.")

    users_data = {
        "U001": User("Alice", "Johnson", "U001", "member", "1234567890"),
        "U002": User("Bob", "Smith", "U002", "member", "0987654321"),
        "U003": User("Emma", "Brown", "U003", "employee", "1122334455")
    }

    books_data = {
        "B001": Book("The Great Gatsby", "F. Scott Fitzgerald", "B001", True, 1925),
        "B002": Book("To Kill a Mockingbird", "Harper Lee", "B002", False, 1960),
        "B003": Book("1984", "George Orwell", "B003", True, 1949),
    }

    library_management = LibraryManagement(users_data, books_data)


    while True:
        # Display the menu options.
        try:
            selection = int(input("Enter the desired option:\n1. Add New Book\n"
                          "2. Remove Book\n"
                          "3. Search Book\n"
                          "4. Rent a book\n"
                          "5. Return a book\n"
                          "6. Register a user\n"
                          "7. Check a user's membership\n"
                          "8. Delete a user\n"
                          "9. Exit\n"))

        except ValueError:
            print("Invalid input. Please enter a number.")
            continue

        # Select the desired option
        # 1. Add New Book
        if selection == 1:
            title = input("Enter  the title: ")
            author = input("Enter the author name: ")
            while True:
                try:
                    year_published = int(input("Enter year published: "))
                    break
                except ValueError:
                    print("Please enter a valid year.")
            print(library_management.add_book(title,author,year_published))

        # 2. Remove Book
        elif selection == 2:
            book_id = input("Enter the book ID to remove: ").strip()
            print(library_management.remove_book(book_id = book_id))

        # 3. Search Book
        elif selection == 3:
            book_id = input("Enter the book ID to return: ")
            title = input("Enter title (or leave blank): ").strip()
            author = input("Enter author (or leave blank): ").strip()

            while True:
                try:
                    year = int(input("Enter year: "))
                    break
                except ValueError:
                    print("Please enter a valid year.")

            book = library_management.search_book(book_id = book_id, title=title, author=author, year_published=year)
            if book:
                print(book.get_book_info())
            else:
                print("Book not found.")

        # 4. Rent a book
        elif selection == 4:
            while True:
                title = input("Enter the title: ").strip()
                if title:
                    break
                print("Title cannot be empty. Please enter a valid title.")
            author = input("Enter the author name (optional): ").strip()
            book_id = input("Enter the book id: ").strip()

            while True:
                try:
                    year_published = int(input("Enter the year published: ").strip())
                    break
                except ValueError:
                    print("Please enter a valid year.")

            while True:
                first_name = input("Enter first name: ")
                last_name = input("Enter last name: ")
                user_id = input("Enter user id: ").strip()
                national_code = input("Enter national code: ")
                if first_name and last_name and user_id and national_code:
                    break
                print("First name and last name and user id cannot be empty.")

            while True:
                membership_status = input("Enter role (member or employee): ").strip().lower()
                if membership_status in ["member", "employee"]:
                    break
                print("Invalid role. Please enter 'member' or 'employee'.")

            print(library_management.rent_book(title=title,author=author,book_id=book_id,
                                               year_published=year_published,first_name=first_name,
                                               last_name=last_name,user_id=user_id,
                                               national_code=national_code,
                                               membership_status=membership_status))

        # 5. Return a book
        elif selection == 5:
            rent_book_id = input("Enter the rent book id: ").strip()
            rent_user_id = input("Enter the rent user id: ").strip()
            print(library_management.return_book(rent_book_id,rent_user_id))

        # 6. Register a user
        elif selection == 6:
            # Get user data
            first_name = input("Enter first name: ")
            last_name = input("Enter last name: ")
            national_code = input("Enter national code: ")

            while True:
                role = input("Enter role (member or employee): ").strip().lower()
                if role in ["member", "employee"]:
                    break
                print("Invalid role. Please enter 'member' or 'employee'.")

            print(library_management.register_user(first_name,last_name,national_code,role))

        # 7. Check a user's membership
        elif selection == 7:
            user_id = input("Enter user ID: ").strip()
            if user_id in users_data:
                print(users_data[user_id].check_membership())
            else:
                print("User not found.")


        # 8. Delete a user
        elif selection == 8:
            user_id = input("Enter user ID to delete: ").strip()
            print(library_management.remove_user(user_id=user_id))

        # 9. Exit
        elif selection == 9:
            break
