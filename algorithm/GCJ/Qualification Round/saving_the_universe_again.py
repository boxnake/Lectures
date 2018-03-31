## Google CodeJam Qualification #1
import copy

def minimum(*args):
    min = -1
    for arg in args[0]:
        if min == -1 or min > arg:
            min = arg
    return min

def damage_calculate(P):
    dam = 0
    atk = 1
    for ch in P:
        if ch == 'C':
            atk *= 2
        elif ch == 'S':
            dam += atk
    return dam


#maybe back tracking?
def get_minimum_move(D, P):
    length = len(P)
    round = 0
    if P.count('S') > D:
        return -1
    while True:
        if damage_calculate(P) <= D:
            return round
        for i in range(length-2,-1,-1):
            if P[i+1] == 'S' and P[i] == 'C':
                P = P[:i] + P[i+1] + P[i] + P[i+2:]
                round += 1
                break
    


## =========================== main ===========================
test_case_num = int(input())

for t in range(1,test_case_num+1):
    input_text = input()
    D = int(input_text.split(' ')[0])
    P = input_text.split(' ')[1]
    minimum_move = get_minimum_move(D, P)
    if minimum_move == -1:
        print('Case #{0}: IMPOSSIBLE'.format(t))
    else:
        print('Case #{0}: {1}'.format(t, minimum_move))

