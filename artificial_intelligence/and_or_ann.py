weights = []
learning_rate = 0.1
input_data = [(0,0), (0,1), (1,0), (1,1)]
and_answer = [0, 0, 0, 1]
or_answer = [0, 1, 1, 1]


def initialize_weights(*args):
    global weights
    weights = list(args)

def step_activation_function(threshold,x):
    sum = 0
    for i in range(2):
        sum += (weights[i]*x[i])
    sum -= threshold
    if sum >= 0:
        return 1
    else:
        return 0

def weight_learning(x,y,d,operate_type):
    print('{0} {1}'.format(x[0], x[1]), end=' ')
    if operate_type == 'AND':
        error = and_answer[d] - y
        print('{0}'.format(and_answer[d]), end=' ')
    else:
        error = or_answer[d] - y
        print('{0}'.format(or_answer[d]), end=' ')
    print('{0} {1} {2} {3}'.format(weights[0],weights[1], y, error), end=' ')
    for i in range(2):
        delta = learning_rate * x[i] * error
        weights[i] += delta
    print('{0} {1}'.format(weights[0], weights[1]))
    if error == 0:
        return True
    else:
        return False

def test_epoke(operate_type):
    success_count = 0
    for i in range(4):
        x = input_data[i]
        if weight_learning(x, step_activation_function(0.2,x), i, operate_type):
            success_count += 1
    success_rate = success_count / 4 * 100
    return success_rate
        
def print_epoke_result(p, success_rate):
    print('epoke {0}\'s success rate : {1}'.format(p, success_rate))
    if success_rate == 100.0:
        return True
    else:
        return False

def test_epokes(operate_type):
    for epoke in range(100):
        if print_epoke_result(epoke, test_epoke(operate_type)):
            break
        # print('w1 = {0}, w2 = {1}'.format(weights[0], weights[1]))
    print('w1 = {0}, w2 = {1}'.format(weights[0], weights[1]))


initialize_weights(0.2, -0.1)
test_epokes('AND')
print('='*40)
initialize_weights(0.1, -0.1)
test_epokes('OR')

            
    

    
