import math
import sys

############### FUNCTIONS ###############


#calculate straight line distance from current position to goal
def calcSLD(currX, currY, goalX, goalY):
    return math.sqrt(((currX - goalX) ** 2) + ((currY - goalY) ** 2))


#returns coords of newly explored node
def getNewCoords(currX, currY, direction):
    if direction == 0:
        return currX + 1, currY
    elif direction == 1:
        return currX + 1, currY + 1
    elif direction == 2:
        return currX, currY + 1
    elif direction == 3:
        return currX - 1, currY + 1
    elif direction == 4:
        return currX - 1, currY
    elif direction == 5:
        return currX - 1, currY - 1
    elif direction == 6:
        return currX, currY - 1
    else:
        return currX + 1, currY - 1


#checks if the node is on the grid and isn't a black cell
def validNode(nodes, data, x, y, width, height):
    inBounds = (0 <= x < width) and (0 <= y < height)
    if not inBounds:
        return False

    row = height - y
    col = x
    isWhite = data[row][col] != 1

    return isWhite

#explores a node by generating the child nodes for all 8 directions
def generateNodes(data, nodes, exploredNodes, coords, currNode, goal, width, height):
    ans = {}
    currPathCost = currNode[1]
    currMoves = currNode[3]

    #generate a child node for each direction
    for dir in range(8):
        newX, newY = getNewCoords(coords[0], coords[1], dir)
        stepCost = 1 if dir in [0,2,4,6] else math.sqrt(2)

        #if the new node should be added to the list, calculate all the relevant info
        if validNode(nodes, data, newX, newY, width, height):
            pathCost = currPathCost + stepCost
            sld = calcSLD(newX, newY, goal[0], goal[1])
            cost = pathCost + sld
            moves = currMoves[:]
            moves.append(dir)

            #if the child node hasn't been discovered yet, then add it to the list
            if (newX, newY) not in nodes:
                ans.update({(newX,newY) : [cost, pathCost, sld, moves]})
            #if the child node has been discovered, but offers a shorter path, edit the nodes list
            #and remove it from the list of exploredNodes so that it can be re-explored with its
            #shorter path
            else:
                if nodes[newX, newY][0] > cost:
                    nodes[newX, newY] = [cost, pathCost, sld, moves]
                    if (newX, newY) in exploredNodes:
                        exploredNodes.remove((newX, newY))

    return ans


#choose the node with the lowest cost
def findBestNode(nodes, exploredNodes):
    currBestCost = math.inf
    currBestNode = None

    for coords, info in nodes.items():
        #ignore nodes that have already been explored
        if info[0] < currBestCost and coords not in exploredNodes:
            currBestCost = info[0]
            currBestNode = coords

    return currBestNode


############### SETUP ###############

filename = sys.argv[1]
input = open(filename)
lines = input.readlines()
input.close()

#store the int values in nodes list
data = []
for i in range(len(lines)):
    if lines[i][0] != '\n':
        line = lines[i].strip().split()
        line = [int(val) for val in line]
        data.append(line)


start = data[0][0], data[0][1]   #coords of start node
goal = data[0][2], data[0][3]   #coords of goal node
width = len(data[1])            #width of grid
height = len(data) - 1          #height of grid


initialSLD = calcSLD(start[0], start[1], goal[0], goal[1])

#nodes format is {coordinates : [f(n), g(n), h(n), moves]}
nodes = {start : [initialSLD, 0, initialSLD, []]}
#exploredNodes will contain the coordinates of nodes that have already been explored
exploredNodes = []

curr = start


############### ALGORITHM ###############


while (curr != goal):
    #info about the node
    currNode = nodes.get(curr)

    #expand node and add it to list of generated nodes
    newNodes = generateNodes(data, nodes, exploredNodes, curr, currNode, goal, width, height)
    nodes.update(newNodes)

    #add node to list of explored nodes
    exploredNodes.append(curr)

    #pick the node with the lowest f(n)
    curr = findBestNode(nodes, exploredNodes)



############### BUG TESTING ###############

# for key, value in nodes.items():
#     print(key)
#     print(value)
#     print('\n')


############### WRITE OUTPUT FILE ###############

#at this point, curr is equal to the goal node and contains info about the solution
moves = nodes.get(curr)[3]
depth = len(moves)
numNodes = len(nodes)
grid = data[1:]

#trace the path to record all the relevant f(n) values
#modify the grid to reflect the path
costs = [round(initialSLD,3)]
temp = start
for i in range(depth):
    #move to the next location in the moves list
    temp = getNewCoords(temp[0], temp[1], moves[i])
    #add the f(n) value of each node to the cost list
    costs.append(round(nodes.get(temp)[0], 3))
    #replace 0s with 4s as we move along the path
    if grid[height - temp[1] - 1][temp[0]] != 5:
        grid[height - temp[1] - 1][temp[0]] = 4



output = open('output.txt', 'w')
#write depth and number of nodes generated
output.write(str(depth) + '\n' + str(numNodes) + '\n')
#write moves
for i in range(depth):
    output.write(str(moves[i]))
    output.write(' ') if (i < depth - 1) else output.write('\n')
#write f(n) values
for i in range(len(costs)):
    output.write(str(costs[i]))
    output.write(' ') if (i < len(costs) - 1) else output.write('\n')
#write grid values
for i in range(len(grid)):
    for j in range(len(grid[i])):
        output.write(str(grid[i][j]) + ' ')
    output.write('\n')

output.close()
