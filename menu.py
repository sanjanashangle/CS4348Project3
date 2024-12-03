import os
from index_file import create_index_file, open_index_file, insert_key_value
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


def load_key_value_pairs(input_filename, index_filename):
    """Read a file of comma-separated unsigned integers and insert each pair into the B-tree index."""
    print(f"Loading key-value pairs from {input_filename} into {index_filename}...")
    try:
        with open(input_filename, 'r') as input_file:
            for line_number, line in enumerate(input_file, start=1):
                line = line.strip()
                if not line:
                    continue  # Skip empty lines

                try:
                    # Ensure the line contains exactly two integers
                    parts = line.split(',')
                    if len(parts) != 2:
                        raise ValueError("Line does not contain exactly two values.")
                    
                    key, value = map(int, parts)
                    if key < 0 or value < 0:
                        raise ValueError("Key and value must be unsigned integers.")

                    # Insert the key-value pair into the index file
                    insert_key_value(index_filename, key, value)
                    print(f"Inserted pair (Key: {key}, Value: {value}) from line {line_number}.")
                
                except ValueError as ve:
                    print(f"Skipping line {line_number}: {line} - {ve}")
                    continue

    except FileNotFoundError:
        print(f"Error: Input file '{input_filename}' not found.")
    except Exception as e:
        print(f"An unexpected error occurred: {e}")

def extract_key_value_pairs(index_filename):
    # Prompt for file name
    output_filename = input("Enter the filename to save key-value pairs: ")
    
    # Check if the file exists
    if os.path.exists(output_filename):
        overwrite = input(f"File {output_filename} exists. Do you want to overwrite it? (y/n): ")
        if overwrite.lower() != 'y':
            print("Operation aborted.")
            return

    # Open the output file for writing
    with open(output_filename, 'w') as output_file:
        # Iterate over the nodes in the index and save the key-value pairs
        node_id = 0  # Start with the root node (adjust as per your index structure)
        
        while True:
            node = read_node(index_filename, node_id)  # Read the node from the index file (you'll need to define this function)
            
            # If the node is empty or no longer exists, break the loop
            if not node:
                break
            
            # Write the key-value pairs from the node to the file
            for key, value in zip(node['keys'], node['values']):
                output_file.write(f"{key},{value}\n")
            
            # Move to the next node (this will depend on your tree structure)
            node_id += 1

    print(f"Key-value pairs saved to {output_filename}.")


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
            filename = input("Enter the filename to search in: ")  # Prompt for the filename
            btree.search(filename, key)
        
        elif choice == '5':  # Load Key-Value Pairs from File
            input_filename = input("Enter the name of the file to load from: ")
            index_filename = input("Enter the name of the index file to insert into: ")
            try:
                load_key_value_pairs(input_filename, index_filename)
            except Exception as e:
                print(f"An error occurred: {e}")

        
        elif choice == '6':  # Print Index
            filename = input("Enter the filename to print: ")  # Prompt for the filename
            btree.print_tree(filename)  # Pass the filename to print_tree

        
        elif choice == '7':  # Extract Key-Value Pairs to File
            if not index_filename:  # Check if index_filename is set
                print("Please open or create an index file first.")
            else:
                extract_key_value_pairs(index_filename)
        
        elif choice == '8':  # Quit
            print("Exiting the program.")
            break
        
        else:
            print("Invalid option, please try again.")

if __name__ == "__main__":
    main()
