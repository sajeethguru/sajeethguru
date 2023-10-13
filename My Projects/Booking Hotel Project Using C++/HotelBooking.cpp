#include<iostream>
#include<string>
#include<fstream>

void logo(){
    std::cout << "\n\n\n=========================================\n";
    std::cout << "=\t\t\t\t\t=\n";
    std::cout << "=\t\tABC HOTEL\t\t=\n";
    std::cout << "=\t\t\t\t\t=\n";
    std::cout << "=========================================" << std::endl;
}

class Hotel{
    private:
        int room_no;
        std::string name;
        int age;
        int phone;
        std::string address;
        int days;
        int count;
        float fare;
    public:
        void mainmenu();
        void addRoom();
        void display();
        void showDetails(int);
        void edit();
        void rooms();
        bool checkRoom(int);
        void modify();
        void deleteRecord();
};

void Hotel::mainmenu(){
    int option;
    while(option != 5){
        logo();
        std::cout << "\n\t ----------------------- \n";
        std::cout << "\t|\t\t\t|\n";
        std::cout << "\t|\tMain Menu\t|\n";
        std::cout << "\t|\t\t\t|\n";
        std::cout << "\t -----------------------\n ";
        std::cout << "\n\t1. Book a Room";
        std::cout << "\n\t2. Rooms Allocated";
        std::cout << "\n\t3. Customer Record";
        std::cout << "\n\t4. Edit Record";
        std::cout << "\n\t5. Exit";
        std::cout << "\n\tEnter Your Choice: ";
        std::cin >> option;
        switch(option){
            case 1: addRoom();break;
            case 2: rooms();break;
            case 3: display();break;
            case 4: edit();break;
            case 5: break;
            default:
                std::cout << "\n\t Invalid Choice, Please select again!" << std::endl;
        }
    }
}

void Hotel::addRoom(){
    logo();
    int roomNo;
    std::cout << "\n\tEnter the Room Number: ";
    std::cin >> roomNo;
    std::fstream fout;
    fout.open("Record.dat",std::ios::app | std::ios::binary);
    if(checkRoom(roomNo)){
        std::cout << "\n\n\tEnter Customer Details: \n" << std::endl;
        room_no = roomNo;
        std::cout << "\n\tName : ";
        std::cin >> name;
        std::cout << "\n\tAge : ";
        std::cin >> age;
        std::cout << "\n\tPhone: ";
        std::cin >> phone;
        std::cout << "\n\tAddress: ";
        std::cin >> address;
        std::cout << "\n\tNo of Person: ";
        std::cin >> count;
        std::cout << "\n\tNo of Days: ";
        std::cin >> days;
        fare = days * count * 1000;
        if(fout.is_open()){
            fout.write((char*)this,sizeof(Hotel));
            std::cout << "\n\tRoom is Booked Successfully!";
            fout.close();
            showDetails(room_no);
        }
        else{
            fout.close();
            std::cout << "\n\tPlease Try again";
        }
    }
    else{
        std::cout << "\n\tRoom is Already Filled!." << std::endl;
    }
}

void Hotel::display(){
    logo();
    int roomNo;
    std::cout << "\n\tEnter Room Number: ";
    std::cin >> roomNo;
    std::fstream fin;
    fin.open("Record.dat",std::ios::in | std::ios::binary);
    unsigned short flag = 0;
    while(!fin.eof()){
        fin.read((char*)this,sizeof(Hotel));
        if(room_no == roomNo){
            std::cout << "\n\n\tName: " << name;
            std::cout << "\n\tAge: " << age;
            std::cout << "\n\tPhone: " << phone;
            std::cout << "\n\tAddress: " << address;
            std::cout << "\n\tDays: " << days;
            std::cout << "\n\tNo of Person: " << count;
            std::cout << "\n\tFare: " << fare;
            flag = 1;
            break;
        }
    }
    if(flag == 0){
        std::cout << "\n\n\tRoom is Vacant or Not Available!" << std::endl;
    }
    fin.close();
}

void Hotel::showDetails(int roomNo){
    std::fstream fin;
    fin.open("Record.dat",std::ios::in | std::ios::binary);
    while(!fin.eof()){
        fin.read((char*)this,sizeof(Hotel));
        if(room_no == roomNo){
            std::cout << "\n\n\tName: " << name;
            std::cout << "\n\tAge: " << age;
            std::cout << "\n\tPhone: " << phone;
            std::cout << "\n\tAddress: " << address;
            std::cout << "\n\tDays: " << days;
            std::cout << "\n\tNo of Person: " << count;
            std::cout << "\n\tFare: " << fare;
            break;
        }
    }
    fin.close();
}

void Hotel::rooms(){
    logo();
    std::fstream fin;
    fin.open("Record.dat",std::ios::in | std::ios::binary);
    while(!fin.eof()){
        fin.read((char*)this,sizeof(Hotel));
        std::cout << "\n\n\tRoom: " <<room_no;
        std::cout << "\n\tName: " << name;
        std::cout << "\n\tAge: " << age;
        std::cout << "\n\tPhone: " << phone;
        std::cout << "\n\tAddress: " << address;
        std::cout << "\n\tDays: " << days;
        std::cout << "\n\tNo of Person: " << count;
        std::cout << "\n\tFare: " << fare;
    }
}

bool Hotel::checkRoom(int roomNo){
    std::fstream fin;
    fin.open("Record.dat",std::ios::in | std::ios::binary);
    unsigned short flag = 0;
    while(!fin.eof()){
        fin.read((char*)this,sizeof(Hotel));
        if(room_no == roomNo){
            flag = 1;
            break;
        }
    }
    fin.close();
    if(flag == 0){
        return true;
    }
    return false;
    
}

void Hotel::edit(){
    logo();
    int choice;
    std::cout << "\n\t\tEdit Menu\n";
    std::cout << "\n\t1. Modify Customer Record";
    std::cout << "\n\t2. Delete Customer Record";
    std::cout << "\n\tEnter Your Choice: ";
    std::cin >> choice;
    switch(choice){
        case 1:modify();break;
        case 2:deleteRecord();break;
        default:
        std::cout << "Invalid Input.";
    }
}

void Hotel::modify(){
    logo();
    int roomNo,flag = 0;
    std::cout << "\n\tEnter The Room Number to Modify: ";
    std::cin >> roomNo;
    std::fstream file("Record.dat",std::ios::in|std::ios::out|std::ios::binary);
    long pos;
    while(!file.eof()){
        pos = file.tellg();
        file.read((char*)this,sizeof(Hotel));
        if(room_no == roomNo){
            std::cout << "\n\n\t\tEnter New Details" << std::endl;
            std::cout << "\n\tName : ";
            std::cin >> name;
            std::cout << "\n\tAge : ";
            std::cin >> age;
            std::cout << "\n\tPhone: ";
            std::cin >> phone;
            std::cout << "\n\tAddress: ";
            std::cin >> address;
            std::cout << "\n\tNo of Person: ";
            std::cin >> count;
            std::cout << "\n\tNo of Days: ";
            std::cin >> days;
            fare = days * count * 1000;
            file.seekg(pos);
            file.write((char*)this,sizeof(Hotel));
            std::cout << "\n\tRecord Modified Sucessfully" << std::endl;
            flag = 1;
            break;
        }
    }
    file.close();
    if(flag == 0){
        std::cout << "\n\tRoom is Vacant or Not Available" << std::endl;
    }
}

void Hotel::deleteRecord(){
    logo();
    int roomNo,flag = 0;
    std::cout << "\n\tEnter The Room Number for Deletion: ";
    std::cin >> roomNo;
    std::fstream fin("Record.dat",std::ios::in|std::ios::binary);
    std::fstream fout("temp.dat",std::ios::out|std::ios::binary);
    while(!fin.eof()){
        fin.read((char*)this,sizeof(Hotel));
        if(room_no == roomNo){
            std::cout << "\n\n\tName: " << name;
            std::cout << "\n\tAge: " << age;
            std::cout << "\n\tPhone: " << phone;
            std::cout << "\n\tAddress: " << address;
            std::cout << "\n\tDays: " << days;
            std::cout << "\n\tNo of Person: " << count;
            std::cout << "\n\tFare: " << fare;
            std::cout << "\n\n\tDo you Really want to delete?(y/n): ";
            char decision;
            std::cin >> decision;
            flag = 1;
            if(decision == 'n' || decision == 'N'){
                fout.write((char*)this,sizeof(Hotel));
            }
            else{
                continue;
            }
        }
        else{
            fout.write((char*)this,sizeof(Hotel));
        }
    }
    fin.close();
    fout.close();
    if(flag == 0){
        std::cout  << "\n\tThe Room is Either Already Empty or Not Available";
    }
    else{
        remove("Record.dat");
        rename("temp.dat","Record.dat");
    }

}

int main(){
    logo();
    std::string userName;
    std::string password;
    while(true){
        std::cout << "\nEnter Username : ";
        std::cin >> userName ;
        std::cout << "\nEnter Password : ";
        std::cin >> password;
        if(userName == "admin" && password == "1234"){
            Hotel h;
            h.mainmenu();
            break;
        }
    }
    return 0;
}