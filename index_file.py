import os
import struct

# Constants for the file structure
MAGIC_NUMBER = b"4337PRJ3"  # 8-byte magic number
BLOCK_SIZE = 512  # Each block is 512 bytes
HEADER_FORMAT = '8s Q Q'  # Magic number, root node ID, next block ID
NODE_FORMAT = 'Q Q Q 152s 152s 160s'  # Block ID, Parent ID, num keys, keys, values, children

HEADER_SIZE = struct.calcsize(HEADER_FORMAT)
NODE_SIZE = struct.calcsize(NODE_FORMAT)

def create_index_file(filename):
    """Create a new index file with a header block."""
    if os.path.exists(filename):
        overwrite = input(f"The file {filename} already exists. Do you want to overwrite it? (y/n): ")
        if overwrite.lower() != 'y':
            return
    
    with open(filename, 'wb') as f:
        header = struct.pack(HEADER_FORMAT, MAGIC_NUMBER, 0, 1)  # Magic, Root ID (0), Next Block ID (1)
        f.write(header)
    
    print(f"Index file {filename} created.")

def open_index_file(filename):
    """Open an existing index file."""
    if not os.path.exists(filename):
        print("Error: File does not exist.")
        return None
    
    with open(filename, 'rb') as f:
        header = f.read(HEADER_SIZE)
        magic_number, root_block_id, next_block_id = struct.unpack(HEADER_FORMAT, header)
        
        if magic_number != MAGIC_NUMBER:
            print("Error: Invalid file format (magic number mismatch).")
            return None
        
        return root_block_id, next_block_id

def insert_key_value(filename, key, value):
    """Insert a key-value pair into the index file."""
    with open(filename, 'rb+') as f:
        # Read the header
        f.seek(0)
        header = f.read(HEADER_SIZE)
        magic_number, root_block_id, next_block_id = struct.unpack(HEADER_FORMAT, header)

        # Ensure keys and values are packed correctly
        key_packed = struct.pack('Q', key) + b'\0' * (152 - 8)  # 152 bytes for key
        value_packed = struct.pack('Q', value) + b'\0' * (152 - 8)  # 152 bytes for value
        children = b'\0' * 160  # Placeholder for child pointers

        # Pack the node with key-value pair (1 key, 1 value)
        node_data = struct.pack(
            NODE_FORMAT, next_block_id, root_block_id, 1, key_packed, value_packed, children
        )

        # Print before padding
        print(f"Node data before padding: {node_data[:100]}...")  # Print the first 100 bytes of packed node data

        # Pad to fill the block size (512 bytes)
        node_data = node_data + b'\0' * (BLOCK_SIZE - len(node_data))  # Pad to 512 bytes

        # Print after padding
        print(f"Node data after padding: {node_data[:100]}...")  # Print the first 100 bytes of packed node data

        # Write the new node to the file at the next available block
        f.seek(next_block_id * BLOCK_SIZE)
        f.write(node_data)

        # Update the header with the new next_block_id
        f.seek(0)
        new_header = struct.pack(HEADER_FORMAT, MAGIC_NUMBER, root_block_id, next_block_id + 1)
        f.write(new_header)

        print(f"Key-value pair ({key}, {value}) inserted into the index.")

def print_index(filename):
    """Print all the key-value pairs in the index file."""
    with open(filename, 'rb') as f:
        # Print the header first
        f.seek(0)
        header = f.read(HEADER_SIZE)
        magic_number, root_block_id, next_block_id = struct.unpack(HEADER_FORMAT, header)
        print(f"Header: Magic Number: {magic_number}, Root Block ID: {root_block_id}, Next Block ID: {next_block_id}")
        
        # Then, read and print each node
        f.seek(BLOCK_SIZE)  # Start after the header
        while True:
            node_data = f.read(BLOCK_SIZE)  # Read 512 bytes for a block (including padding)
            if not node_data:
                break  # Exit if no more data is available
            
            # Ensure that we have exactly 512 bytes before unpacking
            if len(node_data) != BLOCK_SIZE:
                print(f"Warning: Skipping block of size {len(node_data)} bytes (expected {BLOCK_SIZE} bytes).")
                continue
            
            block_id, parent_id, num_keys, keys, values, children = struct.unpack(NODE_FORMAT, node_data)

            # Decode the keys and remove padding
            keys = keys.strip(b'\0')  # Remove padding
            print(f"Node {block_id} (Parent: {parent_id}):")
            print(f"  Keys: {keys.decode(errors='ignore')}")  # Use 'ignore' to skip invalid characters

            # Print values as raw bytes (since they are not text)
            print(f"  Values: {values[:num_keys*8]}")  # Print only valid number of values based on num_keys
            # Print children as raw data
            print(f"  Children: {children[:(num_keys + 1) * 8]}")  # Assuming 8-byte IDs for children
