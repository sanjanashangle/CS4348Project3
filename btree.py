from index_file import insert_key_value, print_index, HEADER_SIZE, HEADER_FORMAT, NODE_FORMAT, BLOCK_SIZE, NODE_SIZE, MAGIC_NUMBER
import struct

class BTree:
    def __init__(self):
        self.root = None
        self.nodes = {}

    def insert(self, filename, key, value):
        """Insert a key-value pair into the B-tree."""
        # Insert logic for B-tree, here it's simplified for the example
        print(f"Inserting key-value pair: ({key}, {value})")
        insert_key_value(filename, key, value)


    def search(self, filename, key):
        """Search for a key in the B-tree."""
        print(f"Searching for key: {key} in {filename}")
        try:
            with open(filename, 'rb') as f:
    
                header = f.read(HEADER_SIZE)
                magic_number, root_block_id, next_block_id = struct.unpack(HEADER_FORMAT, header)
                if magic_number != MAGIC_NUMBER:
                    print("Error: Invalid file format (magic number mismatch).")
                    return
            
                print(f"Header: Magic Number: {magic_number}, Root Block ID: {root_block_id}, Next Block ID: {next_block_id}")
            
                #Traverse the nodes
                for block_id in range(root_block_id, next_block_id):
                    f.seek(block_id * BLOCK_SIZE)
                    node_data = f.read(BLOCK_SIZE)
                
                    try:
                        block_id, parent_id, num_keys, raw_keys, raw_values, raw_children = struct.unpack(NODE_FORMAT, node_data[:NODE_SIZE])
                    
                        keys = [
                            int.from_bytes(raw_keys[i:i+8], 'little')
                            for i in range(0, num_keys * 8, 8)
                        ]
                        values = [
                            int.from_bytes(raw_values[i:i+8], 'little')
                            for i in range(0, num_keys * 8, 8)
                        ]
                    
                        #Search for key
                        if key in keys:
                            value_index = keys.index(key)
                            value = values[value_index]
                            print(f"Found Key: {key}, Value: {value} in Node {block_id}")
                            return
                    except struct.error as e:
                        print(f"Error unpacking node {block_id}: {e}. Data: {node_data[:64]}...")
            
                print(f"Key {key} not found.")
        except FileNotFoundError:
            print(f"Error: File '{filename}' does not exist.")
        except Exception as e:
            print(f"An error occurred: {e}")



    def print_tree(self, filename):
        """Print the entire B-tree."""
        print_index(filename)



