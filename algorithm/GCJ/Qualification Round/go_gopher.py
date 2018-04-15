#Google CodeJam Qualification #3
import sys

orchard = []
delta_arr = [(1,1), (1,2), (3,1), (3,2)]

def initialize_orchard():
    global orchard
    for i in range(1000):
        for j in range(1000):
            orchard[i][j] = False

def check_adjacent_tiles(a,b):
    global orchard
    for i in range(-1,2):
        for j in range(-1,2):
            if not orchard[a+i][b+j]:
                return False
    return True

def readline_two_int():
    input_text = input()
    input_text = input_text.split(' ')
    return (int(input_text[0]), int(input_text[1]))

#======================================= main ===============================
for i in range(1000):
    temp = []
    for j in range(1000):
        temp.append(False)
    orchard.append(temp)

test_case_num = int(input())

for t in range(1,test_case_num+1):
    initialize_orchard()
    A = int(input())
    round = int(A/20)
    for i in range(round):
        base_point = (i*4, 0)
        for j in range(4):
            delta = delta_arr[j]
            center_point = (base_point[0]+delta[0], base_point[1]+delta[1])
            while not check_adjacent_tiles(center_point[0], center_point[1]):
                print('{0} {1}'.format(center_point[0]+1, center_point[1]+1))
                sys.stdout.flush()
                (a,b) = readline_two_int()
                if a==0 and b==0:
                    break
                orchard[a-1][b-1] = True


                

        
