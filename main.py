"""
Main script for running the genetic algorithm.

This script initializes a population of chromosomes, evolves them over generations,
and displays the best chromosomes in real-time. It also allows saving images of the
best chromosomes and the population at regular intervals.

Author: Daniil Grydin
Date: April 1, 2025
"""

import time
import cv2
import numpy as np
from typing import List
from chromosome import Chromosome, Population
from resources import Resources

# Constants
GENERATIONS_PER_UPDATE: int = 1
INITIAL_GOAL: int = 100
PREVIEW_WIDTH: int = 256
PREVIEW_HEIGHT: int = 256
OUTPUT_DIR: str = "output"
GIF_DIR: str = "gif"


def main() -> None:
    """
    Main function to run the genetic algorithm.

    This function initializes the population, evolves it over generations,
    and displays the best chromosomes in real-time. It also handles user input
    for saving images and exiting the program.
    """
    # Initialize variables
    goal: int = INITIAL_GOAL
    generation_count: int = 0
    population: Population = Population(Resources(input("Input file name/location: ")), size=100)
    generation: int = 0
    start_time: float = time.time()
    last_update_time: float = time.time()

    while True:
        # Perform one generation step
        population.step()
        generation += 1
        generation_count += 1

        # Update display every `GENERATIONS_PER_UPDATE` generations
        if generation % GENERATIONS_PER_UPDATE == 0:
            # Get the top chromosomes and their images
            top_chromosomes: List[Chromosome] = population.population[:6]
            combined_images: np.ndarray = cv2.hconcat([chrom.image for chrom in top_chromosomes])
            cv2.imshow("Population", combined_images)

            # Display the best chromosome along side the original image
            best_chromosome_preview: np.ndarray = top_chromosomes[0].to_image()
            best_chromosome_preview = cv2.resize(best_chromosome_preview, (PREVIEW_WIDTH, PREVIEW_HEIGHT), interpolation=cv2.INTER_NEAREST)
            original_image: np.ndarray = population.resources.target.copy()
            original_image = cv2.resize(original_image, (PREVIEW_WIDTH, PREVIEW_HEIGHT))
            combined_preview: np.ndarray = cv2.hconcat([original_image, best_chromosome_preview])
            cv2.imshow("Best Chromosome", combined_preview)

            # Print statistics
            elapsed_time: float = time.time() - last_update_time
            total_time: float = time.time() - start_time
            print(
                f"Best Fitness: {top_chromosomes[0].fitness}\t[Generation: {generation}]\t"
                f"FPS: {GENERATIONS_PER_UPDATE / elapsed_time:.2f}\t"
                f"Total Time: {total_time:.2f}s"
            )
            last_update_time = time.time()

        # Handle user input
        key = cv2.waitKey(1) & 0xFF
        if key == ord('q'):  # Quit the program
            break
        elif key == ord('s'):  # Save the best chromosome image
            save_best_chromosome(top_chromosomes[0], generation)

        # Save population image periodically
        if generation_count >= goal:
            generation_count = 0
            goal = int(goal * 1.05)  # Gradually increase the goal
            save_population_image(top_chromosomes[0], generation)

    # Print final statistics and cleanup
    total_time: float = time.time() - start_time
    print(f"Total Time: {total_time:.2f}s")
    print(f"Total Generations: {generation}")
    print(f"Average FPS: {generation / total_time:.2f}")
    print(f"Best Fitness: {top_chromosomes[0].fitness}")
    cv2.destroyAllWindows()


def save_best_chromosome(chromosome: Chromosome, generation: int) -> None:
    """
    Save the best chromosome's image to the output directory.

    Args:
        chromosome (Chromosome): The best chromosome to save.
        generation (int): The current generation number.
    """
    timestamp: str = time.strftime("%Y%m%dt%H%M%S")
    file_name: str = f"{OUTPUT_DIR}/g{generation}d{timestamp}f{chromosome.fitness:.0f}.png"
    cv2.imwrite(file_name, chromosome.image)
    print(f"Saved best chromosome image as `{file_name}`")


def save_population_image(chromosome: Chromosome, generation: int) -> None:
    """
    Save the best chromosome's image to the GIF directory.

    Args:
        chromosome (Chromosome): The best chromosome in the population.
        generation (int): The current generation number.
    """
    file_name: str = f"{GIF_DIR}/frame_{generation}.png"
    cv2.imwrite(file_name, chromosome.image)
    print(f"Saved gif frame as `{file_name}`")


if __name__ == "__main__":
    main()