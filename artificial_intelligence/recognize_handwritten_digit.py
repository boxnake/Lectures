import random
import math
import time

NUM_OF_LEARNING_EPOCH = 10
INPUT_LAYER_SIZE = 784 #28*28
HIDDEN_LAYER_SIZE = 30
OUTPUT_LAYER_SIZE = 10
INPUT_TO_HIDDEN = 0
HIDDEN_TO_OUTPUT = 1
TOTAL_DATA_SIZE = 70000
LEARNING_SET_SIZE = int(TOTAL_DATA_SIZE / 100 * 70)
TEST_SET_SIZE = int(TOTAL_DATA_SIZE / 100 * 30)
LEARNING_RATE = 0.1
UPPER_BOUND = 0.5
LOWER_BOUND = -0.5



# weights[0] is weights between input and hidden, weights [1] is weights between hidden and output
weights = []
hidden_y = []
output_y = []
input_data = []
input_target = 0
target_list = []
error_gradient_k = []
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

def initialize_count():
    global total_count, success_count
    total_count = [0] * OUTPUT_LAYER_SIZE
    success_count = [0] * OUTPUT_LAYER_SIZE

def initialize_threshold():
    initialize_hidden_threshold()
    initialize_output_threshold()

def initialize_hidden_threshold():
    global threshold_hidden
    threshold_hidden = [0] * HIDDEN_LAYER_SIZE
    for i in range(HIDDEN_LAYER_SIZE):
        threshold_hidden[i] = random.uniform(LOWER_BOUND,UPPER_BOUND)

def initialize_output_threshold():
    global threshold_output
    threshold_output = [0] * OUTPUT_LAYER_SIZE
    for i in range(OUTPUT_LAYER_SIZE):
        threshold_output[i] = random.uniform(LOWER_BOUND,UPPER_BOUND)

def initialize_y():
    initialize_hidden_y()
    initialize_output_y()

def initialize_hidden_y():
    global hidden_y
    hidden_y = [0] * HIDDEN_LAYER_SIZE

def initialize_output_y():
    global output_y
    output_y = [0] * OUTPUT_LAYER_SIZE

def initialize_weights():
    global weights
    weights = []
    initialize_input_hidden_weights()
    initialize_hidden_output_weights()

def initialize_input_hidden_weights():
    global weights
    weights_list = []
    for i in range(INPUT_LAYER_SIZE):
        temp_list = []
        for j in range(HIDDEN_LAYER_SIZE):
            rand_num = random.uniform(LOWER_BOUND,UPPER_BOUND)
            temp_list.append(rand_num)
        weights_list.append(temp_list)
    weights.append(weights_list)

def initialize_hidden_output_weights():
    global weights
    weights_list = []
    for i in range(HIDDEN_LAYER_SIZE):
        temp_list = []
        for j in range(OUTPUT_LAYER_SIZE):
            rand_num = random.uniform(LOWER_BOUND,UPPER_BOUND)
            temp_list.append(rand_num)
        weights_list.append(temp_list)
    weights.append(weights_list)
            
def calculate_hidden_neurons_output():
    global hidden_y
    for i in range(HIDDEN_LAYER_SIZE):
        X = calculate_hidden_neuron_output(i)
        hidden_y[i] = sigmoid_activation_function(X)

# calculate only one hidden layer neuron's output
# idx is hidden neuron's index
def calculate_hidden_neuron_output(idx):
    global threshold_hidden, weights, input_data
    X = 0
    for i in range(INPUT_LAYER_SIZE):
        X += (input_data[i]*weights[INPUT_TO_HIDDEN][i][idx])
    X -= threshold_hidden[idx]
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
    print("maxidx = {} inputtarget = {}".format(max_idx, input_target))
    print(output_y)
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
        X += (hidden_y[i]*weights[HIDDEN_TO_OUTPUT][i][idx])
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
    global error_gradient_k, target_list, threshold_output
    error_gradient_k = []
    for k in range(OUTPUT_LAYER_SIZE):
        error = target_list[k] - output_y[k]
        error_gradient = output_y[k] * (1-output_y[k]) * error
        error_gradient_k.append(error_gradient)
        for j in range(HIDDEN_LAYER_SIZE):
            delta = LEARNING_RATE * hidden_y[j] * error_gradient
            weights[HIDDEN_TO_OUTPUT][j][k] += delta
        delta = LEARNING_RATE * -1 * error_gradient
        threshold_output[k] += delta


    
def learn_hidden_neurons():
    global error_gradient_k, input_data, threshold_hidden
    for j in range(HIDDEN_LAYER_SIZE):
        gradient_sum = 0
        for k in range(OUTPUT_LAYER_SIZE):
            gradient_sum += (error_gradient_k[k]*weights[HIDDEN_TO_OUTPUT][j][k])
        error_gradient = hidden_y[j] * (1-hidden_y[j]) * gradient_sum
        for i in range(INPUT_LAYER_SIZE):
            delta = LEARNING_RATE * input_data[i] * error_gradient
            weights[INPUT_TO_HIDDEN][i][j] += delta
        delta = LEARNING_RATE * -1 * error_gradient
        threshold_hidden[j] += delta


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
    return success_rate
    
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


HIDDEN_LAYER_SIZE = int(input('hidden size? '))
LEARNING_RATE = float(input('learning rate? '))
print('learning_rate: {}'.format(LEARNING_RATE))
print('hidden_layer_size: {}'.format(HIDDEN_LAYER_SIZE))
print('(lower,upper): ({},{})'.format(LOWER_BOUND,UPPER_BOUND))
start_time = time.time()
initialize_threshold()
initialize_y()
initialize_weights()
epoch = 1
while True:
    f = open('MNIST.txt')
    learning_phase(f)
    testing_phase(f)
    test_success_rate = print_result(epoch, 'testing')
    if test_success_rate > 99.0:
        break
    f.close()
    epoch += 1
end_time = time.time()
elapsed_time = end_time - start_time
print('elapsed time : {0}s'.format(elapsed_time))
    
