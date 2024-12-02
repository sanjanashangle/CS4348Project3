import os
from index_file import create_index_file, open_index_file
from btree import BTree

# Create an instance of the BTree class
btree = BTree()

def print_menu():
    """Display the menu options."""
    print("\n--- B-Tree Index File Menu ---")
    print("1. Create Index File")
    print("2. Open Index File")
    print("3. Insert Key-Value Pair")
    print("4. Search Key")
    print("5. Load Key-Value Pairs from File")
    print("6. Print Index")
    print("7. Extract Key-Value Pairs to File")
    print("8. Quit")

def load_key_value_pairs():
    """Load key-value pairs from a file and insert them into the BTree."""
    file_name = input("Enter the name of the file to load from: ")
    try:
        with open(file_name, "r") as file:
            for line in file:
                key, value = map(int, line.strip().split(','))
                btree.insert(key, value)  # Assuming insert is a method of BTree class
        print(f"Successfully loaded key-value pairs from {file_name}.")
    except FileNotFoundError:
        print(f"Error: {file_name} not found.")
    except ValueError:
        print("Error: Invalid format in file.")

def extract_key_value_pairs():
    """Extract all key-value pairs to a file."""
    file_name = input("Enter the name of the file to extract to: ")
    try:
        with open(file_name, "w") as file:
            for key, value in btree.get_all_key_value_pairs():  # Assuming get_all_key_value_pairs is a method of BTree
                file.write(f"{key},{value}\n")
        print(f"Successfully extracted key-value pairs to {file_name}.")
    except IOError:
        print("Error: Could not write to file.")

def main():
    while True:
        print_menu()
        choice = input("Choose an option: ").strip().lower()
        
        if choice == '1':  # Create Index File
            filename = input("Enter the filename to create: ")
            create_index_file(filename)
        
        elif choice == '2':  # Open Index File
            filename = input("Enter the filename to open: ")
            open_index_file(filename)
        
        elif choice == '3':  # Insert Key-Value Pair
            key = int(input("Enter the key (unsigned integer): "))
            value = int(input("Enter the value (unsigned integer): "))
            filename = input("Enter the filename to insert into: ")  # Prompt for the filename
            btree.insert(filename, key, value)  # Use the correct filename here

        
        elif choice == '4':  # Search Key
            key = int(input("Enter the key to search for: "))
            btree.search(key)
        
        elif choice == '5':  # Load Key-Value Pairs from File
            load_key_value_pairs()
        
        elif choice == '6':  # Print Index
            filename = input("Enter the filename to print: ")  # Prompt for the filename
            btree.print_tree(filename)  # Pass the filename to print_tree

        
        elif choice == '7':  # Extract Key-Value Pairs to File
            extract_key_value_pairs()
        
        elif choice == '8':  # Quit
            print("Exiting the program.")
            break
        
        else:
            print("Invalid option, please try again.")

if __name__ == "__main__":
    main()
