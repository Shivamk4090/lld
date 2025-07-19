# user -> see list of book/search -> take book -> return book 
# library -> add book 


class User:
    def __init__(self, id, name):
        self.id = id
        self.name = name
        self.bw = {}
    
    def borrow(self, isbn):
        self.bw[isbn] = False

    def borrow_history(self):
        for isbn, returned in self.bw.items():
            status = "returned" if returned else "not returned"
            print(f"--> {self.name} - Book {isbn} - {status}")

class Book:
    def __init__(self, isbn, title, avail=False):
        self.isbn = isbn
        self.title = title
        self.avail = avail

class LibraryManger:
    def __init__(self):
        self.books  = []
        self.users = []

    def add_book(self, isbn, title):
        bk = Book(isbn, title, True)
        self.books.append(bk)
        return bk

    def borrow_book(self, user:User, book:Book):
        for bk in self.books:
            if bk.isbn == book.isbn:
                if bk.avail:
                    bk.avail = False
                    user.borrow(bk.isbn)
                    print(f"{user.name} borrowed the book {bk.title}")
                else:
                    print(f"{bk.title} not available 🥲 {user.name}")
    
    def return_book(self, user: User, isbn: int):
        for b in self.books:
            if b.isbn == isbn:
                b.avail = True
                user.bw[isbn] = True
                return f"{user.name} returned {b.title}"
        return "Book not found!"
    

    def search_books(self, title=None, only_available=False):
        results = []
        for b in self.books:
            if (not title  in b.title) and (not only_available or b.avail):
                results.append((b.isbn, b.title, "Available" if b.avail else "Borrowed"))
        return results





lib = LibraryManger()

# add book in library
bk1 = lib.add_book(101, "Harry Potter")
bk2 = lib.add_book(102, "The Roman Empire")

steve  = User(1, "steve")
alex  = User(2, "alex")

# borrow functionality
lib.borrow_book(steve, bk1)
lib.borrow_book(alex, bk1)

# return functionality
lib.return_book(steve, 101)

lib.borrow_book(alex, bk1)


steve.borrow_history()
alex.borrow_history() 