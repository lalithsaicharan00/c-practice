#include <iostream>

int main(){
    int firstNumber;
    std::cout << "Enter first number : ";
    std::cin >> firstNumber;
    std::cout << "\n";

    int secondNumber;
    std::cout << "Enter second number : ";
    std::cin >> secondNumber;
    std::cout << "\n";

    int avg = firstNumber + secondNumber;
    std::cout << "The avg of two numbers is : " << avg << "\n";
    return 0;
}