#Google CodeJam 2018 Qualification #4
import math

QUANT_SIZE = 3600000
quantum = math.pi / QUANT_SIZE
base_point = [[[0.5, 0.0, 0.0]], [[0.0, 0.5, 0.0]], [[0.0, 0.0, 0.5]]]

def matrix_multi(a, b):
    result = []
    rows = len(a)
    cols = len(b[0])
    for i in range(rows):
        row = []
        for j in range(cols):
            entry = 0
            for k in range(len(b)):
                entry += (a[i][k] * b[k][j])
            row.append(entry)
        result.append(row)
    return result

def x_axis_rot(point, rad):
    cosine = math.cos(rad)
    sine = math.sin(rad)
    R = [[1, 0, 0], [0, cosine, -sine], [0, sine, cosine]]
    return matrix_multi(point, R)

def z_axis_rot(point, rad):
    cosine = math.cos(rad)
    sine = math.sin(rad)
    R = [[cosine, -sine, 0], [sine, cosine, 0], [0,0,1]]
    return matrix_multi(point, R)

def print_center_point(points):
    for point in points:
        print('{} {} {}'.format(point[0][0], point[0][1], point[0][2]))

def orthogonal_projection(seta):
    return 1*(1/math.cos(quantum*seta))

def try_rotation(A):
    start = 0
    end = int(QUANT_SIZE/2)+1
    for i in [start, end]:
        if abs(orthogonal_projection(i)-A) <= 0.000001:
            center_point = []
            for k in range(3):
                center_point.append(z_axis_rot(base_point[k], quantum*i))
            return center_point
    while end>=start:
        mid = int((start+end)/2)
        if abs(orthogonal_projection(mid)-A) <= 0.000001:
            center_point = []
            for k in range(3):
                center_point.append(z_axis_rot(base_point[k], quantum*mid))
            return center_point
        elif ((orthogonal_projection(start)-A)*(orthogonal_projection(mid)-A) < 0) and ((orthogonal_projection(mid)-A)*(orthogonal_projection(end)-A) > 0):
            # print('elif : {0} {1} {2}'.format(orthogonal_projection(start)-A, orthogonal_projection(mid)-A, orthogonal_projection(end)-A))
            end = mid-1
        elif ((orthogonal_projection(start)-A)*(orthogonal_projection(mid)-A) > 0) and ((orthogonal_projection(mid)-A)*(orthogonal_projection(end)-A) < 0):
            # print('else : {0} {1} {2}'.format(orthogonal_projection(start)-A, orthogonal_projection(mid)-A, orthogonal_projection(end)-A))
            start = mid+1
        else:
            if abs(orthogonal_projection(start)-A) < abs(orthogonal_projection(end)-A):
                end = mid-1
            else:
                start = mid+1



#=================== main ======================
test_case_num = int(input())

for t in range(1, test_case_num+1):
    A = float(input())
    print('Case #{}:'.format(t))
    if abs(1-A) <= 0.000001:
        print_center_point(base_point)
    else:
        print_center_point(try_rotation(A))
