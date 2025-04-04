/*
 * Chromosome class implementation
 * Zachary Prins
 * March 10, 2025
 */
#include "Chromosome.h"

//constructor
Chromosome::Chromosome() : tileTypes() ,tileColours(), mutationChance(0.02){};

//randomizes the chromosome's genome
void Chromosome::randomize() {
    srand(time(0));

    for(int i = 0; i < NUMTILES; i++) {
        tileTypes[i] = std::rand() % NUMTYPES;
        tileColours[i] = std::rand() % NUMCOLOURS;
    }

    backgroundColour = std::rand() % NUMCOLOURS;
}

//Mutates the current chromosome using helper methods: charMutation, colourMutation, backgroundMutation
Chromosome* Chromosome::mutate() {

    //chance of mutating the background
    if(boolProb(mutationChance)) {
        backgroundMutation();
    }

    for(int index = 0; index < NUMTILES; index++) {
        //mutationChance% of colour mutation on each tile
        if(boolProb(mutationChance)) {
            colourMutation(index);
        }
        //mutationChance% chance of character mutation on each tile
        if(boolProb(mutationChance)) {
            charMutation(index);
        }
    }

    return  this;
}

//performs a tile mutation on the specified tile
void Chromosome::charMutation(int index) {
    srand(time(0));

    //generating size of mutation
    int mutation = std::ceil(gammaDis(gen));
    mutation *= (std::rand() % 2 == 0? 1 : -1);//Randomly choose if increase or decrease mutation

    //add the mutation, ensuring the resulting index corresponds to a valid tile type
    this->tileTypes[index] = (this->tileTypes[index] + mutation) % NUMTYPES;
}

//performs a colour mutation on the specified tile
void Chromosome::colourMutation(int index) {
    srand(time(0));

    //generating size of mutation
    int mutation = std::ceil(gammaDis(gen));
    mutation *= std::rand() % 2 == 0? 1 : -1;//Randomly choose if increase or decrease mutation

    //add the mutation, ensuring the resulting index corresponds to a valid tile colour
    this->tileTypes[index] = (this->tileTypes[index] + mutation) % NUMCOLOURS;
}

//performs a mutation on the background colour
void Chromosome::backgroundMutation() {

    //generating size of mutation
    int mutation = std::ceil(gammaDis(gen));
    mutation *= std::rand() % 2 == 0? 1 : -1;//Randomly choose if increase or decrease mutation

    //add the mutation, ensuring the resulting index corresponds to a valid tile colour
    backgroundColour = (backgroundColour + mutation) % NUMCOLOURS;
}

//performs a crossover between two chromosome and returns the resulting chromosome
Chromosome* Chromosome::crossover(Chromosome* other) {
    Chromosome *child = new Chromosome();

    for(int index = 0; index < NUMTILES; index++) {
        //50% probability of tile coming from each parent
        if(boolProb(0.5)) {
            child->tileTypes[index] = this->tileTypes[index];
        }else {
            child->tileTypes[index] = other->tileTypes[index];
        }

        //50% probability of colour coming from each parent
        if(boolProb(0.5)) {
            child->tileColours[index] = this->tileColours[index];
        }else {
            child->tileColours[index] = other->tileColours[index];
        }
    }

    //50% probability of background colour coming from each parent
    if(boolProb(0.5)) {
        child->backgroundColour = this->backgroundColour;
    } else {
        child->backgroundColour = other->backgroundColour;
    }
    return  child;
}

//determines the fitness of the chromosome
int Chromosome::calculateFitness() const{
    //to be implemented
    return -1;
}

//sets mutation chance
void Chromosome::setMutationChance(float chance) {
    mutationChance = chance;
}

//destructor
Chromosome::~Chromosome() = default;

//returns true prob% of the time
bool Chromosome::boolProb( double prob )   // probability between 0.0 and 1.0
{
    std::bernoulli_distribution d(prob);
    return d(gen);
}
