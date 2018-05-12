#include<iostream>
#include<fstream>
#include<cstdlib>
#include<ctime>
#include<vector>
#include<cmath>
#include<limits>

using namespace std;

class TreeNode{
public:
    bool isTerminal = false;
    TreeNode *left = NULL;
    TreeNode *right = NULL;
    char op = 0;
    double value;
    int numOfTerm = 1;
    TreeNode();
    TreeNode(char ch);
};

vector<TreeNode*> currentGeneration;
vector<TreeNode*> nextGeneration;
vector<double> dataSet;
vector<double> rulletWheel;
double bestFitness;
double testFitness;
double totalFitness;
double totalTreeSize;
TreeNode* bestFitTree;

const int MAX_NUM_OF_TERMINAL_NODE = 150;
const double X_CONSTANT_RATIO = 0.6;
const int N = 2000;
const int E = 2000;
const int TOTAL_DATA_LENGTH = 10000;
const int LEARNING_DATA_LENGTH = 9000;
const int TESTING_DATA_LENGTH = 1000;
const double COPY_RATE = 0.5;
const double CROSSOVER_RATE = 0.4;
const double MUTATION_RATE = 0.1;
const char OP_CODE_ADD = 0;
const char OP_CODE_SUB = 1;
const char OP_CODE_MUL = 2;
const char OP_CODE_DIV = 3;
const double DATA_LOWER_BOUND = -500.0;
const double DATA_UPPER_BOUND = 500.0;
const double TERMINAL_NODE_LOWER_BOUND = -5.0;
const double TERMINAL_NODE_UPPER_BOUND = 5.0;

ofstream bestOutput("best.txt");
ofstream averageOutput("average.txt");
ofstream testOutput("test.txt");


TreeNode::TreeNode(){
}

TreeNode::TreeNode(char ch){
    if(ch == 'T'){
        isTerminal = true;
    }
    else{
        isTerminal = false;
    }
}

double getResultValueFromTree(TreeNode *root, double x){
    if(root->isTerminal){
        if(root->op == 'x'){
            return x;
        }
        else{
            return root->value;
        }
    }
    else{
        if(root->op == OP_CODE_ADD){
            return getResultValueFromTree(root->left, x) + getResultValueFromTree(root->right, x);
        }
        else if(root->op == OP_CODE_SUB){
            return getResultValueFromTree(root->left, x) - getResultValueFromTree(root->right, x);
        }
        else if(root->op == OP_CODE_MUL){
            return getResultValueFromTree(root->left, x) * getResultValueFromTree(root->right, x);
        }
        else if(root->op == OP_CODE_DIV){
            return getResultValueFromTree(root->left, x) / getResultValueFromTree(root->right, x);
        }
    }
}

double getResultValueFromFunction(double x){
    return (x*x*x)-(9*x*x)+(27*x)-27;
}

double getFitnessValueFromTree(TreeNode *root, double x){
    double ret = getResultValueFromTree(root, x) - getResultValueFromFunction(x);

    if(isnan(ret))
        return 0.0;
    ret = 1 / (1+abs(ret));
    return ret;
}

double getAverageFitnessFromTree(TreeNode *root, bool isTest){
    double fit = 0.0;
    if(isTest){
        for(int i=LEARNING_DATA_LENGTH; i<TOTAL_DATA_LENGTH; i++){
            fit += getFitnessValueFromTree(root, dataSet[i]);
        }
        return fit / TESTING_DATA_LENGTH * 100;
    }
    else{
        for(int i=0; i<LEARNING_DATA_LENGTH; i++){
            fit += getFitnessValueFromTree(root, dataSet[i]);
        }
        return fit / LEARNING_DATA_LENGTH * 100;
    }
}

void clearTreeNode(TreeNode *root){
    if(root->isTerminal){
        delete root;
    }
    else{
        clearTreeNode(root->left);
        clearTreeNode(root->right);
        delete root;
    }
}

TreeNode* deepCopyTreeNode(TreeNode *root){
    if(root->isTerminal){
        TreeNode *ret = new TreeNode('T');
        ret->numOfTerm = root->numOfTerm;
        ret->op = root->op;
        ret->value = root->value;
        return ret;
    }
    else{
        TreeNode *ret = new TreeNode('N');
        ret->numOfTerm = root->numOfTerm;
        ret->op = root->op;
        ret->left = deepCopyTreeNode(root->left);
        ret->right = deepCopyTreeNode(root->right);
        return ret;
    }
}

int randomIntegerGenerate(int min, int max){
    int ret = rand() % (max-min+1);
    ret = ret + min;
    return ret;
}

double randomNumberGenerate(float min, float max){
    double ret = (double)rand() / RAND_MAX;
    ret = ret * (max-min);
    ret = ret + min;
    return ret;
}

int recalculateNumOfTerm(TreeNode* root){
    if(root->isTerminal){
        return 1;
    }
    else{
        root->numOfTerm = recalculateNumOfTerm(root->left) + recalculateNumOfTerm(root->right);
        return root->numOfTerm;
    }
}

TreeNode* createExpressionTree(int min, int max){
    vector<TreeNode*> v;
    vector<TreeNode*>::iterator iter;
    int numOfTerm = randomIntegerGenerate(min, max);
    for(int i=0; i<numOfTerm; i++){
        TreeNode* temp = new TreeNode('T');
        if(randomNumberGenerate(0.0,1.0) <= X_CONSTANT_RATIO){
            temp->op = 'x';
        }
        else{
            temp->op = 0;
            temp->value = randomNumberGenerate(TERMINAL_NODE_LOWER_BOUND, TERMINAL_NODE_UPPER_BOUND);
        }
        v.push_back(temp);
    }

    while(v.size() > 1){
        int offset = randomIntegerGenerate(0, v.size()-1);
        iter = v.begin() + offset;
        TreeNode *t1 = *iter;
        v.erase(iter);

        offset = randomIntegerGenerate(0, v.size()-1);
        iter = v.begin() + offset;
        TreeNode *t2 = *iter;
        v.erase(iter);

        TreeNode *newRoot = new TreeNode('N');
        newRoot->left = t1;
        newRoot->right = t2;
        newRoot->numOfTerm = t1->numOfTerm + t2->numOfTerm;
        newRoot->op = randomIntegerGenerate(OP_CODE_ADD, OP_CODE_DIV);
        v.push_back(newRoot);
    }

    return v[0];
}

void initializeGeneration(){
    for(int i=0; i<N; i++){
        currentGeneration.push_back(createExpressionTree(2,MAX_NUM_OF_TERMINAL_NODE));
    }
}

void initializeDataSet(){
    for(int i=0; i<TOTAL_DATA_LENGTH; i++){
        dataSet.push_back(randomNumberGenerate(DATA_LOWER_BOUND, DATA_UPPER_BOUND));
    }
}

void evaluateCurrentGeneration(){
    vector<TreeNode*>::iterator iter;
    double cursum = 0.0;
    bestFitness = -1.0;
    totalTreeSize = 0;
    rulletWheel.clear();
    rulletWheel.push_back(cursum);

    for(iter = currentGeneration.begin(); iter != currentGeneration.end(); iter++){
        double fit = getAverageFitnessFromTree(*iter, false);
        if(bestFitness < fit){
            bestFitness = fit;
            bestFitTree = *iter;
        }
        totalTreeSize += (*iter)->numOfTerm;
        cursum += fit;
        rulletWheel.push_back(cursum);
    }
    totalFitness = cursum;
    testFitness = getAverageFitnessFromTree(bestFitTree, true);
}

int selectRandomChromosome(){
    float _rand = randomNumberGenerate(rulletWheel[0], rulletWheel[N]);
    for(int i=1; i<=N; i++){
        if(_rand <= rulletWheel[i]){
            return i-1;
        }
    }
    return N-1;
}

TreeNode** selectBranch(TreeNode* root){
    vector<TreeNode*> _queue;
    vector<TreeNode**> _rullet;
    _queue.push_back(root);
    
    while(_queue.size() != 0){
        TreeNode* cur = _queue.front();
        _queue.erase(_queue.begin());

        if(!cur->isTerminal){
            _queue.push_back(cur->left);
            _queue.push_back(cur->right);
            _rullet.push_back(&(cur->left));
            _rullet.push_back(&(cur->right));
        }
    }

    vector<TreeNode**>::iterator iter = _rullet.begin() + randomIntegerGenerate(0, _rullet.size()-1);
    TreeNode** ret = *iter;
    return ret;
}

void swapBranch(TreeNode **branch1, TreeNode **branch2){
    TreeNode *temp;
    temp = *branch1;
    *branch1 = *branch2;
    *branch2 = temp;
}

void crossoverTree(TreeNode* tree1, TreeNode* tree2){
    swapBranch(selectBranch(tree1), selectBranch(tree2));
}

void mutateTree(TreeNode* tree){
    TreeNode **selected = selectBranch(tree);
    double subTreeSize = (*selected)->numOfTerm;

    clearTreeNode(*selected);
    *selected = createExpressionTree(subTreeSize, subTreeSize);
}

void populationUpdate(){
    vector<TreeNode*>::iterator iter;
    for(iter = currentGeneration.begin(); iter != currentGeneration.end(); iter++){
        clearTreeNode(*iter);
    }
    currentGeneration = nextGeneration;
    nextGeneration.clear();
}

void printTreeNodePrefix(TreeNode *root){
    if(root->isTerminal){
        if(root->op == 'x')
            cout << "x ";
        else
            cout << root->value << " ";
    }
    else{
        cout << "( ";
        if(root->op == OP_CODE_ADD)
            cout << "+ ";
        else if(root->op == OP_CODE_SUB)
            cout << "- ";
        else if(root->op == OP_CODE_MUL)
            cout << "* ";
        else if(root->op == OP_CODE_DIV)
            cout << "/ ";
        printTreeNodePrefix(root->left);
        printTreeNodePrefix(root->right);
        cout << ") ";
    }
}

void printResult(){
    static int epoch=0;
    cout << "=================== " << ++epoch << "epoch =======================" << endl;
    cout << "best: " << bestFitness << endl;
    testOutput << testFitness << endl;
    cout << "best with test: " << testFitness << endl;
    bestOutput << bestFitness << endl;
    cout << "average: " << (totalFitness / N) << endl;
    averageOutput << (totalFitness / N) << endl;
    cout << "averageTreeSize: " << (totalTreeSize / N) << endl;
    cout << "best->numofterm: " << bestFitTree->numOfTerm << endl;
    printTreeNodePrefix(bestFitTree);
    cout << endl;
}

int main(int argc, char **argv){
    srand(time(NULL));
    initializeDataSet();
    initializeGeneration();
    evaluateCurrentGeneration();
    printResult();

    for(int i=0; i<E; i++){
        while(nextGeneration.size() < N){
            int select1, select2;
            double averageTreeSize, fit1, fit2;
            TreeNode *newTree1, *newTree2;

            if(nextGeneration.size() == 0){
                newTree1 = deepCopyTreeNode(bestFitTree);
                newTree2 = deepCopyTreeNode(bestFitTree);
                nextGeneration.push_back(newTree1);
                mutateTree(newTree2);
                nextGeneration.push_back(newTree2);
                continue;
            }
            select1 = selectRandomChromosome();
            select2 = selectRandomChromosome();

            newTree1 = deepCopyTreeNode(currentGeneration[select1]);
            newTree2 = deepCopyTreeNode(currentGeneration[select2]);

            double _rand = randomNumberGenerate(0.0, 1.0);
            if(_rand <= MUTATION_RATE){
                mutateTree(newTree1);
                mutateTree(newTree2);
            }
            else if(_rand <= (MUTATION_RATE+CROSSOVER_RATE)){
                crossoverTree(newTree1, newTree2);
            }

            recalculateNumOfTerm(newTree1);
            recalculateNumOfTerm(newTree2);

            averageTreeSize = (newTree1->numOfTerm + newTree2->numOfTerm) / 2;
            fit1 = getAverageFitnessFromTree(newTree1, false);
            fit2 = getAverageFitnessFromTree(newTree2, false);
            double sizeThreshold = (averageTreeSize <= 50)? 0 : (averageTreeSize-50)/(MAX_NUM_OF_TERMINAL_NODE-50);

            if(randomNumberGenerate(0.0,1.0) >= sizeThreshold){
                nextGeneration.push_back(newTree1);
                nextGeneration.push_back(newTree2);
            }
            else if(fit1 > bestFitness || fit2 > bestFitness){
                if(newTree1->numOfTerm <= MAX_NUM_OF_TERMINAL_NODE && newTree2->numOfTerm <= MAX_NUM_OF_TERMINAL_NODE){
                    nextGeneration.push_back(newTree1);
                    nextGeneration.push_back(newTree2);
                }
            }
            else{
                clearTreeNode(newTree1);
                clearTreeNode(newTree2);
            }
        }
        populationUpdate();
        evaluateCurrentGeneration();
        printResult();
        cout.flush();
    }
    cout << "best tree's test result : " << getAverageFitnessFromTree(bestFitTree, true) << endl;
    printTreeNodePrefix(bestFitTree);
    return 0;
}