/*
* Chromosome class Definition
 * Zachary Prins
 * March 10, 2025
 */
#ifndef CHROMOSOME_H
#define CHROMOSOME_H

//various include statements I've omitted for conciseness
#include <random>
#include <stdlib.h>
#include <ctime>
#include <iomanip>
#include <iostream>
#include <map>
#include <string>
#include <cmath>

//random number generator object
std::random_device rd;  // Seed generator
std::mt19937 gen(rd()); // Mersenne Twister PRNG

std::gamma_distribution<> gammaDis(1.0, 1);

class Chromosome {

private:
    static int const NUMTYPES = 128;    //PETSCII type set has 128 unique characters
    static int const NUMCOLOURS = 16;   //PETSCII type set has 16 colours
    static int const NUMTILES = 256;    //128x128 pixel image represented by 16x16 = 256 tiles

    //each index represents the state of the corresponding square
    int tileTypes[NUMTILES];
    int tileColours[NUMTILES];

    int backgroundColour;

    void charMutation(int);      //performs a tile mutation
    void colourMutation(int);    //performs a colour mutation
    void backgroundMutation();   //performs a mutation on the background colour

    static bool boolProb(double prob);  //returns true prob% of the time

public:
    float mutationChance;               //probability of a mutation happening

    Chromosome();                       //constructor
    void randomize();                   //Randomly assigns values to each square
    Chromosome* mutate();               //performs a mutation using helper methods
    //performs a crossover between two chromosome and returns the results chromosome
    Chromosome* crossover(Chromosome* other);
    int calculateFitness()const;        //determines the fitness of the chromosome
    void setMutationChance(float);
    ~Chromosome();                      //destructor
};



#endif //CHROMOSOME_H
