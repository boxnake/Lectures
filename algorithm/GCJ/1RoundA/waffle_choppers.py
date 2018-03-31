test_case_num = 0
R = 0
C = 0
H = 0
V = 0
one_piece = 0
waffle = []
chips_r = []
chips_c = []
chips = []

def sum_arr(arr):
    ret = 0
    for i in arr:
        ret += i
    return ret

def initialize_chips(R,C):
    global chips_r, chips_c
    chips_r = []
    for i in range(R):
        chips_r.append(0)
    chips_c = []
    for i in range(C):
        chips_c.append(0)

def input_waffle(R,C):
    global waffle, chips_r, chips_c
    waffle = []
    initialize_chips(R,C)
    for i in range(R):
        line = input()
        for j in range(C):
            if line[j] == '@':
                chips_r[i] += 1
                chips_c[j] += 1
        waffle.append(line)
            
def chip_count(r_min, r_max, c_min, c_max):
    global waffle, R, C
    count = 0
    for i in range(R):
        if i >= r_min and i <= r_max:
            for j in range(C):
                if j >= c_min and j <= c_max:
                    if waffle[i][j] == '@':
                        count += 1
    return count
            

    
    
def is_cuttable():
    global R,C,H,V
    length = len(chips)
    total_sum = chip_count(0, R-1, 0, C-1)
    if total_sum%((H+1)*(V+1)) != 0:
        return False
    row_size = int(total_sum / (H+1))
    piece_size = int(row_size / (V+1))






test_case_num = int(input())
for t in range(1,test_case_num+1):
    line = input()
    line = line.split(' ')
    R = int(line[0])
    C = int(line[1])
    H = int(line[2])
    V = int(line[3])
    input_waffle(R,C)
    row_piece = sum_arr()
    if is_cuttable(chips_r, H) and is_cuttable(chips_c, V):
        result = 'POSSIBLE'
    else:
        result = 'IMPOSSIBLE'
    print('Case #{}: {}'.format(t, result))
