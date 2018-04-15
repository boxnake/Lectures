import random
import math
import time

NUM_OF_EPOCH = 100
INPUT_LAYER_SIZE = 784 #28*28
HIDDEN_LAYER_DEPTH = 3
HIDDEN_LAYER_SIZE = 10
OUTPUT_LAYER_SIZE = 10
INPUT_TO_HIDDEN = 0
HIDDEN_TO_OUTPUT = HIDDEN_LAYER_DEPTH
TOTAL_DATA_SIZE = 70000
LEARNING_SET_SIZE = 49000
TEST_SET_SIZE = 21000
LEARNING_RATE = 0.01



# weights[0] is weights between input and hidden, weights [1] is weights between hidden and output
weights = []   
hidden_y = []
output_y = []
input_data = []
input_target = 0
target_list = []
error_gradients = []
threshold_hidden = []
threshold_output = []
total_count = []
success_count = []

def read_data_from_file(f):
    global input_data, input_target, target_list
    input_data = []
    line = f.readline()
    input_target = int(line)
    target_list = make_target_list(input_target)
    for i in range(28):
        line = f.readline()
        line_arr = line.split(' ')
        for j in range(28):
            input_data.append(int(line_arr[j]))

def initialize_error_gradients():
    global error_gradients
    for h in range(HIDDEN_LAYER_DEPTH):
        temp_list = []
        if h < (HIDDEN_LAYER_DEPTH-1):
            for i in range(HIDDEN_LAYER_SIZE):
                temp_list.append(0)
        else:
            for i in range(OUTPUT_LAYER_SIZE):
                temp_list.append(0)
        error_gradients.append(temp_list)

def initialize_count():
    global total_count, success_count
    total_count = []
    success_count = []
    for i in range(OUTPUT_LAYER_SIZE):
        total_count.append(0)
        success_count.append(0)

def initialize_threshold():
    initialize_hidden_threshold()
    initialize_output_threshold()

def initialize_hidden_threshold():
    global threshold_hidden
    for h in range(HIDDEN_LAYER_DEPTH):
        temp_list = []
        for i in range(HIDDEN_LAYER_SIZE):
            temp_list.append(random.uniform(-0.5,0.5))
        threshold_hidden.append(temp_list)

def initialize_output_threshold():
    global threshold_output
    for i in range(OUTPUT_LAYER_SIZE):
        threshold_output.append(random.uniform(-0.5,0.5))

def initialize_y():
    initialize_hidden_y()
    initialize_output_y()

def initialize_hidden_y():
    global hidden_y
    for h in range(HIDDEN_LAYER_DEPTH):
        temp_list = []
        for i in range(HIDDEN_LAYER_SIZE):
            temp_list.append(0)
        hidden_y.append(temp_list)

def initialize_output_y():
    global output_y
    for i in range(OUTPUT_LAYER_SIZE):
        output_y.append(0)

def initialize_weights():
    initialize_input_hidden_weights()
    initialize_hidden_hidden_weights()
    initialize_hidden_output_weights()

def initialize_input_hidden_weights():
    global weights
    weights_list = []
    for i in range(INPUT_LAYER_SIZE):
        w_ij_array = []
        for j in range(HIDDEN_LAYER_SIZE):
            rand_num = random.uniform(-0.5,0.5)
            w_ij_array.append(rand_num)
        weights_list.append(w_ij_array)
    weights.append(weights_list)

def initialize_hidden_hidden_weights():
    global weights
    for h in range(HIDDEN_LAYER_DEPTH-1):
        weights_list = []
        for i in range(HIDDEN_LAYER_SIZE):
            w_jj_array = []
            for j in range(HIDDEN_LAYER_SIZE):
                rand_num = random.uniform(-0.5,0.5)
                w_jj_array.append(rand_num)
            weights_list.append(w_jj_array)
        weights.append(weights_list)

def initialize_hidden_output_weights():
    global weights
    weights_list = []
    for i in range(HIDDEN_LAYER_SIZE):
        w_jk_array = []
        for j in range(OUTPUT_LAYER_SIZE):
            rand_num = random.uniform(-0.5,0.5)
            w_jk_array.append(rand_num)
        weights_list.append(w_jk_array)
    weights.append(weights_list)
            
def calculate_hidden_neurons_output():
    global hidden_y
    for depth in range(0,HIDDEN_LAYER_DEPTH):
        for i in range(HIDDEN_LAYER_SIZE):
            X = calculate_hidden_neuron_output(depth, i)
            hidden_y[depth][i] = sigmoid_activation_function(X)

# calculate only one hidden layer neuron's output
# idx is hidden neuron's index
def calculate_hidden_neuron_output(depth, idx):
    global threshold_hidden, weights, input_data
    X = 0
    if depth == INPUT_TO_HIDDEN:
        for i in range(INPUT_LAYER_SIZE):
            X += (input_data[i]*weights[INPUT_TO_HIDDEN][i][idx])
        X -= threshold_hidden[depth][idx]
    else:
        for j in range(HIDDEN_LAYER_SIZE):
            X += (hidden_y[depth-1][j]*weights[depth][j][idx])
        X -= threshold_hidden[depth][idx]
    return X

def calculate_output_neurons_output():
    global output_y
    for i in range(OUTPUT_LAYER_SIZE):
        X = calculate_output_neuron_output(i)
        output_y[i] = sigmoid_activation_function(X)
    check_correction()

def check_correction():
    global output_y, input_target, total_count, success_count
    max_idx = 0
    for i in range(OUTPUT_LAYER_SIZE):
        if output_y[i] > output_y[max_idx]:
            max_idx = i
    if max_idx == input_target:
        total_count[input_target] += 1
        success_count[input_target] += 1
    else:
        total_count[input_target] += 1

# calculate only one output layer neuron's output
# idx is output neuron's index
def calculate_output_neuron_output(idx):
    global threshold_output, weights, data
    X = 0
    for i in range(HIDDEN_LAYER_SIZE):
        X += (hidden_y[-1][i]*weights[HIDDEN_TO_OUTPUT][i][idx])
    X -= threshold_output[idx]
    return X

def make_target_list(input_number):
    target_list = []
    for i in range(OUTPUT_LAYER_SIZE):
        if i == input_number:
            target_list.append(1)
        else:
            target_list.append(0)
    return target_list

def learn_output_neurons():
    global error_gradients, target_list, threshold_output
    for k in range(OUTPUT_LAYER_SIZE):
        error = target_list[k] - output_y[k]
        error_gradient = output_y[k] * (1-output_y[k]) * error
        error_gradients[HIDDEN_TO_OUTPUT-1][k] = error_gradient
        for j in range(HIDDEN_LAYER_SIZE):
            delta = LEARNING_RATE * hidden_y[HIDDEN_TO_OUTPUT-1][j] * error_gradient
            weights[HIDDEN_TO_OUTPUT][j][k] += delta
        delta = LEARNING_RATE * -1 * error_gradient
        threshold_output[k] += delta


    
def learn_hidden_neurons():
    global error_gradients, input_data, threshold_hidden
    for depth in range(HIDDEN_LAYER_DEPTH-1, -1, -1):
        for j in range(HIDDEN_LAYER_SIZE):
            gradient_sum = 0
            if depth == HIDDEN_LAYER_DEPTH-1:
                for k in range(OUTPUT_LAYER_SIZE):
                    gradient_sum += (error_gradients[depth][k]*weights[HIDDEN_TO_OUTPUT][j][k])
            else:
                for k in range(HIDDEN_LAYER_SIZE):
                    gradient_sum += (error_gradients[depth][k]*weights[depth+1][j][k])
            error_gradient = hidden_y[depth][j] * (1-hidden_y[depth][j]) * gradient_sum
            if depth > 0:
                error_gradients[depth-1][j] = error_gradient
            if depth == 0:
                for i in range(INPUT_LAYER_SIZE):
                    delta = LEARNING_RATE * input_data[i] * error_gradient
                    weights[INPUT_TO_HIDDEN][i][j] += delta
            else:
                for i in range(HIDDEN_LAYER_SIZE):
                    delta = LEARNING_RATE * hidden_y[depth-1][i] * error_gradient
                    weights[depth][i][j] += delta
            delta = LEARNING_RATE * -1 * error_gradient
            threshold_hidden[depth][j] += delta


def sigmoid_activation_function(X):
    try:
        return 1 / (1+math.exp(-X))
    except OverflowError:
        if X > 0:
            return 1
        elif X < 0:
            return 0
        else:
            return 0.5

def print_result(epoch, phase):
    global total_count, success_count
    banner_string = ('='*15) + ' {} epoch  {} phase ' + ('='*15)
    print(banner_string.format(epoch, phase))
    for i in range(OUTPUT_LAYER_SIZE):
        success_rate = success_count[i] / total_count[i] * 100
        print('Category {0} : [{1}/{2}] ({3:.2f}%)'.format(i, success_count[i], total_count[i], success_rate))
    success_rate = sum(success_count) / sum(total_count) * 100
    print('total: [{0}/{1}] ({2:.2f}%)'.format(sum(success_count), sum(total_count), success_rate))
    
def learning_phase(f):
    initialize_count()
    for i in range(LEARNING_SET_SIZE):
        print('learning {}th data...'.format(i+1), end='\r')
        read_data_from_file(f)
        calculate_hidden_neurons_output()
        calculate_output_neurons_output()
        learn_output_neurons()
        learn_hidden_neurons()

def testing_phase(f):
    initialize_count()
    for t in range(TEST_SET_SIZE):
        print('testing {}th data...'.format(t+1), end='\r')
        read_data_from_file(f)
        calculate_hidden_neurons_output()
        calculate_output_neurons_output()



start_time = time.time()
print('epoch: {}'.format(NUM_OF_EPOCH))
print('hidden size: {}'.format(HIDDEN_LAYER_SIZE))
print('hidden depth: {}'.format(HIDDEN_LAYER_DEPTH))
print('learning rate: {}'.format(LEARNING_RATE))
initialize_threshold()
initialize_y()
initialize_weights()
initialize_error_gradients()
for epoch in range(1,NUM_OF_EPOCH+1):
    f = open('MNIST.txt')
    learning_phase(f)
    print_result(epoch, 'learning')
    if epoch == NUM_OF_EPOCH:
        testing_phase(f)
        print_result(epoch, 'testing')
    end_time = time.time()
    elapsed_time = end_time - start_time
print('elapsed time : {0}s'.format(elapsed_time))

    