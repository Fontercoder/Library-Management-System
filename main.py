from core import inventory as inv
from core import user_management as um

choice = None
while choice != "0":
    print("\nLibrary Management System")
    print("1. Manage Books Inventory")
    print("2. Manage  users")
    print("3. Delete Book")
    print("4. View All Books")
    print("5. Search Book")
    print("0. Exit")

    choice = input("Enter your choice: ").strip()

    if choice == "1":
        inv.inventory_menu()
    elif choice == "2":
        um.user_menu()
    elif choice == "3":
        inv.delete_book()
    elif choice == "4":
        inv.view_books()
    elif choice == "5":
        inv.search_book()
    elif choice == "0":
        print("Exiting...")
    else:
        print("Invalid choice, please try again.")
