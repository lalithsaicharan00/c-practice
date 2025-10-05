#include <iostream>

int main(){
    float pencil;
    float pen;
    float eraser;

    std::cout << "Enter the pencil price : ";
    std::cin >> pencil;

    std::cout << "Enter the pen price : ";
    std::cin >> pen;

    std::cout << "Enter the eraser price : ";
    std::cin >> eraser;

    float subtotal = pencil + pen + eraser;
    float gst = (18 * subtotal) / 100;
    float total = subtotal + gst;

    std::cout << "\n";
    std::cout << "\n";
    std::cout << "\n";

    std::cout << "Subtotal : " << subtotal<<"\n";
    std::cout << "GST : " << gst<<"\n";
    std::cout << "-------------------- \n";
    std::cout << "Total : " << total<<"\n";

    return 0;
}