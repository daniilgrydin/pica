import cv2
import chromosome
import resources
import time
import numpy
from typing import List
# from collections import deque
# import numpy as np

# def compute_alpha(sequence):
#     sequence = np.array(sequence)
#     L = sequence[-1]  # estimated limit (can be changed if known)
    
#     # Compute errors
#     errors = np.abs(sequence - L)
    
#     # Avoid division by zero or log of zero
#     with np.errstate(divide='ignore', invalid='ignore'):
#         alpha_n = np.log(errors[2:] / errors[1:-1]) / np.log(errors[1:-1] / errors[:-2])
    
#     return alpha_n

gens_per_update: int = 1

goal = 100

def main():
    global goal, gens_per_update
    # limited_array = deque(maxlen=100)
    count = 0
    population: chromosome.Population = chromosome.Population(resources.Resources(input("input file name/location: ")), size=100)
    generation: int = 0
    last_time: float = time.time()
    first_time: float = time.time()

    while True:
        population.step()
        generation += 1
        count += 1
        
        if generation % gens_per_update == 0:
            # Display the best chromosome
            chroms: List[chromosome.Chromosome] = population.population[:6].copy()
            images: numpy.ndarray = cv2.hconcat([chrom.image for chrom in chroms])
            cv2.imshow("Population", images)
            preview: numpy.ndarray = cv2.resize(chroms[0].display(), (512, 256), interpolation=cv2.INTER_NEAREST)
            cv2.imshow("Best Chromosome", preview)
            print("Best Fitness:", chroms[0].fitness, f"[{generation}]", "FPS", gens_per_update/(time.time() - last_time), "Time:", time.time() - first_time)
            last_time = time.time()
            # limited_array.append(chroms[0].fitness)
        
        # Check for exit key
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
        
        if cv2.waitKey(1) & 0xFF == ord('s'):
            
            # Save the best chromosome image
            file_name: str = str(f"output/best_{generation}-{chroms[0].fitness}.png")
            cv2.imwrite(file_name, chroms[0].image)
            print(f"Saved best chromosome image as {file_name}")
        
        if count == goal:
            count = 0
            goal *= 1.05
            goal = int(goal)
            # Save the population image every 100 generations
            file_name: str = str(f"gif/population_{generation}.png")
            cv2.imwrite(file_name, chroms[0].image)
            print(f"Saved population image as {file_name}")
    
    print("Total time:", time.time() - first_time)
    print("Total generations:", generation)
    print("Average FPS:", generation / (time.time() - first_time))
    print("Best fitness:", chroms[0].fitness)
    # Cleanup
    cv2.destroyAllWindows()
    
main()