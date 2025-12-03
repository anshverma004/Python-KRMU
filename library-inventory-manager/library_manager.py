import json
import os
from pathlib import Path

class Book:
    def __init__(self, title, author, isbn, status="available"):
        self.title = title.strip()
        self.author = author.strip()
        self.isbn = isbn.strip()
        self.status = status
        
    def __str__(self):
        return f"{self.title} by {self.author} | {self.isbn} | {self.status}"
    
    def to_dict(self):
        return {'title': self.title, 'author': self.author, 'isbn': self.isbn, 'status': self.status}
    
    def issue(self):
        if self.status == "available":
            self.status = "issued"
            return True
        return False
    
    def return_book(self):
        if self.status == "issued":
            self.status = "available"
            return True
        return False

class LibraryInventory:
    def __init__(self, filename="books.json"):
        self.filename = filename
        self.books = []
        self.load_books()
    
    def load_books(self):
        if os.path.exists(self.filename):
            try:
                with open(self.filename, 'r') as f:
                    data = json.load(f)
                self.books = [Book(b['title'], b['author'], b['isbn'], b['status']) for b in data]
                print(f"✅ Loaded {len(self.books)} books")
            except:
                print("⚠️  Starting fresh (corrupted file)")
                self.books = []
        else:
            print("📭 No saved books found")
    
    def save_books(self):
        try:
            data = [book.to_dict() for book in self.books]
            with open(self.filename, 'w') as f:
                json.dump(data, f, indent=2)
            print("💾 Saved to books.json")
        except Exception as e:
            print(f"❌ Save error: {e}")
    
    def add_book(self, title, author, isbn):
        book = Book(title, author, isbn)
        self.books.append(book)
        self.save_books()
        return book
    
    def find_by_isbn(self, isbn):
        for book in self.books:
            if book.isbn == isbn:
                return book
        return None
    
    def find_by_title(self, keyword):
        return [b for b in self.books if keyword.lower() in b.title.lower()]
    
    def show_all(self):
        return self.books

# === MAIN PROGRAM ===
def main():
    inventory = LibraryInventory()
    
    while True:
        print("\n" + "="*50)
        print("📚 LIBRARY MANAGER")
        print("="*50)
        print("1. Add Book     2. Show All")
        print("3. Issue Book   4. Return Book") 
        print("5. Search       6. Exit")
        print("-"*50)
        
        choice = input("Choose (1-6): ").strip()
        
        if choice == '1':
            title = input("Title: ").strip()
            author = input("Author: ").strip()
            isbn = input("ISBN: ").strip()
            if title and author and isbn:
                book = inventory.add_book(title, author, isbn)
                print(f"✅ Added: {book}")
            else:
                print("❌ Fill all fields!")
                
        elif choice == '2':
            books = inventory.show_all()
            if books:
                print(f"\n📚 {len(books)} books:")
                for i, b in enumerate(books, 1):
                    print(f"{i}. {b}")
            else:
                print("📭 No books")
                
        elif choice == '3':
            isbn = input("ISBN to issue: ").strip()
            book = inventory.find_by_isbn(isbn)
            if book and book.issue():
                inventory.save_books()
                print("✅ Issued!")
            else:
                print("❌ Not found or already issued")
                
        elif choice == '4':
            isbn = input("ISBN to return: ").strip()
            book = inventory.find_by_isbn(isbn)
            if book and book.return_book():
                inventory.save_books()
                print("✅ Returned!")
            else:
                print("❌ Not found or not issued")
                
        elif choice == '5':
            keyword = input("Search title: ").strip()
            results = inventory.find_by_title(keyword)
            if results:
                print(f"\n📖 Found {len(results)} books:")
                for b in results:
                    print(f"  • {b}")
            else:
                print("❌ No matches")
                
        elif choice == '6':
            print("👋 Bye!")
            break
            
        else:
            print("❌ Choose 1-6!")
        
        input("\n[Press Enter]")

if __name__ == "__main__":
    main()
