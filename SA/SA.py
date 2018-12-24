from matplotlib.lines import Line2D
import matplotlib.pyplot as plt
import numpy as np

DATASIZE = 136
# graph_x_min = 1000000
# graph_x_max = 0
# graph_y_min = 1000000
# graph_y_max = 0

class city:

  def __init__(self, num, x, y):
    self.num = num
    self.x = x
    self.y = y

def calcitiesDistance():
  for i in range(DATASIZE):
    j = i
    while j < DATASIZE:
      tempDistance = np.sqrt(np.square(cities[i].x - cities[j].x) + np.square(cities[i].y - cities[j].y))
      citiesDistance[i][j] = tempDistance
      citiesDistance[j][i] = tempDistance
      j += 1

def getTheLengthOfTheRoad():
  length = 0
  for i in range(DATASIZE - 1):
    length += citiesDistance[cities[i].num][cities[i + 1].num]
  length += citiesDistance[cities[0].num][cities[DATASIZE - 1].num]
  return length


def getTheGraph(pathLength, T):
  plt.clf()
  # figure, ax = plt.subplots()
  plt.scatter(coordinates[:, 0], coordinates[:, 1], s=5)
  for i in range(DATASIZE - 1):
    plt.plot([cities[i].x, cities[i + 1].x],[cities[i].y, cities[i + 1].y], "black")
  plt.plot([cities[0].x, cities[DATASIZE - 1].x],[cities[0].y, cities[DATASIZE - 1].y], "black")
  plt.title('T: ' + str(T) + ', cost: ' + str(pathLength))
  plt.draw()
  plt.pause(0.000001)


def initData():
  global pathLength
  # global graph_x_min
  # global graph_x_max
  # global graph_y_min
  # global graph_y_max
  fr = open('pr136.txt')
  lines = fr.readlines()
  for i in range(len(lines)):
    lineArr = lines[i].strip().split()
    tempCity = city(int(lineArr[0]) - 1, int(lineArr[1]), int(lineArr[2]))
    coordinates[i][0] = int(lineArr[1])
    coordinates[i][1] = int(lineArr[2])
    # if int(lineArr[1]) > graph_x_max:
    #   graph_x_max = int(lineArr[1])
    # elif int(lineArr[1]) < graph_x_min:
    #   graph_x_min = int(lineArr[1])
    # if int(lineArr[2]) > graph_y_max:
    #   graph_y_max = int(lineArr[2])
    # elif int(lineArr[2]) < graph_y_min:
    #   graph_y_min = int(lineArr[2])
    cities.append(tempCity)
  fr.close()
  calcitiesDistance()
  for i in range(DATASIZE):
    pos = int(np.random.uniform(0, DATASIZE))
    cities[i], cities[pos] = cities[pos], cities[i]
    pathLength = getTheLengthOfTheRoad()
  print('the length of this path: {}'.format(pathLength))


def SASearch(temperature_limit, temperature, times, raduceRate):
  global pathLength
  getTheGraph(pathLength, temperature)
  recent_pathLengths = [0, 0]
  while temperature > temperature_limit:
    times *= 1.01
    temperature_times = times
    while(temperature_times > 0):
      pos1 = 0
      pos2 = 0
      while (pos1 == pos2 or (pos1 == 0 and pos2 == DATASIZE - 1)):
        pos1 = int(np.random.uniform(0, DATASIZE))
        pos2 = int(np.random.uniform(0, DATASIZE))
        if (pos1 > pos2):
          pos1, pos2 = pos2, pos1
      offset = (citiesDistance[cities[pos2].num][cities[(pos1 - 1 + DATASIZE) % DATASIZE].num] 
        + citiesDistance[cities[pos1].num][cities[(pos2 + 1) % DATASIZE].num] 
        - citiesDistance[cities[pos2].num][cities[(pos2 + 1) % DATASIZE].num] 
        - citiesDistance[cities[pos1].num][cities[(pos1 - 1 + DATASIZE) % DATASIZE].num])
      if offset < 0 or np.exp(-offset / temperature) >= np.random.rand():
        while (pos1 < pos2):
          cities[pos1], cities[pos2] = cities[pos2], cities[pos1]
          pos1 += 1
          pos2 -= 1
        pathLength += offset
      temperature_times -= 1
    # if (pathLength == recent_pathLengths[0] and pathLength == recent_pathLengths[1]):
    #   break
    # getTheGraph()
    print("temperature: {} the length of this path: {}, {}% ".format(temperature, pathLength, (pathLength - 96772) / 96772 * 100))
    getTheGraph(pathLength, temperature)
    recent_pathLengths[0] = recent_pathLengths[1]
    recent_pathLengths[1] = pathLength 
    temperature *= raduceRate
    
def localSearch(times):
  global pathLength
  for time in range(times):
    # pos1 = 0
    # pos2 = 0
    # while (pos1 == pos2 or (pos1 == 0 and pos2 == DATASIZE - 1)):
    #   pos1 = int(np.random.uniform(0, DATASIZE))
    #   pos2 = int(np.random.uniform(0, DATASIZE))
    #   if (pos1 > pos2):
    #     pos1, pos2 = pos2, pos1
    # offset = (citiesDistance[cities[pos2].num][cities[(pos1 - 1 + DATASIZE) % DATASIZE].num]
    #   + citiesDistance[cities[pos1].num][cities[(pos2 + 1) % DATASIZE].num]
    #   - citiesDistance[cities[pos2].num][cities[(pos2 + 1) % DATASIZE].num]
    #   - citiesDistance[cities[pos1].num][cities[(pos1 - 1 + DATASIZE) % DATASIZE].num])
    # if (offset < 0):
    #   while (pos1 < pos2):
    #     cities[pos1], cities[pos2] = cities[pos2], cities[pos1]
    #     pos1 += 1
    #     pos2 -= 1
    #   pathLength += offset
    ReverseRoad()
    TwoPTchange()
    printData()
    # getTheGraph(pathLength, 0)

def ReverseRoad():
  global pathLength
  pos1 = 0
  pos2 = 0
  while (pos1 == pos2 or (pos1 == 0 and pos2 == DATASIZE - 1)):
    pos1 = int(np.random.uniform(0, DATASIZE))
    pos2 = int(np.random.uniform(0, DATASIZE))
    if (pos1 > pos2):
      pos1, pos2 = pos2, pos1
  offset = (citiesDistance[cities[pos2].num][cities[(pos1 - 1 + DATASIZE) % DATASIZE].num]
    + citiesDistance[cities[pos1].num][cities[(pos2 + 1) % DATASIZE].num]
    - citiesDistance[cities[pos2].num][cities[(pos2 + 1) % DATASIZE].num]
    - citiesDistance[cities[pos1].num][cities[(pos1 - 1 + DATASIZE) % DATASIZE].num])
  if (offset < 0):
    while (pos1 < pos2):
      cities[pos1], cities[pos2] = cities[pos2], cities[pos1]
      pos1 += 1
      pos2 -= 1
    pathLength += offset
    # print("cal length:{}".format(getTheLengthOfTheRoad()))
  

def TwoPTchange():
  global pathLength
  pos1 = 0
  pos2 = 0
  offset = 0
  while (pos1 == pos2):
    pos1 = int(np.random.uniform(0, DATASIZE))
    pos2 = int(np.random.uniform(0, DATASIZE))
    if (pos1 > pos2):
      pos1, pos2 = pos2, pos1
  if pos1 + 1 == pos2:
    offset = (citiesDistance[cities[pos2].num][cities[(pos1 - 1 + DATASIZE) % DATASIZE].num]
      + citiesDistance[cities[pos1].num][cities[(pos2 + 1) % DATASIZE].num]
      - citiesDistance[cities[pos2].num][cities[(pos2 + 1) % DATASIZE].num]
      - citiesDistance[cities[pos1].num][cities[(pos1 - 1 + DATASIZE) % DATASIZE].num])
  elif pos1 == 0 and pos2 == DATASIZE - 1:
    offset = (citiesDistance[cities[pos2].num][cities[(pos1 + 1 + DATASIZE) % DATASIZE].num]
      + citiesDistance[cities[pos1].num][cities[(pos2 - 1) % DATASIZE].num]
      - citiesDistance[cities[pos2].num][cities[(pos2 - 1) % DATASIZE].num]
      - citiesDistance[cities[pos1].num][cities[(pos1 + 1 + DATASIZE) % DATASIZE].num])
  else:
    offset = (citiesDistance[cities[pos2].num][cities[(pos1 - 1 + DATASIZE) % DATASIZE].num]
      + citiesDistance[cities[pos2].num][cities[(pos1 + 1) % DATASIZE].num]
      + citiesDistance[cities[pos1].num][cities[(pos2 - 1 + DATASIZE) % DATASIZE].num]
      + citiesDistance[cities[pos1].num][cities[(pos2 + 1) % DATASIZE].num]
      - citiesDistance[cities[pos2].num][cities[(pos2 - 1 + DATASIZE) % DATASIZE].num]
      - citiesDistance[cities[pos2].num][cities[(pos2 + 1) % DATASIZE].num]
      - citiesDistance[cities[pos1].num][cities[(pos1 - 1 + DATASIZE) % DATASIZE].num]
      - citiesDistance[cities[pos1].num][cities[(pos1 + 1) % DATASIZE].num])
  # print("pos1: {}, pos2: {}, offset: {}".format(pos1, pos2, offset))
  if (offset < 0):
    cities[pos1], cities[pos2] = cities[pos2], cities[pos1]
    pathLength += offset
    # print("cal length:{}".format(getTheLengthOfTheRoad()))

def printData():
  print('the length of this path: {}, {}% '.format(pathLength, (pathLength - 96772) / 96772 * 100))

pathLength = 0
citiesDistance = np.zeros([DATASIZE,DATASIZE])
coordinates = np.zeros([DATASIZE,2])
cities = []
initData()
localSearch(2000000)
# SASearch(10, 300, 30000, 0.98)
printData()
