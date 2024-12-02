# Import necessary functions from index_file
from index_file import insert_key_value, print_index

class BTree:
    def __init__(self):
        self.root = None
        self.nodes = {}

    def insert(self, filename, key, value):
        """Insert a key-value pair into the B-tree."""
        # Insert logic for B-tree, here it's simplified for the example
        print(f"Inserting key-value pair: ({key}, {value})")
        insert_key_value(filename, key, value)

    def search(self, key):
        """Search for a key in the B-tree."""
        print(f"Searching for key: {key}")
        # Add search logic to find key-value pair
        # For simplicity, just print the index content
        print_index('index_file.dat')

    def print_tree(self, filename):
        """Print the entire B-tree."""
        print_index(filename)
