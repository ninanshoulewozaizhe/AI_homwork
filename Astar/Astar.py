import numpy as np

def findtheResult(array, mode):
    # create open&close list
    openList = np.empty([0, 14])
    closeList = np.empty([0, 14])
    openList = np.append(openList, [array], axis=0)
    done = False
    while True:
        if len(openList) == 0:
            print("can not find the result\n")
            break
        else:
            #pop the open list
            target = openList[0]
            result = []
            openList = np.delete(openList, 0, axis=0)
            target[10] = len(closeList)
            closeList = np.append(closeList, [target], axis=0)
            for direction in range(4):
                temp = move(target, direction, mode)
                if temp[0] == 1:
                    temp = temp[1:]
                    print("newnode:")
                    printNode(temp)
                    if temp[12] == 0:
                        result = temp
                        done = True
                    elif not exist(temp, openList, closeList):
                        openList = np.append(openList, [temp], axis=0)
                    if done:
                        break
            # sort according to f
            openList = openList[np.lexsort(openList.T[0,None])]
            printMinfNode(openList)
            print("The sum of the explore nodes: {}".format(len(openList) + len(closeList) + 1))
            if done:
                print("find the result")
                printBestPath(result, closeList)
                break

def printNode(target):
    print("f: {} parent: {}\nnode:".format(target[0], int(target[13])))
    for i in [1, 4, 7]:
        print("{} {} {}".format(int(target[i]), int(target[i + 1]), int(target[i + 2])))
    print("\n")

def printMinfNode(list):
    print("The number of the node in openList: {}\n The min f node:".format(len(list)))
    printNode(list[0])

def printBestPath(result, closeList):
    path = np.empty([0, 14])
    path = np.insert(path, 0, [result], axis=0)
    # printNode(result)
    parent = result[13]
    while parent != -1:
        # for node in closeList:
        #     if node[10] == parent:
        # printNode(node)
        path = np.insert(path, 0, [closeList[int(parent)]], axis=0)
        parent = closeList[int(parent)][13]
        # break
    for node in path:
        printNode(node)
    print("steps: {}".format(len(path)))

def exist(target, openList, closeList):
    targetTmp = target[1:10]
    for i in range(len(openList)):
        nodeTmp = openList[i][1:10]
        if (targetTmp == nodeTmp).all():
            if target[11] < openList[i][11]:
                openList[i] = target
            return True
    for i in range(len(closeList)):
        nodeTmp = closeList[i][1:10]
        if (targetTmp == nodeTmp).all():
            if target[11] < closeList[i][11]:
                closeList[i][11] = target[11]
                closeList[i][13] = target[13]
                calculateFagain(openList, closeList, closeList[i][10] + 1)
            return True
    return False

def calculateFagain(openList, closeList, Cindex):
    for i in range(len(openList)):
        parent = openList[i][13]
        floor = 1
        while parent != -1:
            parent = closeList[parent][13]
            floor += 1
        openList[i][11] = floor
        openList[i][0] = floor + openList[i][12]
    while Cindex < len(closeList):
        parent = closeList[Cindex][13]
        floor = 1
        while parent != -1:
            parent = closeList[parent][13]
            floor += 1
        closeList[Cindex][11] = floor
        closeList[Cindex][0] = floor + closeList[Cindex][12]
        Cindex += 1

def move(target, direction, mode):
    # global nextNum
    zeroPos = np.argwhere(target == 0).flatten()[0]
    newNode = target.copy()
    
    # move
    # up
    if direction == 0 and zeroPos > 3:
        newNode[zeroPos], newNode[zeroPos - 3] = newNode[zeroPos - 3], newNode[zeroPos]
    # right
    elif direction == 1 and zeroPos % 3 != 0:
        newNode[zeroPos], newNode[zeroPos + 1] = newNode[zeroPos + 1], newNode[zeroPos]
    # down
    elif direction == 2 and zeroPos < 7:
        newNode[zeroPos], newNode[zeroPos + 3] = newNode[zeroPos + 3], newNode[zeroPos]
    # left
    elif direction == 3 and zeroPos % 3 != 1:
        newNode[zeroPos], newNode[zeroPos - 1] = newNode[zeroPos - 1], newNode[zeroPos]
    else:
        return [0]

    # # set num
    # newNode[10] = nextNum
    # nextNum += 1
    if mode == 0:
        # set w 
        newNode[12] = getW(newNode)
    elif mode == 1:
        # set os
        newNode[12] = getOsDistance(newNode[1:10])
    elif mode == 2:
        newNode[12] = getHmDistance(newNode[1:10])
    # set floor
    newNode[11] += 1
    # set f
    newNode[0] = newNode[11] + newNode[12]
    # set parent
    newNode[13] = target[10]
    #set newNode flag
    newNode = np.insert(newNode, 0, 1)
    return newNode

def getW(array):
    global Sg
    result = Sg[1:10]
    current = array[1:10]
    return 9 - np.sum(result == current)

def getOsDistance(array):
    Numdict = np.array([[1,1],[0,0],[0,1],[0,2],[1,2],[2,2],[2,1],[2,0],[1,0]])
    temp = array.reshape([3,3])
    distance = 0
    for row in range(3):
        for col in range(3):
            distance += np.sqrt(np.square(Numdict[int(temp[row][col])][0] - row) + np.square(Numdict[int(temp[row][col])][1] - col))
    return distance

def getHmDistance(array):
    Numdict = np.array([[1,1],[0,0],[0,1],[0,2],[1,2],[2,2],[2,1],[2,0],[1,0]])
    temp = array.reshape([3,3])
    distance = 0
    for row in range(3):
        for col in range(3):
            distance += np.abs(Numdict[int(temp[row][col])][0] - row) + np.abs(Numdict[int(temp[row][col])][1] - col)
    return distance

def Available(array):
    des = 1
    count = 0
    while des < 9:
        if array[des] != 0:
            for i in range(des):
                if array[i] > array[des]:
                    count += 1
        des += 1
    return count % 2 == 1

# f, {eight nums}, 10:num, 11:floor, 12: w, 13:parent
Sg = np.array([1, 1, 2, 3, 8, 0, 4, 7, 6, 5, 0, 1, 0, -1])

mode = input("please use 0 or 1 or 2 to choose your function\n")
arr = raw_input("please input your eight num array\n")
S0 = np.array([int(n) for n in arr.split()])
if not Available(S0):
    print("it can not find the result")
else:
    # initial
    S0 = np.append(np.insert(S0, 0, 1), [0, 1, 0, -1])
    nextNum = 2
    S0[12] = getW(S0)
    if S0[12] == 0:
        print("it is the result already")
    else:
        # findtheResult(S0)
        S0[0] += S0[12]
        findtheResult(S0, mode)