"""
------------------------------------------------------------------------------------------------------------------------

TRUCK AND PACKAGES PROBLEM
Submitted by :  NIVEDHA RAMESH (40128111)
                JAGADEESHWARAN RAJA UMASHANKAR (40126184)


-----------------------------------------------------------------------------------------------------------------------
"""

from datetime import date
import json
import visualize_plotly as vis
import visualize as vis2
import population as gen
import fitnesscalc as ft
import recombination as re
import mutation as mt
import nsga2 as ns
import survivor_selection as ss
import matplotlib.pyplot as plt
from tabulate import tabulate
from copy import deepcopy
import matplotlib.tri as mtri

# import Dataset as ds
# import interface.Add as Add

NUM_OF_ITERATIONS = 3
NUM_OF_INDIVIDUALS = 40
NUM_OF_GENERATIONS = 100
PC = int(0.8 * NUM_OF_INDIVIDUALS)
PM1 = 0.2
PM2 = 0.02
K = 2
ROTATIONS = 2

# 1 or 2 or 6

ColorPair = {}


def plot_stats(average_fitness, title=""):
    x1 = range(len(average_fitness))
    avg_freespace = []
    avg_number = []
    avg_value = []

    for item in average_fitness:
        avg_freespace.append(item[0])
        avg_number.append(item[1])
        avg_value.append(item[2])

    plt.plot(x1, avg_freespace, label='Average Occupied Volume')
    plt.plot(x1, avg_number, label='Average Number of Boxes')
    plt.plot(x1, avg_value, label='Average Value of Boxes')
    plt.xlabel('Number of Generations')
    plt.ylabel('Fitness Values')
    plt.xticks(ticks=[t for t in x1 if t % 20 == 0])
    plt.title(title)
    plt.legend()
    plt.show()


def calc_average_fitness(individuals):
    fitness_sum = [0.0, 0.0, 0.0]
    count = 0
    for key, value in individuals.items():
        if value['Rank'] == 1:
            count += 1
            fitness_sum[0] += value['fitness'][0]
            fitness_sum[1] += value['fitness'][1]
            fitness_sum[2] += value['fitness'][2]
    average = [number / count for number in fitness_sum]
    return average


def draw_pareto(population):
    fitness = []
    number = []
    weight = []
    fitness2 = []
    number2 = []
    weight2 = []
    fig = plt.figure()
    ax = fig.add_subplot(111, projection='3d')
    colors = []

    for key, value in population.items():
        if value['Rank'] == 1:
            fitness.append(value['fitness'][0])
            number.append(value['fitness'][1])
            weight.append(value['fitness'][2])
            colors.append('red')
        else:
            colors.append('blue')
            fitness2.append(value['fitness'][0])
            number2.append(value['fitness'][1])
            weight2.append(value['fitness'][2])

    if len(fitness) > 2:
        try:
            ax.scatter(fitness2, number2, weight2, c='b', marker='o')
            ax.scatter(fitness, number, weight, c='r', marker='o')
            triang = mtri.Triangulation(fitness, number)
            ax.plot_trisurf(triang, weight, color='red')
            ax.set_xlabel('occupied space')
            ax.set_ylabel('no of boxes')
            ax.set_zlabel('value')
            plt.show()
        except:
            print(
                "ERROR : Please try increasing the number of individuals as the unique Rank 1 solutions is less than 3")


def start():
    with open('input.json', 'r') as outfile:
        data = json.load(outfile)

    # data = ds.Packing_Prepare()
    # date = Add.RunPacking
    problem_indices = list(data.keys())

    for p_ind in problem_indices:

        print("Running Problem Set {}".format(p_ind))
        print(tabulate([['Generations', NUM_OF_GENERATIONS], ['Individuals', NUM_OF_INDIVIDUALS],
                        ['Rotations', ROTATIONS], ['Crossover Prob.', PC], ['Mutation Prob1', PM1],
                        ['Mutation Prob2', PM2], ['Tournament Size', K]], headers=['Parameter', 'Value'],
                       tablefmt="github"))
        print()

        # Extracting inputs from the json file
        truck_dimension = data[p_ind]['truck dimension']
        packages = data[p_ind]['solution']
        print(len(packages))
        boxes = data[p_ind]['boxes']
        print(len(boxes))
        total_value = data[p_ind]['total value']
        box_count = data[p_ind]['number']
        box_params = {}
        for index in range(len(boxes)):
            box_params[index] = boxes[index]

        # Storing the average values over every single iteration
        average_vol = []
        average_num = []
        average_value = []

        for i in range(NUM_OF_ITERATIONS):
            # Generate the initial population
            population = gen.generate_pop(box_params, NUM_OF_INDIVIDUALS, ROTATIONS)

            # print(i)
            Gen = 0
            average_fitness = []
            while Gen < NUM_OF_GENERATIONS:
                population, fitness = ft.evaluate(population, truck_dimension, box_params, total_value)
                population = ns.rank(population, fitness)
                offsprings = re.crossover(deepcopy(population), PC, k=K)
                offsprings = mt.mutate(offsprings, PM1, PM2, ROTATIONS)
                population = ss.select(population, offsprings, truck_dimension, box_params, total_value,
                                       NUM_OF_INDIVIDUALS)
                average_fitness.append(calc_average_fitness(population))
                Gen += 1
            results = []

            # for value in population.items():
            #     print(value)

            # exit(0)
            # Storing the final Rank 1 solutions
            Vol = 0
            MostNum = 0

            ProbResult = []

            for key, value in population.items():
                if value['Rank'] == 1:
                    # print(value['fitness'][0])
                    # print(value['fitness'][1])
                    if value['fitness'][1] >= Vol:
                        ProbResult = deepcopy(value['result'])

                        # print (Vol)
                        Vol = value['fitness'][0]
                        MostNum = value['fitness'][1]

                    # results.append(value['result'])
            # results = deepcopy(ProbResult)
            results.append(ProbResult)

            # print(len(results))
            # for pieces in results:
            #     print("pieces:",pieces)
            #     for each in pieces:
            #         print("each:",each)
            #         # print(type(each))
            # exit(0)
            # Plot using plotly
            # print(len(packages))

            # # color_index, ColorPair = vis.draw_solution(pieces=packages)
            # print(len(color_index[0]), len(color_index[1]))
            # print(ColorPair)
            #
            # # print(color_index)
            # print(len(results[0]))
            # exit(0)

            # vis.draw(results, color_index, ColorPair)
            #
            # Plot using matplotlib
            color_index,ColorPair = vis2.draw(pieces=packages, title="True Solution Packing")
            for each in results:
                vis2.draw(each, color_index, title="Figure {} ".format(ColorPair))
            # draw_pareto(population)
            average_vol.append(average_fitness[-1][0])
            average_num.append(average_fitness[-1][1])
            average_value.append(average_fitness[-1][2])
            # plot_stats(average_fitness,
            #            title="Average Fitness Values for Run {} over {} generations".format(i + 1,
            #                                                                                 NUM_OF_GENERATIONS))
            print(average_fitness[-1][0])

        print(tabulate(
            [['Problem Set', p_ind], ['Runs', NUM_OF_ITERATIONS], ['Avg. Volume%', sum(average_vol) / len(average_vol)],
             ['Avg. Number%', sum(average_num) / len(average_num)],
             ['Avg. Value%', sum(average_value) / len(average_value)]],
            headers=['Parameter', 'Value'], tablefmt="github"))


if __name__ == "__main__":
    start()
