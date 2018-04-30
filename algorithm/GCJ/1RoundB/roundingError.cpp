#include<iostream>
#include<cmath>

using namespace std;

int T, N, L;
int* Li;
int max_percentage;
int base_percent;

int get_percent_sum(){
    int percent_sum=0;
    for(int i=0; i<L; i++){
        percent_sum += (int)floor(((double)Li[i]/N*100)+0.5);
    }
    return percent_sum;
}

void back_track(int R){
    if(R == 0){
        int temp = get_percent_sum()+base_percent;
        max_percentage = (temp > max_percentage)?temp:max_percentage;
        return;
    }

    for(int i=0; i<L; i++){
        Li[i]++;
        back_track(R-1);
        Li[i]--;
    }
}

int main(void){
    cin >> T;
    for(int t=0; t<T; t++){
        cin >> N;
        cin >> L;
        Li = new int[L];
        int R = 0;
        max_percentage = 0;
        base_percent = 0;
        for(int i=0; i<L; i++){
            cin >> Li[i];
            R += Li[i];
        }
        R = N - R;

        int pieceSize=0;
        double onePiece;
        for(int i=0; i<R; i++){
            onePiece = (double)(i+1)/N*100;
            if((onePiece - floor(onePiece))>=0.5)
                pieceSize = i+1;
                break;
        }
        if(pieceSize != 0){
            base_percent = (R/pieceSize)*floor(onePiece+0.5);
            R = R%pieceSize;
        }
        // cout << "onepice : " << onePiece << endl;
        // cout << "piecesize : " << pieceSize << endl;
        // cout << "base : " << base_percent << endl;
        back_track(R);
        cout << "Case #" << t+1 << ": " << max_percentage << endl;
    }
    return 0;
}