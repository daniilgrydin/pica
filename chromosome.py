#
# Chromosome class implementation
# Zachary Prins
# March 10, 2025
# 
# Translated from C++ to Python by Daniil Grydin
# March 30, 2025
#

import random
import math
import utils
import cv2
import numpy as np
from resources import Resources
from concurrent.futures import ThreadPoolExecutor

class Chromosome:
    NUMTILES = 256    # 128x128 pixel image represented by 16x16 = 256 tiles

    def __init__(self, resources, mutation_chance=0.05):
        # Initialize tileTypes, tileColours, backgroundColour
        self.tileTypes = [0] * self.NUMTILES
        self.tileColours = [0] * self.NUMTILES
        self.backgroundColour = [0] * self.NUMTILES
        # self.backgroundColour = 0  # Single background colour for the entire image
        self.mutationChance = mutation_chance
        self.fitness = math.inf # Initialize fitness to infinity
        self.resources = resources  # Store the resources for later use
        self.image = None  # Initialize image to None
        self.NUMTYPES = len(resources.tiles)  # Number of tile types
        self.NUMCOLOURS = len(resources.colours)  # Number of tile colours

    def randomize(self):
        # Randomizes the chromosome's genome
        for i in range(self.NUMTILES):
            self.tileTypes[i] = random.randint(0, self.NUMTYPES - 1)
            self.tileColours[i] = random.randint(0, self.NUMCOLOURS - 1)
            self.backgroundColour[i] = random.randint(0, self.NUMCOLOURS - 1)
            # self.tileTypes[i] = 0
            # self.tileColours[i] = 0
            # self.backgroundColour[i] = 0
            # self.backgroundColour = 0

    def mutate(self):
        # Mutates the current chromosome using helper methods: charMutation, colourMutation, backgroundMutation
        for index in range(self.NUMTILES):
            if self.boolProb(self.mutationChance):
                self.colourMutation(index)
            if self.boolProb(self.mutationChance):
                self.charMutation(index)
            if self.boolProb(self.mutationChance):
                self.backgroundMutation(index)
        # if self.boolProb(self.mutationChance):
        #     self.backgroundMutation()

        return self

    def charMutation(self, index):
        # Performs a tile mutation on the specified tile
        # mutation = round(random.gauss(0, 3))  # Using a normal distribution to simulate gamma
        mutation = max(-5, min(5, round(random.gauss(0, 5))))
        # Add the mutation, ensuring the resulting index corresponds to a valid tile type
        new = (self.tileTypes[index] + mutation) % self.NUMTYPES
        if new < 0:
            new += self.NUMTYPES
        self.tileTypes[index] = new
        
    def colourMutation(self, index):
        # Performs a colour mutation on the specified tile
        # mutation = round(random.gauss(0, 1))  # Using a normal distribution to simulate gamma
        mutation = max(-5, min(5, round(random.gauss(0, 5))))
        # Add the mutation, ensuring the resulting index corresponds to a valid tile colour
        new = (self.tileColours[index] + mutation) % self.NUMCOLOURS
        if new < 0:
            new += self.NUMCOLOURS
        
        self.tileColours[index] = new

    def backgroundMutation(self, index=0):
        # Performs a mutation on the background colour
        # mutation = round(random.gauss(0, 1))  # Using a normal distribution to simulate gamma
        mutation = max(-5, min(5, round(random.gauss(0, 5))))
        new = (self.backgroundColour[index] + mutation) % self.NUMCOLOURS
        # new = (self.backgroundColour + mutation) % self.NUMCOLOURS
        if new < 0:
            new += self.NUMCOLOURS

        # Add the mutation, ensuring the resulting index corresponds to a valid tile colour
        self.backgroundColour[index] = new
        # self.backgroundColour = new

    def crossover(self, other):
        child = Chromosome(self.resources)
        index = random.randint(0, self.NUMTILES - 1)
        for i in range(self.NUMTILES):
            if i < index:
                child.tileTypes[i] = self.tileTypes[i]
                child.tileColours[i] = self.tileColours[i]
                child.backgroundColour[i] = self.backgroundColour[i]
            else:
                child.tileTypes[i] = other.tileTypes[i]
                child.tileColours[i] = other.tileColours[i]
                child.backgroundColour[i] = other.backgroundColour[i]
        # if random.random() < 0.5:
        #     child.backgroundColour = self.backgroundColour
        # else:
        #     child.backgroundColour = other.backgroundColour
        return child

    def calculateFitness(self):
        if self.image is None:
            self.image = self.toImage()
        self.fitness = np.sum((self.image.astype(np.int32) - self.resources.target.astype(np.int32)) ** 2)
        return self.fitness
    
    def setMutationChance(self, chance):
        # Sets mutation chance
        self.mutationChance = chance

    def boolProb(self, prob):
        # Returns true prob% of the time (Bernoulli distribution)
        return random.random() < prob
    
    def __eq__(self, other):
        # Check if two chromosomes are equal
        return (self.tileTypes == other.tileTypes and
                self.tileColours == other.tileColours and
                self.backgroundColour == other.backgroundColour)
    
    def display(self):
        # chromosome = self.toImage()
        # combined_image = target.copy()
        combined_image = cv2.hconcat([self.image, self.resources.target])
        return combined_image
        
    def toImage(self):
        # Precompute reshaped tiles, colours, and backgrounds for all tiles
        tiles = np.array([self.resources.tiles[t] for t in self.tileTypes])
        colours = np.array([self.resources.colours[c] for c in self.tileColours])
        backgrounds = np.array([self.resources.colours[b] for b in self.backgroundColour])
        # backgrounds = self.resources.colours[self.backgroundColour]  # Single background colour for the entire image
        # backgrounds = np.repeat(backgrounds[np.newaxis, :], self.NUMTILES, axis=0)  # Repeat for all tiles

        # Reshape tiles, colours, and backgrounds for vectorized processing
        reshaped_tiles = tiles[..., np.newaxis] > 128  # Create masks for all tiles
        reshaped_colours = np.repeat(colours[:, np.newaxis, np.newaxis, :], 8, axis=1).repeat(8, axis=2)
        reshaped_backgrounds = np.repeat(backgrounds[:, np.newaxis, np.newaxis, :], 8, axis=1).repeat(8, axis=2)

        # Compute tile images using broadcasting
        tile_images = np.where(reshaped_tiles, reshaped_colours, reshaped_backgrounds)

        # Reshape the tile images into a grid
        grid = tile_images.reshape(16, 16, 8, 8, 3).swapaxes(1, 2).reshape(16 * 8, 16 * 8, 3)

        self.image = grid
        return grid
    
    def copy(self):
        # Create a deep copy of the chromosome
        new_chromosome = Chromosome(self.resources, self.mutationChance)
        new_chromosome.tileTypes = self.tileTypes.copy()
        new_chromosome.tileColours = self.tileColours.copy()
        new_chromosome.backgroundColour = self.backgroundColour.copy()
        # new_chromosome.backgroundColour = self.backgroundColour
        return new_chromosome

class Population:
    def __init__(self, resources, size=100):
        # Initialize the population with a specified size
        self.population = [Chromosome(resources) for _ in range(size)]
        self.population_fitness = [0.0] * size
        self.size = size
        self.resources = resources

        for i in range(size):
            self.population[i].randomize()
        
        self.sort()
        
        
    def sort(self):
        for i in range(self.size):
            self.population_fitness[i] = self.population[i].calculateFitness()
            
        # with ThreadPoolExecutor() as executor:
        #     fitnesses = list(executor.map(lambda c: c.calculateFitness(), self.population))
        #     for i, fitness in enumerate(fitnesses):
        #         self.population[i].fitness = fitness
                
        # Sort the population based on fitness
        self.population.sort(key=lambda x: x.fitness, reverse=False)
        # self.population_fitness = [c.fitness for c in self.population]

    def getChromosome(self, index):
        # Returns the chromosome at the specified index
        return self.population[index]

    def step(self):
        tenth = 20  # Keep the top 10% of the population
        number_of_children = self.size - tenth
    
        # Generate offspring
        with ThreadPoolExecutor() as executor:
            parent_pairs = [(random.choice(self.population), random.choice(self.population)) for _ in range(number_of_children)]
            offsprings = list(executor.map(create_offspring, parent_pairs))
    
        # Preserve the top 10% and replace the rest with offspring
        self.population[tenth:] = offsprings
    
        # Recalculate fitness for the new population
        self.sort()
        
def create_offspring(pair):
    parent1, parent2 = pair
    return parent1.copy().mutate()