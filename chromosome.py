"""
Chromosome and Population classes for genetic algorithm implementation.

Author: Zachary Prins
Translated to Python by Daniil Grydin
Date: March 30, 2025
"""

import random
import math
import cv2
import numpy as np
from resources import Resources
from typing import List, Tuple
from concurrent.futures import ThreadPoolExecutor


class Chromosome:
    """Represents a single chromosome in a genetic algorithm."""

    NUM_TILES: int = 256  # 128x128 pixel image represented by 16x16 = 256 tiles
    TILE_SIZE: int = 8    # Size of each tile in pixels
    GRID_SIZE: int = 16   # Number of tiles along one dimension

    def __init__(self, resources: Resources, mutation_chance: float = 0.01):
        """
        Initialize a Chromosome instance.

        Args:
            resources (Resources): Shared resources like tiles and colors.
            mutation_chance (float): Probability of mutation for each tile.
        """
        self.tile_types: List[int] = [0] * self.NUM_TILES
        self.tile_colours: List[int] = [0] * self.NUM_TILES
        self.background_colours: List[int] = [0] * self.NUM_TILES
        self.mutation_chance: float = mutation_chance
        self.fitness: float = math.inf
        self.resources: Resources = resources
        self.image: np.ndarray | None = None
        self.NUM_TYPES: int = len(resources.tiles)
        self.NUM_COLOURS: int = len(resources.colours)

    def randomize(self) -> None:
        """Randomly initialize the chromosome's tiles, colors, and backgrounds."""
        self.tile_types = [random.randint(0, self.NUM_TYPES - 1) for _ in range(self.NUM_TILES)]
        self.tile_colours = [random.randint(0, self.NUM_COLOURS - 1) for _ in range(self.NUM_TILES)]
        self.background_colours = [random.randint(0, self.NUM_COLOURS - 1) for _ in range(self.NUM_TILES)]

    def mutate(self) -> "Chromosome":
        """Apply mutations to the chromosome."""
        for index in range(self.NUM_TILES):
            if random.random() < self.mutation_chance:
                self.mutate_colour(index)
            if random.random() < self.mutation_chance:
                self.mutate_tile_type(index)
            if random.random() < self.mutation_chance:
                self.mutate_background(index)
        return self

    def mutate_tile_type(self, index: int) -> None:
        """Mutate the tile type at a given index."""
        mutation = max(-64, min(64, round(random.gauss(0, 4))))
        new_type = (self.tile_types[index] + mutation) % self.NUM_TYPES
        self.tile_types[index] = new_type

    def mutate_colour(self, index: int) -> None:
        """Mutate the tile color at a given index."""
        mutation = max(-10, min(10, round(random.gauss(0, 3))))
        new_colour = (self.tile_colours[index] + mutation) % self.NUM_COLOURS
        self.tile_colours[index] = new_colour

    def mutate_background(self, index: int) -> None:
        """Mutate the background color at a given index."""
        mutation = max(-10, min(10, round(random.gauss(0, 3))))
        new_background = (self.background_colours[index] + mutation) % self.NUM_COLOURS
        self.background_colours[index] = new_background

    def crossover(self, other: "Chromosome") -> "Chromosome":
        """Perform crossover with another chromosome to produce an offspring."""
        child = Chromosome(self.resources)
        for i in range(self.NUM_TILES):
            if random.random() < 0.5:
                child.tile_types[i] = self.tile_types[i]
                child.tile_colours[i] = self.tile_colours[i]
                child.background_colours[i] = self.background_colours[i]
            else:
                child.tile_types[i] = other.tile_types[i]
                child.tile_colours[i] = other.tile_colours[i]
                child.background_colours[i] = other.background_colours[i]
        return child

    def calculate_fitness(self) -> float:
        """Calculate the fitness of the chromosome."""
        if self.image is None:
            self.image = self.to_image()
        self.fitness = float(np.sum((self.image.astype(np.int32) - self.resources.target.astype(np.int32)) ** 2))
        return self.fitness

    def to_image(self) -> np.ndarray:
        """Convert the chromosome's data into an image."""
        tiles = np.array([self.resources.tiles[t] for t in self.tile_types])
        colours = np.array([self.resources.colours[c] for c in self.tile_colours])
        backgrounds = np.array([self.resources.colours[b] for b in self.background_colours])

        reshaped_tiles = tiles[..., np.newaxis] > 128
        reshaped_colours = np.repeat(colours[:, np.newaxis, np.newaxis, :], self.TILE_SIZE, axis=1).repeat(self.TILE_SIZE, axis=2)
        reshaped_backgrounds = np.repeat(backgrounds[:, np.newaxis, np.newaxis, :], self.TILE_SIZE, axis=1).repeat(self.TILE_SIZE, axis=2)

        tile_images = np.where(reshaped_tiles, reshaped_colours, reshaped_backgrounds)
        grid = tile_images.reshape(self.GRID_SIZE, self.GRID_SIZE, self.TILE_SIZE, self.TILE_SIZE, 3).swapaxes(1, 2).reshape(
            self.GRID_SIZE * self.TILE_SIZE, self.GRID_SIZE * self.TILE_SIZE, 3
        )

        self.image = grid
        return grid

    def copy(self) -> "Chromosome":
        """Create a copy of the chromosome."""
        new_chromosome = Chromosome(self.resources, self.mutation_chance)
        new_chromosome.tile_types = self.tile_types.copy()
        new_chromosome.tile_colours = self.tile_colours.copy()
        new_chromosome.background_colours = self.background_colours.copy()
        return new_chromosome


class Population:
    """Represents a population of chromosomes in a genetic algorithm."""

    def __init__(self, resources: Resources, size: int = 100):
        """
        Initialize a Population instance.

        Args:
            resources (Resources): Shared resources like tiles and colors.
            size (int): Number of chromosomes in the population.
        """
        self.population: List[Chromosome] = [Chromosome(resources) for _ in range(size)]
        self.size: int = size
        self.resources: Resources = resources

        for chromosome in self.population:
            chromosome.randomize()

        self.sort()

    def sort(self) -> None:
        """Sort the population by fitness."""
        self.population.sort(key=lambda x: x.calculate_fitness())

    def step(self) -> None:
        """Perform one generation step."""
        top_fraction = self.size // 5
        number_of_children = self.size - top_fraction

        parent_pairs = [
            (random.choice(self.population), random.choice(self.population)) for _ in range(number_of_children)
        ]

        with ThreadPoolExecutor() as executor:
            offsprings = list(executor.map(create_offspring, parent_pairs))

        self.population[top_fraction:] = offsprings
        self.sort()


def create_offspring(pair: Tuple[Chromosome, Chromosome]) -> Chromosome:
    """Create an offspring from a pair of parent chromosomes."""
    parent1, parent2 = pair
    return parent1.crossover(parent2).mutate()