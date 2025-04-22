import pandas as pd
import os

USERS_FILE = "data/users.csv"

def load_users():
    if os.path.exists(USERS_FILE):
        return pd.read_csv(USERS_FILE)
    else:
        return pd.DataFrame(columns=["User ID", "User Name", "Course", "Books Borrowed"])

def save_users(df):
    df.to_csv(USERS_FILE, index=False)
    print(" Changes saved to users.csv")

def generate_user_id(df):
    if df.empty:
        return "U001"
    else:
        last_id = df["User ID"].iloc[-1]
        new_id = int(last_id[1:]) + 1
        return f"U{new_id:03d}"

def add_user():
    df = load_users()
    name = input("Enter User Name: ").strip().title()
    course = input("Enter Course (BCA/MCA/etc): ").strip().upper()

    user_id = generate_user_id(df)
    new_row = pd.DataFrame([[user_id, name, course, 0]], columns=df.columns)

    df = pd.concat([df, new_row], ignore_index=True)
    print(f" User '{name}' added with ID: {user_id}")

    save_users(df)

def remove_user():
    df = load_users()
    user_id = input(" Enter User ID to Remove: ").strip().upper()

    if user_id in df["User ID"].values:
        df = df[df["User ID"] != user_id]
        print(f" User with ID {user_id} removed.")
        save_users(df)
    else:
        print("User ID not found.")

def search_user():
    df = load_users()
    query = input("Enter User ID or Name to search: ").strip().lower()

    result = df[df["User ID"].str.lower() == query]
    if result.empty:
        result = df[df["User Name"].str.lower().str.contains(query)]

    if result.empty:
        print("No matching user found.")
    else:
        print("\n User(s) found:")
        print(result.to_string(index=False))

def user_menu():
    while True:
        print("\nUSER MANAGEMENT MENU")
        print("1. Add User")
        print("2. Remove User")
        print("3. Search User")
        print("4. Exit")
        choice = input("Enter your choice (1-4): ").strip()

        if choice == "1":
            add_user()
        elif choice == "2":
            remove_user()
        elif choice == "3":
            search_user()
        elif choice == "4":
            print("Exiting User Management.")
            break
        else:
            print("Invalid choice. Try again.")

if __name__ == "__main__":
    user_menu()
