#include <iostream>

int main(){
    float radius;
    const float PI = 3.14;
    float area;

    std::cout << "Enter the radius : ";
    std::cin >> radius;

    area = 2 * PI * (radius * radius);

    std::cout << "The area of the circle is : " << area << "\n";

    return 0;
}