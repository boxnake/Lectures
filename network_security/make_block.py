import sha256
import time

# global variables
block_size = 0
block_size_field = bytes()
entire_block = bytes()
block_header = bytes()
contents = bytes()
version = b'\x00' * 4
prev_block_hash = b'\x00' * 32
contents_hash = bytes()
time_stamp = bytes()
difficulty = b'\xff' * 4
nonce = b'\x00' * 4
comment = b'\x00' * 20

def set_block_size_field():
    global block_size, block_size_field
    block_size_field = (block_size).to_bytes(4, byteorder='little')

def set_contents_hash(contents_file_name):
    global contents_hash
    contents_hash = sha256.get_hash_digest_from_bytes(sha256.get_hash_digest_from_file(contents_file_name))

def set_time_stamp(_time):
    global time_stamp
    time_stamp = int(_time).to_bytes(4, byteorder='little')

def make_block_header():
    global block_header, contents_hash
    block_header = bytes()
    block_header += version
    block_header += prev_block_hash
    block_header += contents_hash
    block_header += time_stamp
    block_header += difficulty
    block_header += nonce
    block_header += comment

def get_header_hash_from_entire_block(_comment, _nonce, _time):
    global comment, nonce
    comment = _comment
    nonce = _nonce
    with open('contents.txt', 'br') as f:
        contents = f.read()
        block_size = 100 + len(contents)
    set_block_size_field()
    set_contents_hash("contents.txt")
    set_time_stamp(_time)
    make_block_header()
    entire_block = block_size_field + block_header + contents

    hash_value = sha256.get_hash_digest_from_bytes(sha256.get_hash_digest_from_bytes(block_header))
    return hash_value
    
if __name__ == "__main__":
    with open('contents.txt', 'br') as f:
        contents = f.read()
        block_size = 100 + len(contents)
        print('len(contents):{}'.format(len(contents)))
    set_block_size_field()
    set_contents_hash("contents.txt")
    set_time_stamp(time.time())
    make_block_header()
    entire_block = block_size_field + block_header + contents

    hash_value = sha256.get_hash_digest_from_bytes(sha256.get_hash_digest_from_bytes(block_header))
    for i in range(8):
        print('{}'.format(hash_value[i*4:(i+1)*4].hex()), end=' ')