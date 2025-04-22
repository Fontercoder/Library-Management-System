import pandas as pd
import os

BOOKS_FILE = "data/books.csv"

def load_books():
    if os.path.exists(BOOKS_FILE):
        return pd.read_csv(BOOKS_FILE)
    else:
        return pd.DataFrame(columns=["Book Name", "Author", "Genre", "Available Copies"])

def save_books(df):
    df.to_csv(BOOKS_FILE, index=False)
    print("Changes saved to books.csv")

def add_book():
    df = load_books()
    name = input("Book Name: ").strip().title()
    author = input("Author: ").strip().title()
    genre = input("Genre: ").strip().title()

    try:
        copies = int(input("No. of Copies: ").strip())
    except ValueError:
        print("Invalid number of copies.")
        return

    mask = (df["Book Name"] == name) & (df["Author"] == author)

    if mask.any():
        df.loc[mask, "Available Copies"] += copies
        print(f"Added {copies} more copies of '{name}' by {author}.")
    else:
        new_row = pd.DataFrame([[name, author, genre, copies]], columns=df.columns)
        df = pd.concat([df, new_row], ignore_index=True)
        print(f"Book '{name}' by {author} added to inventory.")

    save_books(df)

def update_book():
    df = load_books()
    name = input("Enter Book Name to Update: ").strip().title()
    author = input("Enter Author: ").strip().title()

    mask = (df["Book Name"] == name) & (df["Author"] == author)

    if not mask.any():
        print(" Book not found.")
        return

    print(" What would you like to update?")
    print("1. Genre")
    print("2. Available Copies")
    choice = input("Enter your choice (1/2): ").strip()

    if choice == "1":
        genre = input("New Genre: ").strip().title()
        df.loc[mask, "Genre"] = genre
        print(" Genre updated.")
    elif choice == "2":
        try:
            copies = int(input("New number of copies: "))
            df.loc[mask, "Available Copies"] = copies
            print(" Copies updated.")
        except ValueError:
            print("Invalid number.")
            return
    else:
        print(" Invalid choice.")

    save_books(df)

def delete_book():
    df = load_books()
    name = input(" Enter Book Name to Delete: ").strip().title()
    author = input(" Enter Author: ").strip().title()

    mask = (df["Book Name"] == name) & (df["Author"] == author)

    if not mask.any():
        print(" Book not found.")
        return

    df = df[~mask]
    print(f" Deleted '{name}' by {author} from inventory.")

    save_books(df)

def show_books():
    df = load_books()
    if df.empty:
        print(" No books in inventory.")
    else:
        print("\n Current Book Inventory:")
        print(df.to_string(index=False))

def inventory_menu():
    while True:
        print("\n LIBRARY INVENTORY MENU")
        print("1. Add Book")
        print("2. Update Book")
        print("3. Delete Book")
        print("4. View Inventory")
        print("5. Exit")
        choice = input("Choose an option (1-5): ").strip()

        if choice == "1":
            add_book()
        elif choice == "2":
            update_book()
        elif choice == "3":
            delete_book()
        elif choice == "4":
            show_books()
        elif choice == "5":
            print(" Exiting Inventory Menu.")
            break
        else:
            print("Invalid choice. Try again.")

if __name__ == "__main__":
    inventory_menu()
