import os
from index_file import create_index_file, open_index_file, insert_key_value, MAGIC_NUMBER, print_index
from btree import BTree
import struct 

# Create an instance of the BTree class
btree = BTree()

# Global variable to store the index filename
index_filename = ""

def print_menu():
    """Display the menu options."""
    print("\n--- B-Tree Index File Menu ---")
    print("CREATE   : Create a new index file")
    print("OPEN     : Open an existing index file")
    print("INSERT   : Insert a key-value pair")
    print("SEARCH   : Search for a key")
    print("LOAD     : Load key-value pairs from a file")
    print("PRINT    : Print the key-value pairs in the index")
    print("EXTRACT  : Extract key-value pairs to a file")
    print("QUIT     : Exit the program")

def open_index_file(filename):
    """Open an existing B-Tree index file."""
    try:
        with open(filename, 'rb') as f:
            # Read the magic number from the header
            magic_number = f.read(8)
            
            # Check if the magic number is valid
            if magic_number != MAGIC_NUMBER:
                print(f"Error: Invalid magic number in {filename}.")
                return None
            
            # If the magic number matches, return a success message
            print(f"Index file {filename} opened successfully.")
            return filename  # Return the filename to indicate the file is opened

    except FileNotFoundError:
        print(f"Error: The file {filename} does not exist.")
        return None

def load_key_value_pairs_from_binary(file_name):
    try:
        with open(file_name, 'rb') as f:
            while True:
                # Read the key and value (assuming they are both 8-byte integers)
                data = f.read(16)  # Read 16 bytes (8 for key, 8 for value)
                if len(data) < 16:  # End of file or incomplete data
                    break
                
                # Unpack the data into key and value (assuming big-endian format)
                key, value = struct.unpack('>QQ', data)  # 'Q' is for unsigned long long (8 bytes)
                
                if key == 0 and value == 0:
                    print("Warning: Invalid pair (0, 0) found, skipping.")
                    continue
                
                # Insert the key-value pair into the index
                insert_key_value(file_name, key, value)

    except FileNotFoundError:
        print(f"Error: The file {file_name} does not exist.")
    except Exception as e:
        print(f"Error loading binary file: {e}")


import os

def load_key_value_pairs(filename_to_load, target_filename):
    """Load key-value pairs from a file, either binary or text."""
    print(f"Loading key-value pairs from {filename_to_load} into {target_filename}...")

    try:
        # Try to open the file as a binary file
        with open(filename_to_load, 'rb') as file:
            # Attempt to read the first few bytes to determine if it's binary
            initial_data = file.read(16)

            # If it contains only numeric values that can be converted from bytes, treat it as binary
            try:
                # Check if the first 16 bytes can be unpacked as key-value pairs (assuming 8-byte key-value pairs)
                if len(initial_data) == 16:
                    load_key_value_pairs_from_binary(filename_to_load)  # Call the binary loading function
                    return
            except Exception:
                pass  # If it fails, assume it is not a binary format

        # If the file was not binary, try reading it as a text file
        with open(filename_to_load, 'r') as load_file:
            count = 0  # To count invalid (0, 0) pairs
            for line in load_file:
                # Read key-value pairs in text format (comma-separated)
                key, value = map(int, line.strip().split(','))

                if key == 0 and value == 0:
                    count += 1
                    if count > 10:  # Stop after 10 consecutive (0, 0) pairs
                        print("Warning: Too many invalid (0, 0) pairs encountered. Stopping loading.")
                        break
                    continue  # Skip invalid pair and continue to next read
                
                # Reset invalid pair counter if a valid pair is found
                count = 0

                # Insert the key-value pair into the target index file
                insert_key_value(target_filename, key, value)

        print("Key-value pairs loaded successfully.")

    except FileNotFoundError:
        print(f"Error: File '{filename_to_load}' not found.")
    except ValueError as e:
        print(f"Error processing file content: {e}")
    except Exception as e:
        print(f"An unexpected error occurred: {e}")


def extract_key_value_pairs(index_filename):
    """Extract key-value pairs from the index file and save them to an output file."""
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
    current_file = None  # Start with no file open
    btree = BTree()
    
    while True:

        print_menu()
        command = input("Choose an option: ").strip().lower()

        if command == "create":
            filename = input("Enter the filename to create: ").strip()
            new_file = create_index_file(filename)
            if new_file:
                current_file = new_file  # Update the currently open file

        elif command == "open":
            filename = input("Enter the filename to open: ").strip()
            current_file = open_index_file(filename)
            if current_file:
                print(f"Current file set to {current_file}")
            else:
                print("Failed to open the file.")
        
        elif command == "insert":
            if current_file is None:
                print("Error: No index file is currently open.")
            else:
                key = int(input("Enter the key (unsigned integer): "))
                value = int(input("Enter the value (unsigned integer): "))
                insert_key_value(current_file, key, value)
        elif command == "search":
            if current_file is None:
                print("Error: No index file is currently open.")
            else:
                key = int(input("Enter the key to search for: "))
                btree.search(current_file, key)
        elif command == "load":
            if not current_file:
                print("Error: No index file is currently open.")
                continue
            filename_to_load = input("Enter the name of the file to load from: ").strip()
            # Call the load function to insert key-value pairs from the source file
            load_key_value_pairs(filename_to_load, current_file)
        elif command == "print":
            if current_file is None:
                print("Error: No index file is currently open.")
            else:
                print_index(current_file)
        elif command == "extract":
            if current_file is None:
                print("Error: No index file is currently open.")
            else:
                extract_file = input("Enter the name of the file to save to: ").strip()
                extract_key_value_pairs(current_file, extract_file)
        elif command == "quit":
            print("Exiting the program. Goodbye!")
            break
        else:
            print("Invalid command. Please try again.")

if __name__ == "__main__":
    main()