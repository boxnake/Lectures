#include<iostream>
#include<fstream>
#include<algorithm>
#include<vector>

using namespace std;

char* buf;
int* charCount;
const int BUF_SIZE = 1;
const int CHAR_SCOPE = 128;
const int PRINTABLE_MIN = 32;
int bits = 0;
int binBuffer = 0;
int occupiedBinBufferSize = 0;

const int HEADER_SIZE = 644;

class CharFrequency{
    public:
        char symbol;
        int frequency;
        CharFrequency* left;
        CharFrequency* right;
        CharFrequency(char, int);
};

class HuffmanCode{
    public:
        char symbol = 0;
        char bitLength = 0;
        int bitStream = 0;
};
HuffmanCode *codeTable = new HuffmanCode[128];

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

bool compareHuffmanCode(HuffmanCode left, HuffmanCode right){
    if(left.bitLength < right.bitLength)
        return true;
    else
        return false;
}


void initializeCount(){
    for(int i=0; i<CHAR_SCOPE; i++){
        charCount[i] = 0;
    }
}

void makeHuffmanCode(CharFrequency *root, int depth){
    if(root->symbol != 0){
        codeTable[root->symbol].symbol = root->symbol;
        codeTable[root->symbol].bitLength = (char)depth;
        codeTable[root->symbol].bitStream = bits;
    }
    bits = bits << 1;
    if(root->left != NULL){
        makeHuffmanCode(root->left, depth+1);
        bits = bits >> 1;
    }
    if(root->right != NULL){
        bits = bits | 1;
        makeHuffmanCode(root->right, depth+1);
        bits = bits >> 1;
    }
}

void outputCompressedFile(string fileName, int fileLength){
    ifstream inputFile;
    ofstream outputFile(fileName+".hz", ifstream::binary);

    //code for file header
    char temp;
    for(int i=3; i>=0; i--){
        outputFile << (char)(fileLength >> (i*8));
    }
    int contentsLength=0;
    inputFile.open(fileName);
    for(int i=0; i<128; i++){
        outputFile << codeTable[i].bitLength;
        for(int j=3; j>=0; j--){
            outputFile << (char)(codeTable[i].bitStream >> (j*8));
        }
    }

    // code for compressed file contents
    while(!inputFile.read(buf, BUF_SIZE).eof()){
        for(int i=0; i<BUF_SIZE; i++){
            if(buf[i] == '\0')
                break;
            binBuffer = (binBuffer << codeTable[buf[i]].bitLength) | codeTable[buf[i]].bitStream;
            occupiedBinBufferSize += codeTable[buf[i]].bitLength;

            while(occupiedBinBufferSize >= 8){
                char byte = (char) (binBuffer >> (occupiedBinBufferSize-8));
                outputFile << byte;
                occupiedBinBufferSize -= 8;
            }
        }
    }
    if(occupiedBinBufferSize > 0){
        char byte = (char)binBuffer;
        outputFile << byte;
    }
}

void compressFile(string fileName){
    ifstream inputFile(fileName, ifstream::binary);
    vector<CharFrequency*> v;
    CharFrequency* cf;
    CharFrequency *p, *q;
    int fileLength = 0;

    initializeCount();

    while(!inputFile.read(buf, BUF_SIZE).eof()){
        for(int i =0; i<BUF_SIZE; i++){
            if(buf[i] == '\0')
                break;
            charCount[buf[i]]++;
            fileLength++;
        }
    }

    for(int i=0; i<CHAR_SCOPE; i++){
        if(charCount[i] == 0)
            continue;
        cf = new CharFrequency((char)i, charCount[i]);
        v.push_back(cf);
        // if((char)i == '\r')
        //     cout << "character: " << "\\r" << "(" << i << "), count: " << charCount[i] << endl;
        // else if((char)i == '\n')
        //     cout << "character: " << "\\n" << "(" << i << "), count: " << charCount[i] << endl;
        // else
        //     cout << "character: " << (char)i << "(" << i << "), count: " << charCount[i] << endl;
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
    makeHuffmanCode(cf, 0);
    inputFile.close();
    outputCompressedFile(fileName, fileLength);
}

int bitExtraction(int bits, int bitLength, int extractLength){
    if(bitLength >= extractLength)
        return bits >> (bitLength-extractLength);
    else
        return -1;
}

void decompressFile(string fileName){
    char byte;
    int temp=0;
    int numOfOutputChar = 0;
    int fileLength;
    ifstream inputFile(fileName, ifstream::binary);
    ofstream outputFile(fileName+".txt");
    vector<HuffmanCode> v;

    for(int i=0; i<4; i++){
        inputFile.read(&byte, 1);
        temp =  temp | (int)(unsigned char)byte;
        if(i != 3)
            temp = temp << 8;
    }
    fileLength = temp;

    // Reading header from file
    for(int i=0; i<128; i++){
        inputFile.read(&byte,1);
        codeTable[i].symbol = i;
        codeTable[i].bitLength = (int)(unsigned char) byte;
        
        temp = 0;
        for(int j=0; j<4; j++){
            inputFile.read(&byte, 1);
            temp = temp | (int)(unsigned char) byte;
            if(j != 3)
                temp = temp << 8;
        }
        codeTable[i].bitStream = temp;
        if(codeTable[i].bitLength != 0){
            v.push_back(codeTable[i]);
        }
    }

    stable_sort(v.begin(), v.end(), compareHuffmanCode);

    // Recovering original file from compressed file
    temp = 0;               // temp is used for bit buffer
    occupiedBinBufferSize = 0;
    while(numOfOutputChar < fileLength && !inputFile.eof()){
        if(occupiedBinBufferSize < 23 && !inputFile.eof()){
            inputFile.read(&byte, 1);
            temp = temp << 8;
            temp = temp | (int)(unsigned char) byte;
            occupiedBinBufferSize += 8;
        }

        for(vector<HuffmanCode>::size_type i=0; i < v.size(); i++){
            if(bitExtraction(temp, occupiedBinBufferSize, v[i].bitLength) == v[i].bitStream){
                if(numOfOutputChar < fileLength){
                    outputFile.write(&v[i].symbol, 1);
                    outputFile.flush();
                    numOfOutputChar++;
                    temp &= ~(((1 << v[i].bitLength)-1) << (occupiedBinBufferSize-v[i].bitLength));   // remove used bits
                    occupiedBinBufferSize -= v[i].bitLength;
                    i = 0;
                }
            }
        }
    }
}

int main(int argc, char** argv){
    if(argc != 3){
        cout << "Usage: " << argv[0] << " file_name compression_mode" << endl;
        return 1;
    }
    buf = new char[BUF_SIZE];
    charCount = new int[CHAR_SCOPE];
    string fileName, compressionMode;
    fileName = argv[1];
    compressionMode = argv[2];

    if(compressionMode.compare("comp")==0)
        compressFile(fileName);
    else if(compressionMode.compare("decomp")==0)
        decompressFile(fileName);

    
    return 0;
}
