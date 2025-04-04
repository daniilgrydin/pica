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
from typing import List, Tuple
from concurrent.futures import ThreadPoolExecutor


class Chromosome:
    NUMTILES: int = 256  # 128x128 pixel image represented by 16x16 = 256 tiles

    def __init__(self, resources: Resources, mutation_chance: float = 0.01):
        self.tileTypes: List[int] = [0] * self.NUMTILES
        self.tileColours: List[int] = [0] * self.NUMTILES
        self.backgroundColour: List[int] = [0] * self.NUMTILES
        self.mutationChance: float = mutation_chance
        self.fitness: float = math.inf
        self.resources: Resources = resources
        self.image: np.ndarray | None = None
        self.NUMTYPES: int = len(resources.tiles)
        self.NUMCOLOURS: int = len(resources.colours)

    def randomize(self) -> None:
        for i in range(self.NUMTILES):
            self.tileTypes[i] = random.randint(0, self.NUMTYPES - 1)
            self.tileColours[i] = random.randint(0, self.NUMCOLOURS - 1)
            self.backgroundColour[i] = random.randint(0, self.NUMCOLOURS - 1)

    def mutate(self) -> "Chromosome":
        for index in range(self.NUMTILES):
            if self.boolProb(self.mutationChance):
                self.colourMutation(index)
            if self.boolProb(self.mutationChance):
                self.charMutation(index)
            if self.boolProb(self.mutationChance):
                self.backgroundMutation(index)
        return self

    def charMutation(self, index: int) -> None:
        mutation: int = max(-5, min(5, round(random.gauss(0, 2))))
        new: int = self.tileTypes[index] + mutation
        if new >= self.NUMTYPES:
            new -= self.NUMTYPES
            self.backgroundColour[index], self.tileColours[index] = self.backgroundColour[index], self.tileColours[index]
        elif new < 0:
            new += self.NUMTYPES
            self.backgroundColour[index], self.tileColours[index] = self.backgroundColour[index], self.tileColours[index]
        self.tileTypes[index] = new

    def colourMutation(self, index: int) -> None:
        mutation: int = max(-5, min(5, round(random.gauss(0, 1))))
        new: int = (self.tileColours[index] + mutation) % self.NUMCOLOURS
        if new < 0:
            new += self.NUMCOLOURS
        self.tileColours[index] = new

    def backgroundMutation(self, index: int = 0) -> None:
        mutation: int = max(-5, min(5, round(random.gauss(0, 1))))
        new: int = (self.backgroundColour[index] + mutation) % self.NUMCOLOURS
        if new < 0:
            new += self.NUMCOLOURS
        self.backgroundColour[index] = new

    def crossover(self, other: "Chromosome") -> "Chromosome":
        child: Chromosome = Chromosome(self.resources)
        index: int = random.randint(0, self.NUMTILES - 1)
        for i in range(self.NUMTILES):
            if i < index:
                child.tileTypes[i] = self.tileTypes[i]
                child.tileColours[i] = self.tileColours[i]
                child.backgroundColour[i] = self.backgroundColour[i]
            else:
                child.tileTypes[i] = other.tileTypes[i]
                child.tileColours[i] = other.tileColours[i]
                child.backgroundColour[i] = other.backgroundColour[i]
        return child

    def calculateFitness(self) -> float:
        if self.image is None:
            self.image = self.toImage()
        self.fitness = float(np.sum((self.image.astype(np.int32) - self.resources.target.astype(np.int32)) ** 2))
        return self.fitness

    def setMutationChance(self, chance: float) -> None:
        self.mutationChance = chance

    def boolProb(self, prob: float) -> bool:
        return random.random() < prob

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, Chromosome):
            return False
        return (
            self.tileTypes == other.tileTypes and
            self.tileColours == other.tileColours and
            self.backgroundColour == other.backgroundColour
        )

    def display(self) -> np.ndarray:
        combined_image: np.ndarray = cv2.hconcat([self.image, self.resources.target])
        return combined_image

    def toImage(self) -> np.ndarray:
        tiles: np.ndarray = np.array([self.resources.tiles[t] for t in self.tileTypes])
        colours: np.ndarray = np.array([self.resources.colours[c] for c in self.tileColours])
        backgrounds: np.ndarray = np.array([self.resources.colours[b] for b in self.backgroundColour])

        reshaped_tiles: np.ndarray = tiles[..., np.newaxis] > 128
        reshaped_colours: np.ndarray = np.repeat(colours[:, np.newaxis, np.newaxis, :], 8, axis=1).repeat(8, axis=2)
        reshaped_backgrounds: np.ndarray = np.repeat(backgrounds[:, np.newaxis, np.newaxis, :], 8, axis=1).repeat(8, axis=2)

        tile_images: np.ndarray = np.where(reshaped_tiles, reshaped_colours, reshaped_backgrounds)
        grid: np.ndarray = tile_images.reshape(16, 16, 8, 8, 3).swapaxes(1, 2).reshape(16 * 8, 16 * 8, 3)

        self.image = grid
        return grid

    def copy(self) -> "Chromosome":
        new_chromosome: Chromosome = Chromosome(self.resources, self.mutationChance)
        new_chromosome.tileTypes = self.tileTypes.copy()
        new_chromosome.tileColours = self.tileColours.copy()
        new_chromosome.backgroundColour = self.backgroundColour.copy()
        return new_chromosome


class Population:
    def __init__(self, resources: Resources, size: int = 100):
        self.population: List[Chromosome] = [Chromosome(resources) for _ in range(size)]
        self.population_fitness: List[float] = [0.0] * size
        self.size: int = size
        self.resources: Resources = resources

        for i in range(size):
            self.population[i].randomize()

        self.sort()

    def sort(self) -> None:
        for i in range(self.size):
            self.population_fitness[i] = self.population[i].calculateFitness()

        self.population.sort(key=lambda x: x.fitness, reverse=False)

    def getChromosome(self, index: int) -> Chromosome:
        return self.population[index]

    def step(self) -> None:
        tenth: int = 20
        number_of_children: int = self.size - tenth

        parent_pairs: List[Tuple[Chromosome, Chromosome]] = [
            (random.choice(self.population), random.choice(self.population)) for _ in range(number_of_children)
        ]

        with ThreadPoolExecutor() as executor:
            offsprings: List[Chromosome] = list(executor.map(create_offspring, parent_pairs))

        self.population[tenth:] = offsprings
        self.sort()


def create_offspring(pair: Tuple[Chromosome, Chromosome]) -> Chromosome:
    parent1, parent2 = pair
    return parent1.crossover(parent2).mutate()