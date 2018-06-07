import sha256
import make_block
import time
import sys

MY_NAME = "KimTaeJeong"
MAX_INT = int.from_bytes(b"\xff\xff\xff\xff", byteorder='big')

def make_comment_into_bytes(comment_string):
    if len(comment_string) > 20:
        ret_bytes = comment_string[0:20].encode('ascii')
    else:
        ret_bytes = comment_string.encode('ascii')
        for i in range(20-len(comment_string)):
            ret_bytes += b"\x00"
    return ret_bytes


def make_nonce_into_bytes(nonce_int):
    ret_bytes = (nonce_int).to_bytes(4, byteorder='big')
    return ret_bytes


def checkMiningSuccess(comment, nonce, condition_length, time_field):
    hash_int_arr = []
    hash_value = make_block.get_header_hash_from_entire_block(make_comment_into_bytes(comment), make_nonce_into_bytes(nonce), time_field)
    for i in range(8):
        hash_int_arr.append(int.from_bytes(hash_value[i*4:(i+1)*4], byteorder='big'))
    for i in range(int(((condition_length-1)/32)+1)):
        if (i+1)*32 <= condition_length:
            if hash_int_arr[i] != 0:
                return False
        else:
            if (hash_int_arr[i] >> (32-(condition_length-(i*32)))) != 0:
                return False
    return True

if __name__ == "__main__":
    for condition in range(4,32,4):
        start_time = time.time()
        try_count = 0
        successed = False
        while successed == False:
            time_field = time.time()
            for nonce in range(MAX_INT):
                try_count += 1
                if checkMiningSuccess(MY_NAME, nonce, condition, time_field):
                    end_time = time.time()
                    elapsed_time = end_time - start_time
                    print('zero length: {}, try count: {}, elapsed time: {}'.format(condition, try_count, elapsed_time), flush=True)
                    successed = True
                    break
            