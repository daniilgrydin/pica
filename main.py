import cv2
import chromosome
import resources
import matplotlib.pyplot as plt
import time
import numpy
from typing import List


def main():    
    population: chromosome.Population = chromosome.Population(resources.Resources(input("input file name/location: ")), size=100)
    generation: int = 0
    fitnessi: List[float] = []
    last_time: float = time.time()
    first_time: float = time.time()

    while True:
        population.step()
        generation += 1
        
        # Display the best chromosome
        chroms: List[chromosome.Chromosome] = population.population[:6].copy()
        images: numpy.ndarray = cv2.hconcat([chrom.image for chrom in chroms])
        cv2.imshow("Population", images)
        preview: numpy.ndarray = cv2.resize(chroms[0].display(), (512, 256), interpolation=cv2.INTER_NEAREST)
        cv2.imshow("Best Chromosome", preview)
        print("Best Fitness:", chroms[0].fitness, f"[{generation}]", "FPS", 1/(time.time() - last_time), time.time() - first_time)
        last_time = time.time()
        fitnessi.append(chroms[0].fitness)
        
        # Check for exit key
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
        
        if cv2.waitKey(1) & 0xFF == ord('s'):
            # Save the best chromosome image
            file_name: str = str(f"output/best_{generation}-{chroms[0].fitness}.png")
            cv2.imwrite(file_name, chroms[0].image)
            print(f"Saved best chromosome image as {file_name}")
            
        if generation % 100 == 0:
            # Save the population image every 100 generations
            file_name: str = str(f"gif/population_{generation}.png")
            cv2.imwrite(file_name, chroms[0].image)
            print(f"Saved population image as {file_name}")
    
    print("Total time:", time.time() - first_time)
    print("Total generations:", generation)
    print("Average FPS:", generation / (time.time() - first_time))
    print("Best fitness:", chroms[0].fitness)
    # Cleanup and plot fitness
    cv2.destroyAllWindows()
    plt.plot(fitnessi)
    plt.xlabel('Generation')
    plt.ylabel('Fitness')
    plt.title('Fitness over Generations')
    plt.show()
    
main()