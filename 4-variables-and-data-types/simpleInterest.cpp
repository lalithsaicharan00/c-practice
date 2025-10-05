#include <iostream>

int main(){
    float amount;
    float rate;
    float time;
    float si;

    std::cout << "Enter the priciple amount : ";
    std::cin >> amount;
    std::cout << "Enter the rate of interest : ";
    std::cin >> rate;
    std::cout << "Enter the time ( in years ) : ";
    std::cin >> time;

    si = (amount * rate * time) / 100;

    std::cout << "The simple interest is : " << si << "\n";

    return 0;
}