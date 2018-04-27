#include<iostream>
#include<fstream>
#include<algorithm>
#include<vector>

using namespace std;

char* buf;
int* charCount;
const int BUF_SIZE = 1000;
const int CHAR_SCOPE = 128;
const int PRINTABLE_MIN = 32;

class CharFrequency{
    public:
        char symbol;
        int frequency;
        CharFrequency* left;
        CharFrequency* right;
        CharFrequency(char, int);
};

CharFrequency::CharFrequency(char symbol, int frequency){
    this->symbol = symbol;
    this->frequency = frequency;
    this->left = NULL;
    this->right = NULL;
}

bool compareCharFrequency(CharFrequency* left, CharFrequency* right){
    if(left->frequency >= right->frequency)
        return true;
    else
        return false;
}


void initializeCount(){
    for(int i=0; i<CHAR_SCOPE; i++){
        charCount[i] = 0;
    }
}

void print_huffman_code(CharFrequency* root, int depth){
    if(root->symbol != 0){
        if(root->symbol == '\r')
            cout << "\\r: ";
        else if(root->symbol == '\n')
            cout << "\\n: ";
        else
            cout << root->symbol << ": ";
        for(int i=0; i<depth; i++){
            cout << buf[i];
        }
        cout << endl;
    }
    if(root->left != NULL){
        buf[depth] = '0';
        print_huffman_code(root->left, depth+1);
    }
    if(root->left != NULL){
        buf[depth] = '1';
        print_huffman_code(root->right, depth+1);
    }
}

int main(int argc, char** argv){
    if(argc != 2){
        cout << "Usage: " << argv[0] << " file_name" << endl;
        return 1;
    }

    ifstream inputFile(argv[1]);
    buf = new char[BUF_SIZE];
    charCount = new int[CHAR_SCOPE];
    vector<CharFrequency*> v;
    CharFrequency* cf;
    CharFrequency *p, *q;

    initializeCount();

    while(!inputFile.read(buf, BUF_SIZE).eof()){
        for(int i =0; i<BUF_SIZE; i++){
            if(buf[i] == '\0')
                break;
            charCount[buf[i]]++;
        }
    }

    for(int i=0; i<CHAR_SCOPE; i++){
        if(charCount[i] == 0)
            continue;
        cf = new CharFrequency((char)i, charCount[i]);
        v.push_back(cf);
        if((char)i == '\r')
            cout << "character: " << "\\r" << "(" << i << "), count: " << charCount[i] << endl;
        else if((char)i == '\n')
            cout << "character: " << "\\n" << "(" << i << "), count: " << charCount[i] << endl;
        else
            cout << "character: " << (char)i << "(" << i << "), count: " << charCount[i] << endl;
    }

    make_heap(v.begin(), v.end(), compareCharFrequency);

    cout << endl;

    while(v.size() != 1){
        p = v.front();
        pop_heap(v.begin(), v.end(), compareCharFrequency);
        v.pop_back();

        q = v.front();
        pop_heap(v.begin(), v.end(), compareCharFrequency);
        v.pop_back();

        cf = new CharFrequency((char)0, p->frequency+q->frequency);
        cf->left = p;
        cf->right = q;

        v.push_back(cf);
        push_heap(v.begin(), v.end(), compareCharFrequency);
    }
    cf = v.back();
    print_huffman_code(cf, 0);
    
    return 0;
}
