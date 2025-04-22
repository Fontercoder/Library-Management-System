import pandas as pd
import os
from datetime import datetime

BOOKS_FILE = "data/books.csv"
USERS_FILE = "data/users.csv"
TRANSACTIONS_FILE = "data/transactions.csv"

# Load or create empty DataFrames if files are missing
def load_csv(file, columns):
    return pd.read_csv(file) if os.path.exists(file) else pd.DataFrame(columns=columns)

def save_csv(df, file):
    df.to_csv(file, index=False)

def issue_book():
    books = load_csv(BOOKS_FILE, ["Book Name", "Author", "Genre", "Available Copies"])
    users = load_csv(USERS_FILE, ["User ID", "User Name", "Course", "Books Borrowed"])
    transactions = load_csv(TRANSACTIONS_FILE, ["Transaction ID", "User ID", "Book Name", "Date", "Type"])

    user_id = input("👤 Enter User ID: ").strip().upper()
    book_name = input("📘 Enter Book Name to Issue: ").strip().title()

    # Check user exists
    if user_id not in users["User ID"].values:
        print(" User not found.")
        return

    # Check book exists and is available
    if book_name not in books["Book Name"].values:
        print(" Book not found in inventory.")
        return

    book_row = books[books["Book Name"] == book_name]
    available = int(book_row["Available Copies"].values[0])
    if available <= 0:
        print(" No copies available for this book.")
        return

    # Update books.csv
    books.loc[books["Book Name"] == book_name, "Available Copies"] = available - 1

    # Update users.csv
    users.loc[users["User ID"] == user_id, "Books Borrowed"] += 1

    # Add to transactions.csv
    trans_id = f"T{len(transactions) + 1:04d}"
    today = datetime.now().strftime("%Y-%m-%d")
    new_transaction = pd.DataFrame([[trans_id, user_id, book_name, today, "Issue"]],
                                   columns=transactions.columns)
    transactions = pd.concat([transactions, new_transaction], ignore_index=True)

    save_csv(books, BOOKS_FILE)
    save_csv(users, USERS_FILE)
    save_csv(transactions, TRANSACTIONS_FILE)

    print(f" Book '{book_name}' issued to {user_id} on {today}.")

def return_book():
    books = load_csv(BOOKS_FILE, ["Book Name", "Author", "Genre", "Available Copies"])
    users = load_csv(USERS_FILE, ["User ID", "User Name", "Course", "Books Borrowed"])
    transactions = load_csv(TRANSACTIONS_FILE, ["Transaction ID", "User ID", "Book Name", "Date", "Type"])

    user_id = input("👤 Enter User ID: ").strip().upper()
    book_name = input(" Enter Book Name to Return: ").strip().title()

    # Check user exists
    if user_id not in users["User ID"].values:
        print(" User not found.")
        return

    # Check book exists
    if book_name not in books["Book Name"].values:
        print(" Book not found in inventory.")
        return

    # Update books.csv
    books.loc[books["Book Name"] == book_name, "Available Copies"] += 1

    # Update users.csv
    users.loc[users["User ID"] == user_id, "Books Borrowed"] -= 1

    # Add return to transactions.csv
    trans_id = f"T{len(transactions) + 1:04d}"
    today = datetime.now().strftime("%Y-%m-%d")
    new_transaction = pd.DataFrame([[trans_id, user_id, book_name, today, "Return"]],columns=transactions.columns)
    transactions = pd.concat([transactions, new_transaction], ignore_index=True)

    save_csv(books, BOOKS_FILE)
    save_csv(users, USERS_FILE)
    save_csv(transactions, TRANSACTIONS_FILE)

    print(f"✅ Book '{book_name}' returned by {user_id} on {today}.")

def menu():
    while True:
        print("\n ISSUE/RETURN MENU")
        print("1. Issue Book")
        print("2. Return Book")
        print("3. Exit")
        choice = input("Enter your choice: ").strip()

        if choice == "1":
            issue_book()
        elif choice == "2":
            return_book()
        elif choice == "3":
            print(" Exiting Issue/Return system.")
            break
        else:
            print(" Invalid choice. Try again.")

if __name__ == "__main__":
    menu()
