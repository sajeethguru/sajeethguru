#include<iostream>
#include<vector>

class BomberMan{
    int size;
    int player[2];
    int key[2];
    int villain;
    std::vector<std::vector<int>> villainPos;
    int bricks;
    std::vector<std::vector<int>> brickPos;
    std::vector<std::vector<char>> field;
    int bomb[2];

    public:
        BomberMan();
        bool play();
        int move(int,int);
        void printField();
        int detonate();
        void instruction();
};      

void BomberMan::instruction(){
    std::cout << "\n\n<-------------------------------------------------Game Instructions------------------------------------------------>\n";
    std::cout << "\n1. Find the key without Caught by the Villains.\n";
    std::cout << "2. you can place a bomb to detonate the bricks and villains but you shouldn't caught in its radius which is 3x3.\n";
    std::cout << "\nLabels  => 'K' - Key , 'P' - Player , 'V' - Villain , 'B' - Brick \n";
    std::cout << "To Move => Top -> 'w' , Bottom -> 's' , Left -> 'a' , Right -> 'd'\n";
    std::cout << "\t   Top-Left -> 'q' , Top-Right -> 'e' , Bottom-Left -> 'z' , Bottom-Right -> 'c'\n";
    std::cout << "Bomb    => to Place a Bomb -> 'b' , To detonate a Bomb -> 'x'\n";
    std::cout << "Press 'h' to see Instruction again in between Game.\n";
    std::cout << "\n<----------------------------------------------------------------------------------------------------------------->\n\n";
    
}

BomberMan::BomberMan(){
    instruction();
    int s,flag = 1;
    while(flag){
        std::cout << "Enter Size: ";
        std::cin >> s;
        if(s % 2 != 0){
            std::cout <<"size should be even\n";
        }
        else{
            flag = 0;
        }
    }
    size = s;
    field.assign(size,std::vector<char>(size,' '));
    field[0][0] = '+';
    char temp = 'A';
    for(int i=1;i< s;i++){
        field[i][0] = temp;
        field[0][i] = temp;
        temp++;
        field[1][i] = '*';
        field[i][1] = '*';
        field[s-1][i] = '*';
        field[i][s-1] = '*';
    }
    for(int i=3;i<size-2;i+=2){
        for(int j=3;j<size-2;j+=2){
            field[i][j] = '*';
        }
    }
    printField();
    std::string pos;
    flag = 1;
    while(flag){
        std::cout << "Enter Player Position: ";
        std::cin >> pos;
        if(pos[0] < 'B' || pos[0] > temp || pos[1] < 'B' || pos[1] > temp){
            std::cout << "Player Should be placed within the wall\n";
        }
        else if(field[pos[0] - '@'][pos[1] - '@'] != ' '){
            std::cout << "Player can't be Placed over an object\n";
        }
        else{
            player[0] = int(pos[0] - '@');
            player[1] = int(pos[1] - '@');
            field[player[0]][player[1]] = 'P';
            flag = 0;
        }
    }
            
    while(!flag){
        std::cout << "Enter the Key Position: ";
        std::cin >> pos;
        if(pos[0] < 'B' || pos[0] > temp || pos[1] < 'B' || pos[1] > temp){
            std::cout << "\nKey Should be placed within the wall\n";
        }
        else if(field[pos[0] - '@'][pos[1] - '@'] != ' '){
            std::cout << "\nKey can't be Placed over an object\n";
        }
        else{
            key[0] = int(pos[0] - '@');
            key[1] = int(pos[1] - '@');
            field[key[0]][key[1]] = 'K';
            flag = 1;
        }
    }

    std::cout << "Enter Number of Villains: ";
    std::cin >> villain;
    villainPos.assign(villain,std::vector<int>(2,0));
    for(int i=0;i<villain;i++){
        while(true){
            std::cout << "V" << i+1 << ": ";
            std::cin >> pos;
            if(pos[0] < 'B' || pos[0] > temp || pos[1] < 'B' || pos[1] > temp){
                std::cout << "\nVillain Should be placed within the wall\n";
            }
            else if(field[pos[0] - '@'][pos[1] - '@'] != ' '){
                std::cout << "\nVillain can't be Placed over an object\n";
            }
            else{
                villainPos[i][0] = int(pos[0] - '@');
                villainPos[i][1] = int(pos[1] - '@');
                field[villainPos[i][0]][villainPos[i][1]] = 'V';
                break;
            }
        }
        
    }

    std::cout << "Enter Number of Bricks:";
    std::cin >> bricks;
    brickPos.assign(bricks,std::vector<int>(2,0));
    for(int i=0;i<bricks;i++){
        while(true){
            std::cout << "B" << i+1 << ": ";
            std::cin >> pos;
            if(pos[0] < 'B' || pos[0] > temp || pos[1] < 'B' || pos[1] > temp){
                std::cout << "\nBrick Should be placed within the wall\n";
            }
            else if(field[pos[0] - '@'][pos[1] - '@'] != ' '){
                std::cout << "\nBrick can't be Placed over an object\n";
            }
            else{
                brickPos[i][0] = int(pos[0] - '@');
                brickPos[i][1] = int(pos[1] - '@');
                break;
            }
        }
        field[brickPos[i][0]][brickPos[i][1]] = 'B';
    }
}

int BomberMan::move(int i,int j){
    if(field[i][j] == '*' || field[i][j] =='B' || field[i][j] == '+'){
        return 3;
    }
    else if(field[i][j] == 'V'){
        std::cout << "Caught By Villain!\n";
        return 0;
    }
    else if(field[i][j] == 'K'){
        field[i][j] = 'P';
        player[0] = i;
        player[1] = j;
        std::cout << "Congrats! You Found the Key\n";
        return 2;
    }
    else{
        field[i][j] = 'P';
        player[0] = i;
        player[1] = j;
        return 1;
    }
}

int BomberMan::detonate(){
    int val = 3;
    for(int i = bomb[0] - 1;i <=  bomb[0] + 1; i++){
        for(int j = bomb[1] - 1;j <= bomb[1] + 1; j++){
            if(field[i][j] == '*' || field[i][j] == 'K'){
                continue;
            }
            else if(field[i][j] == 'P'){
                field[i][j] = ' ';
                val = 0;
            }
            else{
                field[i][j] = ' ';
            }
        }
    }
    bomb[0] = 0;
    bomb[1] = 0;
    std::cout << "Bomb is Detonated!\n";
    return val;
}

bool BomberMan::play(){
    char a;
    int val,currentPos[2];
    while(true){
        std::cin >> a;
        currentPos[0] = player[0];
        currentPos[1] = player[1];

        switch(a){
            case 'w':
                val = move(player[0]-1,player[1]);
                break;
            case 'a':
                val = move(player[0],player[1]-1);
                break;
            case 's':
                val = move(player[0]+1,player[1]);
                break;
            case 'd':
                val = move(player[0],player[1]+1);
                break;
            case 'q':
                val = move(player[0]-1,player[1]-1);
                break;
            case 'e':
                val = move(player[0]-1,player[1]+1);
                break;
            case 'z':
                val = move(player[0]+1,player[1]-1);
                break;
            case 'c':
                val = move(player[0]+1,player[1]+1);
                break;
            case 'b':
                if(bomb[0] == 0){
                    bomb[0] = currentPos[0];
                    bomb[1] = currentPos[1];
                    std::cout << "Bomb is Successfully Planted in " << char(bomb[0] + int('@')) << char(bomb[0] + int('@')) << "\n";
                    val = 3;
                }
                else if(bomb == currentPos){
                    char choice;
                    std::cout << "A Bomb is already Placed in " << bomb << "\nDo you Want to remove the bomb(y/n): ";
                    std::cin >>choice;
                    if(choice == 'y'){
                        bomb[0] = 0;
                        bomb[1] = 0;
                    }
                    std::cout << "Bomb is Removed\n";
                    val = 3;
                }
                else{
                    char choice;
                    std::cout << "A Bomb is already Placed in " << bomb << "\nDo you Want to detonate the bomb(y/n): ";
                    std::cin >>choice;
                    if(choice == 'y'){
                        val = detonate();
                    }
                    else{
                        val = 3;
                    }
                }
                
                break;
            case 'x':
                if(bomb[0] == 0){
                    std::cout << "No Bomb is Placed\n";
                }
                else{
                    val = detonate();
                }
                break;
            case 'h':
                instruction();
                val = 3;
                break;
        } 
        if(val == 1){
            field[currentPos[0]][currentPos[1]] = ' ';
            printField();
        }
        else if(val == 0){
            field[currentPos[0]][currentPos[1]] = ' ';
            printField();
            return 0;
        }
        else if(val == 2){
            field[currentPos[0]][currentPos[1]] = ' ';
            printField();
            return 1;
        }
        else{
            continue;
        }
    }
}

void BomberMan::printField(){
    for(int i=0;i< size;i++){
        for(int j=0;j<size;j++){
            std::cout << field[i][j] << " ";
        }
        std::cout << "\n";
    }
    if(bomb[0] == 0){
        std::cout << "Bomb is not Placed yet\n";
    }
    else{
        std::cout << "Bomb is Placed in " << char(bomb[0] + int('@')) << char(bomb[1] + int('@')) << std::endl;
    }
}
 
int main(){
    BomberMan g;
    g.printField();
    bool result = g.play();
    if(result == 1){
        std::cout << "\nGreat Play!";
    }
    else{
        std::cout << "\nGame Over!";
    }
    return 0;
}