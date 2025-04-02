import cv2
import chromosome
import resources
import cProfile  # Import the profiler
import pstats    # For formatting profiler output
import copy
import matplotlib.pyplot as plt
import time


def main():    
    population = chromosome.Population(resources.Resources("resources/mona.png"), size=100)
    generation = 0
    fitnessi = []
    last_time = time.time()
    while True:
        population.step()
        generation += 1
        
        # Display the best chromosome
        chroms = population.population[:6].copy()
        images = cv2.hconcat([chrom.image for chrom in chroms])
        cv2.imshow("Population", images)
        preview = cv2.resize(chroms[0].display(), (512, 256), interpolation=cv2.INTER_NEAREST)
        cv2.imshow("Best Chromosome", preview)
        print("Best Fitness:", chroms[0].fitness, f"[{generation}]", "FPS", 1/(time.time() - last_time))
        last_time = time.time()
        fitnessi.append(chroms[0].fitness)
        
        # Check for exit key
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
        
        if cv2.waitKey(1) & 0xFF == ord('s'):
            # Save the best chromosome image
            cv2.imwrite(f"output/best_{generation}-{chroms[0].fitness}.png", chroms[0].image)
            print(f"Saved best chromosome image as resources/best_{generation}.png")
    #plot fitness(fitnessi)
    cv2.destroyAllWindows()
    plt.plot(fitnessi)
    plt.xlabel('Generation')
    plt.ylabel('Fitness')
    plt.title('Fitness over Generations')
    plt.show()
    

if __name__ == "__main__":
    # Run the profiler
    with cProfile.Profile() as profiler:
        main()
    
    # Print profiler stats
    stats = pstats.Stats(profiler)
    stats.sort_stats(pstats.SortKey.CUMULATIVE)  # Sort by time
    stats.print_stats(10)  # Print the top 10 results