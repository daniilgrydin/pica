//
// Created by zacha on 2025-03-19.
//

#include <random>
#include <stdlib.h>
#include <ctime>
#include <iomanip>
#include <iostream>
#include <map>
#include <string>
#include <cmath>

int main() {

    std::random_device rd;
    std::mt19937 gen(rd());
    std::gamma_distribution<> f(1.0, 1);


    // Draw a sample from the normal distribution and round it to an integer.
    auto random_int = [&f, &gen]{ return std::ceil(f(gen)); };

    std::map<long, unsigned> histogram{};
    for (auto n{10000}; n; --n)
        ++histogram[random_int()];

    for (const auto [k, v] : histogram)
        std::cout << std::setw(2) << k << ' ' << std::string(v / 200, '*') << '\n';

/*int yes = 0;

    for(int i = 0; i < 1000; i ++) {
        std::bernoulli_distribution d(0.3);
        if( d(gen))
            yes++;
    }

    std::cout << yes << std::endl;*/


}

