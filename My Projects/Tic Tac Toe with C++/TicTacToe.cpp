#include <iostream>

using namespace std;

class game
{
        char board[4][4];
        string xn;
        string on;
    public:
        game();
        void setName(string xi,string oi);
        bool setX(int row,int col);
        bool setO(int row,int col);
        bool checkX();
        bool checkO();
        void printb();
};


game::game(){
    for(int i=0;i<4;i++){
        for(int j=0;j<4;j++){
            board[i][j] = '-';
        }
    }
}

void game::printb(){
    cout << "    0  1  2  3 \n";
    for(int i=0;i<4;i++){
        cout << i << " : ";
        for(int j=0;j<4;j++){
            cout << board[i][j] << "  ";
        }
        cout << "\n";
    }
}

void game::setName(string xi,string oi){
    xn = xi;
    on = oi;
}

bool game::setX(int row,int col){
    if(board[row][col] == '-'){
        board[row][col] = 'X';
        return 1;
    }
    else{
        return 0;
    }
}

bool game::setO(int row,int col){
    if(board[row][col] == '-'){
        board[row][col] = 'O';
        return 1;
    }
    else{
        return 0;
    }
}

bool game::checkX(){
    for(int i=0;i<4;i++){
        int ccount = 0; 
        for(int j=0;j<4;j++){
            if(board[i][j] == 'X'){
                ccount++;
            }
            else{
                break;
            }
        }
        if(ccount == 4){
            return 1;
        }
    }
    
    for(int i=0;i<4;i++){
        int rcount = 0; 
        for(int j=0;j<4;j++){
            if(board[j][i] == 'X'){
                rcount++;
            }
            else{
                break;
            }
        }
        if(rcount == 4){
            return 1;
        }
    }
    int d1count = 0,d2count = 0,k=3;
    for(int i=0;i<4;i++){  
        if(board[i][i] == 'X'){
            d1count++;
        }
    }
    if(d1count == 4){
        return 1;
    }    
    
    for(int i=0;i<4;i++){
        if(board[i][k] == 'X'){
            d2count++;
        }
        else{
            break;
        }
        k--;
    }
    if(d2count == 4){
        return 1;
    }
    return 0;
}

bool game::checkO(){
    for(int i=0;i<4;i++){
        int ccount = 0; 
        for(int j=0;j<4;j++){
            if(board[i][j] == 'O'){
                ccount++;
            }
            else{
                break;
            }
            
        }
        if(ccount == 4){
            return 1;
        }
    }
    
    for(int i=0;i<4;i++){
        int rcount = 0; 
        for(int j=0;j<4;j++){
            if(board[j][i] == 'O'){
                rcount++;
            }
            else{
                break;
            }   
        }
        if(rcount == 4){
            return 1;
        }
    }
    int d2count = 0,d1count = 0,k=3;
    for(int i=0;i<4;i++){ 
        if(board[i][i] == 'O'){
            d1count++;
        }
        else{
            break;
        }
    }
    if(d1count == 4){
        return 1;
    }
    
    for(int i=0;i<4;i++){ 
        if(board[i][k] == 'O'){
            d2count++;
        }
        else{
            break;
        }
        k--;   
    }
    if(d2count == 4){
        return 1;
    }

    return 0;
}

int main(){
    game xox;
    string n1,n2;
    int i,t=0;
    cout << "Enter 'X' user's name: ";
    getline(cin,n1);
    cout << "\nEnter 'O' user's name: ";
    getline(cin,n2);
    xox.setName(n1,n2);
    cout << "\n'X'->" << n1 << " & 'O'->" << n2 << "\n";
    for(i=0;i<8;i++){
        int xpr,xpc,opr,opc;
        xox.printb();
        do{
            cout << "Please enter the row and column where there is no 'X' and 'O'!\n";
            cout <<"Enter row for 'X'    :";
            cin >> xpr;
            cout <<"Enter column for 'X' :";
            cin  >> xpc;
        }while(!(xox.setX(xpr,xpc)));
        if(xox.checkX()){
            t=1;
            cout << "\n'X' user is the winner." << " Congrats " << n1 << " !\n";
            xox.printb();
            break;
        }
        xox.printb();
        do{
            cout << "\nPlease enter the row and column where there is no 'X' and 'O'!\n";
            cout <<"Enter row for 'O'    :";
            cin >> opr;
            cout <<"Enter column for 'O' :";
            cin  >> opc;
        }while(!(xox.setO(opr,opc)));
        if(xox.checkO()){
            t=1;
            cout << "\n'O' user is the winner." << " Congrats " << n2 << " !\n";
            xox.printb();
            break;
        }
    }
    if(t == 0){
        cout << "OOPS! the game is a tie. Well Played.";
    }
    
    return 0;
}