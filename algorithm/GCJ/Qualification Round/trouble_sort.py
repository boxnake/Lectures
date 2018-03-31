## Google CodeJam Qualification #2
from sys import stdin

def check_sorted(input_list):
    length = len(input_list)
    for i in range(length-1):
        if input_list[i] > input_list[i+1]:
            if i!=0 and input_list[i] != input_list[i-1]:
                return i
            else:
                for j in range(i,0):
                    print('j : {}, j-1: {}'.format(input_list[j], input_list[j-1]))
                    if input_list[j] != input_list[j-1]:
                        return j
                return 0
    return -1

def trouble_sort(input_list):
    length = len(input_list)
    done = False
    while not done:
        done = True
        for i in range(length-2):
            if input_list[i] > input_list[i+2]:
                done = False
                temp = input_list[i]
                input_list[i] = input_list[i+2]
                input_list[i+2] = temp
    return check_sorted(input_list)

    

# =========================== main =============================
test_case_num = int(input())

for t in range(1,test_case_num+1):
    length = int(input())
    input_text = stdin.readline()
    input_text = input_text.split(' ')
    input_list = []
    for i in range(length):
        input_list.append(int(input_text[i]))
    # print('input_list:{}'.format(input_list))
    unsorted_index = trouble_sort(input_list)
    if unsorted_index < 0 :
        print('Case #{0}: OK'.format(t))
    else:
        print('Case #{0}: {1}'.format(t, unsorted_index))
    
    