import random
import math
import time

INPUT_LAYER_SIZE = 784 #28*28
HIDDEN_LAYER_SIZE = 5
OUTPUT_LAYER_SIZE = 10
INPUT_TO_HIDDEN = 0
HIDDEN_TO_OUTPUT = 1
TOTAL_DATA_SIZE = 70000
LEARNING_SET_SIZE = 49000
TEST_SET_SIZE = 21000
THRESHOLD_HIDDEN = 0.2
THRESHOLD_OUTPUT = 0.3
LEARNING_RATE = 0.1



# weights[0] is weights between input and hidden, weights [1] is weights between hidden and output
weights = []   
hidden_y = []
output_y = []
input_data = []
input_target = []
error_gradient_k = []

def read_data_from_file(f):
    global input_data, input_target
    input_data = []
    line = f.readline()
    intput_target = int(line)
    for i in range(28):
        line = f.readline()
        line_arr = line.split(' ')
        for j in range(28):
            input_data.append(int(line_arr[j]))

def initialize_y():
    initialize_hidden_y()
    initialize_output_y()

def initialize_hidden_y():
    global hidden_y
    for i in range(HIDDEN_LAYER_SIZE):
        hidden_y.append(0)

def initialize_output_y():
    global output_y
    for i in range(OUTPUT_LAYER_SIZE):
        output_y.append(0)

def initialize_weights():
    initialize_input_hidden_weights()
    initialize_hidden_input_weights()

def initialize_input_hidden_weights():
    global weights
    weights_list = []
    for i in range(INPUT_LAYER_SIZE):
        w_ij_array = []
        for j in range(HIDDEN_LAYER_SIZE):
            rand_num = random.random()-0.5
            w_ij_array.append(rand_num)
        weights_list.append(w_ij_array)
    weights.append(weights_list)

def initialize_hidden_input_weights():
    global weights
    weights_list = []
    for i in range(HIDDEN_LAYER_SIZE):
        w_jk_array = []
        for j in range(OUTPUT_LAYER_SIZE):
            rand_num = random.random()-0.5
            w_jk_array.append(rand_num)
        weights_list.append(w_jk_array)
    weights.append(weights_list)
            
def calculate_hidden_neurons_output():
    for i in range(HIDDEN_LAYER_SIZE):
        X = calculate_hidden_neuron_output(i)
        hidden_y[i] = sigmoid_activation_function(X)

# calculate only one hidden layer neuron's output
# idx is hidden neuron's index
def calculate_hidden_neuron_output(idx):
    global THRESHOLD, weights, input_data
    X = 0
    for i in range(INPUT_LAYER_SIZE):
        X += (input_data[i]*weights[INPUT_TO_HIDDEN][i][idx])
    X -= THRESHOLD_HIDDEN
    return X

def calculate_output_neurons_output():
    for i in range(OUTPUT_LAYER_SIZE):
        X = calculate_output_neuron_output(i)
        output_y[i] = sigmoid_activation_function(X)

# calculate only one output layer neuron's output
# idx is output neuron's index
def calculate_output_neuron_output(idx):
    global THRESHOLD, weights, data
    X = 0
    for i in range(HIDDEN_LAYER_SIZE):
        X += (hidden_y[i]*weights[HIDDEN_TO_OUTPUT][i][idx])
    X -= THRESHOLD_OUTPUT
    return X

def make_target_list():
    global input_target
    target_list = []
    for i in range(OUTPUT_LAYER_SIZE):
        if i == input_target:
            target_list.append(1)
        else:
            target_list.append(0)
    return target_list

def learn_output_neurons():
    global error_gradient_k
    error_gradient_k = []
    target_list = make_target_list()
    for k in range(OUTPUT_LAYER_SIZE):
        error = target_list[k] - output_y[k]
        error_gradient = output_y[k] * (1-output_y[k]) * error
        error_gradient_k.append(error_gradient)
        for j in range(HIDDEN_LAYER_SIZE):
            delta = LEARNING_RATE * hidden_y[j] * error_gradient
            weights[HIDDEN_TO_OUTPUT][j][k] += delta
    
def learn_hidden_neurons():
    global error_gradient_k, input_data
    for j in range(HIDDEN_LAYER_SIZE):
        sum = 0
        for k in range(OUTPUT_LAYER_SIZE):
            sum += (error_gradient_k[k]+weights[HIDDEN_TO_OUTPUT][j][k])
        error_gradient = hidden_y[j] * (1-hidden_y[j]) * sum
        for i in range(INPUT_LAYER_SIZE):
            delta = LEARNING_RATE * input_data[i] * error_gradient
            weights[INPUT_TO_HIDDEN][i][j] += delta


def sigmoid_activation_function(X):
    print(X)
    return 1 / (1+math.exp(-X))
    
def learning_phase(f):
    for i in range(LEARNING_SET_SIZE):
        print('learning {}th data...\r'.format(i+1))
        read_data_from_file(f)
        calculate_hidden_neurons_output()
        calculate_output_neurons_output()
        learn_output_neurons()
        learn_hidden_neurons()
        print()

def testing_phase(f):
    for i in range(TEST_SET_SIZE):
        print('testing {}th data...\r')


start_time = time.time()
initialize_y()
initialize_weights()
f = open('MNIST.txt')
learning_phase(f)
end_time = time.time()
elapsed_time = end_time - start_time
print('elapsed time : {0}s'.format(elapsed_time))

    