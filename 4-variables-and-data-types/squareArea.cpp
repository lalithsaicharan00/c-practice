#include <iostream>

int main(){
    float oneSide;
    std::cout << "Enter the side of the square : ";
    std::cin >> oneSide;

    float area = oneSide * oneSide;
    std::cout << "The area of the suqare is : " << area << "\n";
    return 0;
}