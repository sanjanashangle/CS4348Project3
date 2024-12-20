import os
import struct

MAGIC_NUMBER = b"4337PRJ3"  # 8-byte magic number
BLOCK_SIZE = 512  # Each block is 512 bytes
HEADER_FORMAT = '8s Q Q'  # Magic number, root node ID, next block ID
NODE_FORMAT = 'Q Q Q 152s 152s 160s'  # Block ID, Parent ID, num keys, keys, values, children

HEADER_SIZE = struct.calcsize(HEADER_FORMAT)
NODE_SIZE = struct.calcsize(NODE_FORMAT)

def create_index_file(filename):
    """Create a new B-Tree index file."""
    import os

    if os.path.exists(filename):
        overwrite = input(f"The file '{filename}' already exists. Do you want to overwrite it? (yes/no): ").strip().lower()
        if overwrite != "yes":
            print(f"File '{filename}' was not overwritten.")
            return None

    with open(filename, 'wb') as f:
        magic_number = MAGIC_NUMBER
        root_block_id = 1  
        next_block_id = 2  
        header = struct.pack(HEADER_FORMAT, magic_number, root_block_id, next_block_id)
        f.write(header)

        block_id = 1
        parent_id = 0
        num_keys = 0
        raw_keys = b'\0' * 152
        raw_values = b'\0' * 152
        raw_children = b'\0' * 160
        root_node = struct.pack(
            NODE_FORMAT,
            block_id,
            parent_id,
            num_keys,
            raw_keys,
            raw_values,
            raw_children
        )
        f.write(root_node)

    print(f"Index file {filename} created.")
    return filename 


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
        f.seek(0)
        header = f.read(HEADER_SIZE)
        magic_number, root_block_id, next_block_id = struct.unpack(HEADER_FORMAT, header)

        key_packed = struct.pack('Q', key) + b'\0' * (152 - 8)  # 152 bytes for key
        value_packed = struct.pack('Q', value) + b'\0' * (152 - 8)  # 152 bytes for value
        children = b'\0' * 160  # Placeholder for child pointers

        node_data = struct.pack(
            NODE_FORMAT, next_block_id, root_block_id, 1, key_packed, value_packed, children
        )

        node_data = node_data + b'\0' * (BLOCK_SIZE - len(node_data))  

        f.seek(next_block_id * BLOCK_SIZE)
        f.write(node_data)

        f.seek(0)
        new_header = struct.pack(HEADER_FORMAT, MAGIC_NUMBER, root_block_id, next_block_id + 1)
        f.write(new_header)

        print(f"Key-value pair ({key}, {value}) inserted into the index.")


def print_index(filename):
    """Print the B-Tree index structure."""
    with open(filename, 'rb') as f:
        f.seek(0)
        header = f.read(HEADER_SIZE)
        magic_number, root_block_id, next_block_id = struct.unpack(HEADER_FORMAT, header)
        print(f"Header: Magic Number: {magic_number}, Root Block ID: {root_block_id}, Next Block ID: {next_block_id}")

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
                children = [
                    int.from_bytes(raw_children[i:i+8], 'little')
                    for i in range(0, (num_keys + 1) * 8, 8)
                ]

                print(f"Node {block_id} (Parent: {parent_id}):")
                print(f"  Keys: {keys}")
                print(f"  Values: {values}")
                # print(f"  Children: {children}")
            except struct.error as e:
                print(f"Error unpacking node {block_id}: {e}. Data: {node_data[:64]}...")
