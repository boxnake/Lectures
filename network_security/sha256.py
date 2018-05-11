import math

blocks = []
prime_numbers = []
hash_values = []
constants_k = []
BLOCK_SIZE = 64

def get_prime_numbers(length):
    global prime_numbers
    prime_numbers = [2]
    numb = 2
    while len(prime_numbers) < length:
        for i in range(2,numb):
            if numb % i == 0:
                break
            elif i == numb-1:
                prime_numbers.append(numb)
        numb += 1

def padding_msg(msg):
    padding_size = 64 - ((len(msg)+8) % 64)
    total_length = (len(msg)*8).to_bytes(8, byteorder='big')
    padding_bytes = (128).to_bytes(1, byteorder='big') + bytes(padding_size-1)
    msg = msg + padding_bytes + total_length
    return msg

def slice_into_blocks(input_data):
    global blocks
    blocks = []
    block_length = len(input_data)/64
    for i in range(int(block_length)):
        blocks.append(input_data[0+(i*64):64+(i*64)])

def get_fraction_part_bytes(real_num):
    exp = real_num.hex().split('p')[-1]
    exp = int(exp)
    fraction = real_num.hex().split('p')[0].split('.')[-1]
    fraction = bytes.fromhex(fraction[:-1])
    fraction = int.from_bytes(fraction, byteorder='big')
    if exp > 0:
        fraction = fraction << exp
    elif exp < 0:
        fraction = fraction >> exp
    fraction = fraction.to_bytes(7, byteorder='big')
    fraction = fraction.hex()
    fraction = fraction[2:]
    fraction = fraction[0:8]
    result = bytes.fromhex(fraction)
    return result
    

def initialize_initial_hash_value():
    global hash_values
    get_prime_numbers(8)
    hash_values = []
    for prime in prime_numbers:
        square_root = prime**(1./2.)
        hash_values.append(get_fraction_part_bytes(square_root))

def initialize_constants():
    global constants_k
    get_prime_numbers(64)
    constants_k = []
    for prime in prime_numbers:
        cube_root = prime**(1./3.)
        constants_k.append(get_fraction_part_bytes(cube_root))

def file_read(file_name):
    with open(file_name, 'br') as f:
        file_content = f.read()
        padded_msg = padding_msg(file_content)
        slice_into_blocks(padded_msg)
        initialize_initial_hash_value()
        initialize_constants()


def choose_function(x,y,z):
    result = xor_bytes(and_bytes(x,y), and_bytes(not_bytes(x),z))
    return result

def majority_function(x,y,z):
    result = xor_bytes(xor_bytes(and_bytes(x,y),and_bytes(x,z)), and_bytes(y,z))
    return result

def large_sigma_zero(x):
    result = xor_bytes(rotation_right(x,2), rotation_right(x,13))
    result = xor_bytes(result, rotation_right(x,22))
    return result

def large_sigma_one(x):
    result = xor_bytes(rotation_right(x,6), rotation_right(x,11))
    result = xor_bytes(result, rotation_right(x,25))
    return result

def small_sigma_zero(x):
    result = xor_bytes(rotation_right(x,7), rotation_right(x,18))
    result = xor_bytes(result, shift_right(x, 3))
    return result

def small_sigma_one(x):
    result = xor_bytes(rotation_right(x,17), rotation_right(x,19))
    result = xor_bytes(result, shift_right(x,10))
    return result

def xor_bytes(a,b):
    a = int.from_bytes(a, byteorder='big')
    b = int.from_bytes(b, byteorder='big')
    result = a ^ b
    result = (result).to_bytes(4, byteorder='big')
    return result

def and_bytes(a,b):
    a = int.from_bytes(a, byteorder='big')
    b = int.from_bytes(b, byteorder='big')
    result = a & b
    result = (result).to_bytes(4, byteorder='big')
    return result

def not_bytes(x):
    max_32 = b'\xff\xff\xff\xff'
    result = xor_bytes(x, max_32)
    return result

def rotation_right(word, offset):
    result = int.from_bytes(word, byteorder='big')
    for i in range(offset):
        last_bit = result & 1
        last_bit = last_bit << 31
        result = result >> 1
        result = result | last_bit
    result = (result).to_bytes(4, byteorder='big')
    return result

def shift_right(word, offset):
    result = int.from_bytes(word, byteorder='big')
    result = result >> offset
    result = (result).to_bytes(4, byteorder='big')
    return result

def mod_32_addition(a,b):
    int_a = int.from_bytes(a, byteorder='big')
    int_b = int.from_bytes(b, byteorder='big')
    result = (int_a + int_b) % (2**32)
    result = (result).to_bytes(4, byteorder='big')
    return result

def word_expansion(block):
    result = []
    for i in range(16):
        result.append(block[0+(4*i):4+(4*i)])
    for t in range(16,64):
        word = mod_32_addition(small_sigma_one(result[t-2]), result[t-7])
        word = mod_32_addition(word, small_sigma_zero(result[t-15]))
        word = mod_32_addition(word, result[t-16])
        result.append(word)
    return result

def compute_working_variables(words,a,b,c,d,e,f,g,h):
    for t in range(64):
        T1 = mod_32_addition(h, large_sigma_one(e))
        T1 = mod_32_addition(T1, choose_function(e,f,g))
        T1 = mod_32_addition(T1, constants_k[t])
        T1 = mod_32_addition(T1, words[t])
        T2 = mod_32_addition(large_sigma_zero(a), majority_function(a,b,c))
        h = g
        g = f
        f = e
        e = mod_32_addition(d, T1)
        d = c
        c = b
        b = a
        a = mod_32_addition(T1, T2)
    return (a,b,c,d,e,f,g,h)

def compute_intermediate_hash_value(a,b,c,d,e,f,g,h):
    global hash_values
    hash_values[0] = mod_32_addition(a, hash_values[0])
    hash_values[1] = mod_32_addition(b, hash_values[1])
    hash_values[2] = mod_32_addition(c, hash_values[2])
    hash_values[3] = mod_32_addition(d, hash_values[3])
    hash_values[4] = mod_32_addition(e, hash_values[4])
    hash_values[5] = mod_32_addition(f, hash_values[5])
    hash_values[6] = mod_32_addition(g, hash_values[6])
    hash_values[7] = mod_32_addition(h, hash_values[7])
        
def hash_computation():
    global blocks
    for i in range(len(blocks)):
        words = word_expansion(blocks[i])
        (a,b,c,d,e,f,g,h) = (hash_values)
        (a,b,c,d,e,f,g,h) = compute_working_variables(words, a, b, c, d, e, f, g, h)
        compute_intermediate_hash_value(a,b,c,d,e,f,g,h)


def print_result():
    print('result :', end='')
    for value in hash_values:
        print(' {0}'.format(value.hex()), end='')
    print()

def get_hash_digest_from_file(file_name):
    file_read(file_name)
    hash_computation()
    ret_bytes = bytes()
    for h in hash_values:
        ret_bytes += h
    return ret_bytes

def get_hash_digest_from_bytes(input_bytes):
    padded_msg = padding_msg(input_bytes)
    slice_into_blocks(padded_msg)
    initialize_initial_hash_value()
    initialize_constants()
    hash_computation()
    ret_bytes = bytes()
    for h in hash_values:
        ret_bytes += h
    return ret_bytes


if __name__ == "__main__":
    file_read('sample.txt')
    hash_computation()
    print_result()