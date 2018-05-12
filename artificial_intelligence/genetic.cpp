#include<iostream>
#include<fstream>
#include<cstdlib>
#include<ctime>
#include<vector>
#include<bitset>

using namespace std;

typedef union Chromosome{
    float f;
    int i=0;
}Chromosome;

// global variables
vector<Chromosome> currentGeneration;
vector<Chromosome> nextGeneration;
vector<float> rulletWheel;
float bestFitnessValue;
float totalFitnessValue;
ofstream bestOutputFile("best.txt");
ofstream averageOutputFile("average.txt");

// constant variables
const int CROSSOVER_RATE = 0.7;
const int MUTATION_RATE = 0.1;
const int N = 1000;
const int E = 100;
const float LOWER_BOUND = -100.0;
const float UPPER_BOUND = -10.0;
const float MAX_FIT = 1092727.0f;
const float MIN_FIT = 2197.0f;


float randomNumberGenerate(float min, float max){
    float ret = (float)rand() / RAND_MAX;
    ret = ret * (max-min);
    ret = ret + min;
    return ret;
}

// scope is 0-31(left-right)
Chromosome extractBitsByScope(Chromosome target, int leftIdx, int rightIdx){
    Chromosome temp;
    temp.i = target.i << leftIdx;
    temp.i = temp.i >> leftIdx;
    temp.i = temp.i >> (31-rightIdx);
    temp.i = temp.i << (31-rightIdx);

    return temp;
}

void crossoverChromosome(Chromosome& ch1, Chromosome& ch2){
    Chromosome temp1, temp2;
    if(randomNumberGenerate(0.0,1.0) <= CROSSOVER_RATE){
        temp1.i |= extractBitsByScope(ch1, 0, 15).i;
        temp1.i |= extractBitsByScope(ch2, 16, 31).i;
        temp2.i |= extractBitsByScope(ch2, 0, 15).i;
        temp2.i |= extractBitsByScope(ch1, 16, 31).i;
        
        ch1 = temp1;
        ch2 = temp2;
    }
}

void mutateChromosome(Chromosome& ch){
    if(randomNumberGenerate(0.0,1.0) <= MUTATION_RATE){
        bitset<32> bits(ch.i);
        bits[rand()%32].flip();
        ch.i = bits.to_ulong();
    }
}

float fitnessFunction(Chromosome ch){
    float x = ch.f;
    x = -((x*x*x)-(9*x*x)+(27*x)-27);
    x = (x-MIN_FIT)/(MAX_FIT-MIN_FIT);
    return x;
}

void initializeGeneration(){
    for(int i=0; i<N; i++){
        Chromosome ch;
        ch.f = randomNumberGenerate(-100.0, -10.0);
        currentGeneration.push_back(ch);
    }
}

float getSumOfFitnessValues(){
    float sum = 0.0f;
    for(int i=0; i<currentGeneration.size(); i++){
        sum += fitnessFunction(currentGeneration[i]);
    }
    totalFitnessValue = sum;
    return sum;
}

float getAverageFitnessValue(){
    return totalFitnessValue / N;
}

float getBestFitnessValue(){
    return bestFitnessValue;
}

void evaluateCurrentGeneration(){
    float sumOfFit = getSumOfFitnessValues();
    float cursum = 0.0f;
    bestFitnessValue = -1.0f;
    rulletWheel.clear();
    rulletWheel.push_back(cursum);
    for(int i=0; i<currentGeneration.size(); i++){
        float fit = fitnessFunction(currentGeneration[i]);
        if(bestFitnessValue < fit)
            bestFitnessValue = fit;
        cursum += (fit / sumOfFit);
        rulletWheel.push_back(cursum);
    }
}

void populationUpdate(){
    currentGeneration = nextGeneration;
    nextGeneration.clear();
}

void printResult(){
    cout << "best : " << getBestFitnessValue() << endl;
    bestOutputFile << getBestFitnessValue() << endl;
    cout << "average : " << getAverageFitnessValue() << endl;
    averageOutputFile << getAverageFitnessValue() << endl;
    cout << "total fit : " << totalFitnessValue << endl;
}

int selectRandomChromosome(){
    float _rand = randomNumberGenerate(rulletWheel[0], rulletWheel[N]);
    int ret=-1;
    for(int i=1; i<=N; i++){
        if(_rand <= rulletWheel[i]){
            ret = i-1;
            break;
        }
    }
    return ret;
}

int main(int argc, char **argv){
    srand(time(NULL));

    cout << sizeof(long long) << endl;

    initializeGeneration();
    evaluateCurrentGeneration();
    printResult();
    for(int i=0; i<E; i++){
        while(nextGeneration.size() < N){
            int sel1 = selectRandomChromosome();
            int sel2 = selectRandomChromosome();
            while(sel1 == sel2){
                sel2 = selectRandomChromosome();
            }
            Chromosome ch1, ch2;
            ch1.f = currentGeneration[sel1].f;
            ch2.f = currentGeneration[sel2].f;
            crossoverChromosome(ch1,ch2);
            mutateChromosome(ch1);
            mutateChromosome(ch2);
            if(ch1.f <= UPPER_BOUND && ch1.f >= LOWER_BOUND && ch2.f <= UPPER_BOUND && ch2.f >= LOWER_BOUND){
                nextGeneration.push_back(ch1);
                nextGeneration.push_back(ch2);
            }
        }
        populationUpdate();
        evaluateCurrentGeneration();
        printResult();
    }
    return 0;
}