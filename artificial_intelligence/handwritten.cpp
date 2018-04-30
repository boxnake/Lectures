#include<iostream>
#include<string>
#include<fstream>
#include<cstdlib>
#include<ctime>
#include<cmath>
#include<random>

using namespace std;

// constants
const int INPUT_LAYER_SIZE = 784;
const int OUTPUT_LAYER_SIZE = 10;
const int INPUT_TO_HIDDEN = 0;
const int HIDDEN_TO_OUTPUT = 1;
const int TOTAL_DATA_SIZE = 70000;
const int LEARNING_SET_SIZE = (TOTAL_DATA_SIZE / 100 * 70);
const int TEST_SET_SIZE = (TOTAL_DATA_SIZE / 100 * 30);
const double BOUND_SIZE = 0.5;

//variables
string input_str;
int hiddenLayerSize;
double learningRate;
double ***weights;
double *hiddenY, *outputY;
double *thresholdHidden, *thresholdOutput;
int *inputData = NULL;
int inputTarget;
int *totalCount=NULL, *successCount=NULL;
double errorGradient;
double *errorGradientK;
ifstream inputFile;
int epoch;

random_device rd;
mt19937 gen(rd());
uniform_real_distribution<> udist(-0.5,0.5);


void inputParameters(){
    cout << "hidden size? ";
    cin >> hiddenLayerSize;
    cout << "learning rate? ";
    cin >> learningRate;
}

void initializeInputData(){
    if(inputData == NULL)
        inputData = new int[INPUT_LAYER_SIZE];
}

void readDataFromFile(){
    initializeInputData();
    inputFile >> inputTarget;
    for(int i=0; i<INPUT_LAYER_SIZE; i++){
        inputFile >> inputData[i];
    }
}

void initializeCount(){
    if(totalCount == NULL)
        totalCount = new int[OUTPUT_LAYER_SIZE];
    if(successCount == NULL)
        successCount = new int[OUTPUT_LAYER_SIZE];
    for(int i=0; i<OUTPUT_LAYER_SIZE; i++){
        totalCount[i] = 0;
        successCount[i] = 0;
    }
}

void initializeHiddenThreshold(){
    thresholdHidden = new double[hiddenLayerSize];
    for(int i=0; i<hiddenLayerSize; i++){
        thresholdHidden[i] =  udist(gen);
    }
}

void initializeOutputThreshold(){
    thresholdOutput = new double[OUTPUT_LAYER_SIZE];
    for(int i=0; i<OUTPUT_LAYER_SIZE; i++){
        thresholdOutput[i] = udist(gen);
    }
}

void initializeThreshold(){
    initializeHiddenThreshold();
    initializeOutputThreshold();
}

void initializeHiddenY(){
    hiddenY = new double[hiddenLayerSize];
}

void initializeOutputY(){
    outputY = new double[OUTPUT_LAYER_SIZE];
}

void initializeY(){
    initializeHiddenY();
    initializeOutputY();
}

void initializeInputHiddenWeights(){
    weights[INPUT_TO_HIDDEN] = new double*[INPUT_LAYER_SIZE];
    for(int i=0; i<INPUT_LAYER_SIZE; i++){
        weights[INPUT_TO_HIDDEN][i] = new double[hiddenLayerSize];
        for(int j=0; j<hiddenLayerSize; j++){
            weights[INPUT_TO_HIDDEN][i][j] = udist(gen);
        }
    }
}

void initializeHiddenOutputWeights(){
    weights[HIDDEN_TO_OUTPUT] = new double*[hiddenLayerSize];
    for(int i=0; i<hiddenLayerSize; i++){
        weights[HIDDEN_TO_OUTPUT][i] = new double[OUTPUT_LAYER_SIZE];
        for(int j=0; j<OUTPUT_LAYER_SIZE; j++){
            weights[HIDDEN_TO_OUTPUT][i][j] = udist(gen);
        }
    }
}

void initializeWeights(){
    weights = new double**[2];
    initializeInputHiddenWeights();
    initializeHiddenOutputWeights();
}

double sigmoidActivationFunction(double X){
    double ret = (double)1 / (1+exp(-X));
    return ret;
}

double calculateHiddenNeuronOutput(int idx){
    double X = 0;
    double partialSum;
    for(int i=0; i<INPUT_LAYER_SIZE; i++){
        partialSum = inputData[i] * weights[INPUT_TO_HIDDEN][i][idx];
        X += partialSum;
    }
    X -= thresholdHidden[idx];
    return X;
}

void calculateHiddenNeuronsOutput(){
    for(int i=0; i<hiddenLayerSize; i++){
        double X = calculateHiddenNeuronOutput(i);
        hiddenY[i] = sigmoidActivationFunction(X);
    }
}

double calculateOutputNeuronOutput(int idx){
    double X = 0;
    for(int i=0; i<hiddenLayerSize; i++){
        X += (hiddenY[i]*weights[HIDDEN_TO_OUTPUT][i][idx]);
    }
    X -= thresholdOutput[idx];
    return X;
}

void checkCorrection(){
    int maxIdx = 0;
    for(int i=0; i<OUTPUT_LAYER_SIZE; i++)
        if(outputY[i] > outputY[maxIdx])
            maxIdx = i;
    
    if(maxIdx == inputTarget){
        totalCount[inputTarget]++;
        successCount[inputTarget]++;
    }
    else{
        totalCount[inputTarget]++;
    }
}

void calculateOutputNeuronsOutput(){
    for(int i=0; i<OUTPUT_LAYER_SIZE; i++){
        double X = calculateOutputNeuronOutput(i);
        outputY[i] = sigmoidActivationFunction(X);
    }
    checkCorrection();
}

void learnOutputNeurons(){
    double outputTarget, delta;
    for(int k=0; k<OUTPUT_LAYER_SIZE; k++){
        outputTarget = (k == inputTarget)?1.0:0.0;
        double error = outputTarget - outputY[k];
        errorGradient = outputY[k] * (1-outputY[k]) * error;
        errorGradientK[k] = errorGradient;
        for(int j=0; j<hiddenLayerSize; j++){
            delta = learningRate * hiddenY[j] * errorGradient;
            weights[HIDDEN_TO_OUTPUT][j][k] += delta;
        }
        delta = learningRate * -1 * errorGradient;
        thresholdOutput[k] += delta;
    }
}

void learnHiddenNeurons(){
    double gradientSum, delta;
    for(int j=0; j<hiddenLayerSize; j++){
        gradientSum = 0;
        for(int k=0; k<OUTPUT_LAYER_SIZE; k++)
            gradientSum += (errorGradientK[k]*weights[HIDDEN_TO_OUTPUT][j][k]);
        errorGradient = hiddenY[j] * (1-hiddenY[j]) * gradientSum;
        for(int i=0; i<INPUT_LAYER_SIZE; i++){
            delta = learningRate * inputData[i] * errorGradient;
            weights[INPUT_TO_HIDDEN][i][j] += delta;
        }
        delta = learningRate * -1 * errorGradient;
        thresholdHidden[j] += delta;
    }
}

int getCountSum(int *countList){
    int sum = 0;
    for(int i=0; i<OUTPUT_LAYER_SIZE; i++){
        sum += countList[i];
    }
    return sum;
}

double printResult(int epoch, string phase){
    double successRate;
    string banner = "============";
    cout << banner << " " << epoch << "  " << phase << " phase " << banner << endl;
    for(int i=0; i<OUTPUT_LAYER_SIZE; i++){
        successRate = (double)successCount[i] / totalCount[i] * 100;
        cout << "Category " << i << " : [" << successCount[i] 
            << "/" << totalCount[i] << "] (" << successRate << "%)" << endl;
    }
    successRate = (double)getCountSum(successCount) / getCountSum(totalCount) * 100;
    cout << "Total: " << "[" << getCountSum(successCount)
        << "/" << getCountSum(totalCount) << "] (" << successRate << "%)" << endl;
    return successRate;
}

void learningPhase(){
    initializeCount();
    for(int i=0; i<LEARNING_SET_SIZE; i++){
        cout << "learning " << (i+1) << "th data...\r";
        readDataFromFile();
        calculateHiddenNeuronsOutput();
        calculateOutputNeuronsOutput();
        learnOutputNeurons();
        learnHiddenNeurons();
    }
}

void testingPhase(){
    initializeCount();
    for(int t=0; t<TEST_SET_SIZE; t++){
        cout << "testing " << (t+1) << "th data...\r";
        readDataFromFile();
        calculateHiddenNeuronsOutput();
        calculateOutputNeuronsOutput();
    }
}

void initializeErrorGradientK(){
    errorGradientK = new double[OUTPUT_LAYER_SIZE];
}

int main(int argc, char** argv){
    srand(time(NULL));
    inputParameters();
    initializeThreshold();
    initializeY();
    initializeWeights();
    initializeErrorGradientK();

    epoch = 1;
    double testSuccessRate;

    while(true){
        inputFile.open("MNIST.txt");
        learningPhase();
        testingPhase();
        testSuccessRate = printResult(epoch, "testing");
        if(testSuccessRate > 99.8)
            break;
        inputFile.close();
        epoch++;
    }
    return 0;
}