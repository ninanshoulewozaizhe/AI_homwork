import numpy as np
from constant import const

class city:

  def __init__(self, num, x, y):
    self.num = num
    self.x = x
    self.y = y

class GA_TSP:

    def __init__(self, filepath, pCross, pMutate, cycleTimes):
        self.population = np.empty([const.POPULATION_SIZE, const.CITY_NUM], np.int32)
        self.fitness = np.empty(const.POPULATION_SIZE)
        self.citiesDistance = np.empty([const.CITY_NUM, const.CITY_NUM])
        self.pathLength = np.empty(const.POPULATION_SIZE)
        self.best = 0
        self.cities = []
        self.pCross = pCross
        self.pMutate = pMutate
        self.start(filepath, cycleTimes)

    def start(self, filepath, times):
        self.initialData(filepath)
        for i in range(times):
            self.evolution()
            self.population = self.newPopulation.copy()
            self.calculate()
            self.printBest(i + 1)
            
    def printBest(self, generation):
        print("generation: {}, the shortest length of the path: {}".format(generation, self.pathLength[self.best]))


    def initialData(self, filepath):
        fr = open('pr136.txt')
        # read data
        for line in fr.readlines():
            lineArr = line.strip().split()
            tempCity = city(int(lineArr[0]) - 1, int(lineArr[1]), int(lineArr[2]))
            self.cities.append(tempCity)
            self.population[:, int(lineArr[0]) - 1: int(lineArr[0])] = int(lineArr[0]) - 1
        # calculate citites distance
        self.calcitiesDistance()
        # get the initial population
        for i in range(const.POPULATION_SIZE):
            for j in range(const.CITY_NUM):
                pos = int(np.random.uniform(0, const.CITY_NUM))
                self.population[i][j], self.population[i][pos] = self.population[i][pos], self.population[i][j]
        self.calculate()

    def calculate(self):
        # get the path length and fitness of every individual
        self.getTheLengthOfTheRoads()
        self.getThefitnessOfTheRoads()

    def calcitiesDistance(self):
        for i in range(const.CITY_NUM):
            j = i + 1
            while j < const.CITY_NUM:
                tempDistance = np.sqrt(np.square(self.cities[i].x - self.cities[j].x) + np.square(self.cities[i].y - self.cities[j].y))
                self.citiesDistance[i][j] = tempDistance
                self.citiesDistance[j][i] = tempDistance
                j += 1

    def getTheLengthOfTheRoads(self):
        for i in range(const.POPULATION_SIZE):
            length = 0
            for j in range(const.CITY_NUM - 1):
                length += self.citiesDistance[self.population[i][j]][self.population[i][j+1]]
            length += self.citiesDistance[self.population[i][0]][self.population[i][const.CITY_NUM - 1]]
            self.pathLength[i] = length
        self.best = np.argmin(self.pathLength)

    def getThefitnessOfTheRoads(self):
        for i in range(const.POPULATION_SIZE):
            self.fitness[i] = 1 / self.pathLength[i]
    
    def evolution(self):
        self.TournamentSelet()
        self.orderCrossover()
        self.mutation()

    # Roulette algorithm
    def RouletteSelect(self):
        # calculate Pi
        sumFitness = np.sum(self.fitness)
        Pi = []
        Pi.append(self.fitness[0] / sumFitness)
        for i in range(const.POPULATION_SIZE - 1):
            Pi.append(self.fitness[i + 1] / sumFitness + Pi[i])
        #select the best one before select by Roulette algorithm
        self.newPopulation = np.empty([const.POPULATION_SIZE, const.CITY_NUM], np.int32)       
        self.newPopulation[0] = self.population[self.best]
        for i in range(const.POPULATION_SIZE - 1):
            rand = np.random.random()
            for j in range(const.POPULATION_SIZE):
                if rand <= Pi[j]:
                    self.newPopulation[i + 1] = self.population[j].copy()
                    break
        # print("select")
        # print(self.newPopulation)
    
    def TournamentSelet(self):
        self.newPopulation = np.empty([const.POPULATION_SIZE, const.CITY_NUM], np.int32)
        for i in range(const.POPULATION_SIZE):
            population1 = int(np.random.uniform(0, const.POPULATION_SIZE))
            population2 = int(np.random.uniform(0, const.POPULATION_SIZE))
            if self.fitness[population1] > self.fitness[population2]:
                self.newPopulation[i] = self.population[population1].copy()
            else:
                self.newPopulation[i] = self.population[population2].copy()


    def orderCrossover(self):
        i = 0
        while i < const.POPULATION_SIZE:
            rand = np.random.random()
            if rand >= self.pCross:
                pos1 = int(np.random.uniform(0, const.CITY_NUM))
                pos2 = int(np.random.uniform(0, const.CITY_NUM))
                if (pos1 > pos2):
                    pos1, pos2 = pos2, pos1
                fragment1 = self.newPopulation[i][pos1 : pos2 + 1]
                fragment2 = self.newPopulation[i + 1][pos1 : pos2 + 1]
                # print(fragment1)
                self.newPopulation[i] = self.newChild(self.newPopulation[i], fragment2, pos1)
                self.newPopulation[i + 1] = self.newChild(self.newPopulation[i + 1], fragment1, pos1)
            i += 2
        # print("crossover")
        # print(self.newPopulation)

    def newChild(self, parent, fragment, pos1):
        # print(parent)
        # print("new child")
        # print(fragment)
        # print(pos1)
        chromosomeLength = 0
        child = np.array([])
        # print("child initial")
        # print(child)
        for gene in parent:
            if chromosomeLength == pos1:
                child = np.append(child, fragment, axis=0)
                chromosomeLength += len(fragment)
                # print(child)
                # print(len(child))
            if gene not in fragment:
                child = np.append(child, [gene], axis=0)
                chromosomeLength += 1
        # if the fragment is the tail
        if chromosomeLength == pos1:
                child = np.append(child, fragment, axis=0)
                chromosomeLength += len(fragment)
        # print(child)
        return child
    
    def mutation(self):
        for i in range(const.POPULATION_SIZE):
            rand = np.random.random()
            if rand >= self.pMutate:
                count = int(np.random.uniform(0, const.CITY_NUM))
                for time in range(count):
                    pos1 = int(np.random.uniform(0, const.CITY_NUM))
                    pos2 = int(np.random.uniform(0, const.CITY_NUM))
                    newPath = self.newPopulation[i].copy()
                    oldPathLength = self.pathLength[i]
                    newPath[pos1], newPath[pos2] = newPath[pos2], newPath[pos1]
                    newPathLength = self.getTheLengthOfTheRoad(newPath)
                    if newPathLength < oldPathLength:
                        self.newPopulation[i][pos1], self.newPopulation[i][pos2] = self.newPopulation[i][pos2], self.newPopulation[i][pos1]
                        self.pathLength[i] = newPathLength
                # for time in range(1000):
                # pos1 = 0
                # pos2 = 0
                # while (pos1 == pos2 or (pos1 == 0 and pos2 == const.CITY_NUM - 1)):
                #     pos1 = int(np.random.uniform(0, const.CITY_NUM))
                #     pos2 = int(np.random.uniform(0, const.CITY_NUM))
                #     if (pos1 > pos2):
                #         pos1, pos2 = pos2, pos1
                # offset = (self.citiesDistance[self.population[i][pos2]][self.population[i][(pos1 - 1 + const.CITY_NUM) % const.CITY_NUM]]
                #         + self.citiesDistance[self.population[i][pos1]][self.population[i][(pos2 + 1) % const.CITY_NUM]]
                #         - self.citiesDistance[self.population[i][pos2]][self.population[i][(pos2 + 1) % const.CITY_NUM]]
                #         - self.citiesDistance[self.population[i][pos1]][self.population[i][(pos1 - 1 + const.CITY_NUM) % const.CITY_NUM]])
                # if (offset < 0):
                #     while (pos1 < pos2):
                #         self.population[i][pos1], self.population[i][pos2] = self.population[i][pos2], self.population[i][pos1]
                #         pos1 += 1
                #         pos2 -= 1
                #     self.pathLength[i] += offset

    def getTheLengthOfTheRoad(self, path):
        length = 0
        for j in range(const.CITY_NUM - 1):
            length += self.citiesDistance[path[j]][path[j+1]]
        length += self.citiesDistance[path[0]][path[const.CITY_NUM - 1]]
        return length

test = GA_TSP("pr136.txt", 0.2, 0.8, 10000)

        
        
        

