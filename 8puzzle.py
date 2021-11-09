import time
import copy
import sys

GOAL = [['1', '2', '3'], ['4', '5', '6'], ['7', '8', '0']]


def main():
    global puzzle
    print('======= 8 Puzzle Solver =======')

    # User can choose to use a default puzzle or create their own
    prompt = input('Type “1” to use a default puzzle, \nType “2” to create your own puzzle.\n')
    choice = int(prompt)

    # here's a default puzzle
    if choice == 1:
        # puzzle = (['1', '2', '3'], ['4', '5', '6'], ['7', '8', '0'])  # depth 0
        # puzzle = (['1', '2', '3'], ['4', '5', '6'], ['0', '7', '8'])  # depth 2
        # puzzle = (['1', '2', '3'], ['5', '0', '6'], ['4', '7', '8'])  # depth 4
        # puzzle = (['1', '3', '6'], ['5', '0', '2'], ['4', '7', '8'])  # depth 8
        # puzzle = (['1', '3', '6'], ['5', '0', '7'], ['4', '8', '2'])  # depth 12
        # puzzle = (['1', '6', '7'], ['5', '0', '3'], ['4', '8', '2'])  # depth 16
        # puzzle = (['7', '1', '2'], ['4', '8', '5'], ['6', '3', '0'])  # depth 20
        puzzle = (['0', '7', '2'], ['4', '6', '1'], ['3', '5', '8'])  # depth 24
    # user create puzzle
    elif choice == 2:
        print('Rule1: put spaces between numbers (0-8).\n')
        print('Rule2: use 0 to represent blank tile.\n')
        print('Create your own puzzle now: \n')

        # first row
        row1 = input('First row: ')
        # second row
        row2 = input('Second row: ')
        # third row
        row3 = input('Third row: ')

        # split all 3 rows by spaces
        row1 = row1.split(' ')
        row2 = row2.split(' ')
        row3 = row3.split(' ')

        # put all numbers in puzzle
        puzzle = row1, row2, row3

        print('\n')
    # User can choose to use between these 3 algos
    algoChoice = input('\nChoose your algorithm: '
                       '\n1. Uniform Cost Search '
                       '\n2. A* with the Misplaced Tile heuristic. '
                       '\n3. A* with the Manhattan distance heuristic\n')
    algo = int(algoChoice)

    # run the driver function general search
    print(generalSearch(puzzle, algo))


# return number of misplaced tiles
def misplacedTiles(puzzle):
    misplaceCount = 0
    # loop through each tile of the puzzle
    for i in range(len(puzzle)):
        for j in range(len(puzzle)):
            # if current tile is different from goal then it's misplaced
            # make sure that we dont count zero as misplaced
            if puzzle[i][j] != GOAL[i][j] and puzzle[i][j] != '0':
                misplaceCount += 1

    return misplaceCount


# return the distance needed for all tiles move back to the right spot
def manhattanDistance(puzzle):
    # r, c are row and column number of a tile for goal state puzzle
    # row col are row and column number of a tile for current puzzle
    global r, row, c, col
    distance = 0

    # 3 for loops
    # 1st loops through numbers 1-8
    # 2nd & 3rd loop through the 3x3 puzzle
    # to compare how much distances difference between puzzle and GOAL
    for k in range(1, 9):
        for i in range(len(puzzle)):
            for j in range(len(puzzle)):
                if puzzle[i][j] == str(k) and puzzle[i][j] != 0:
                    row = i
                    col = j
                if GOAL[i][j] == str(k) and GOAL[i][j] != 0:
                    r = i
                    c = j
        # sum the row and col difference to get the distance
        distance += abs(r - row) + abs(c - col)

    return distance


# return new puzzle that zero has been moved up
def moveUp(p, row, col):
    newPuzzle = copy.deepcopy(p)

    temp = newPuzzle[row][col]
    newPuzzle[row][col] = newPuzzle[row - 1][col]  # moving up
    newPuzzle[row - 1][col] = temp  # swapping

    return newPuzzle


# return new puzzle that zero has been moved down
def moveDown(p, row, col):
    newPuzzle = copy.deepcopy(p)

    temp = newPuzzle[row][col]
    newPuzzle[row][col] = newPuzzle[row + 1][col]  # moving up
    newPuzzle[row + 1][col] = temp  # swapping

    return newPuzzle


# return new puzzle that zero has been moved left
def moveLeft(p, row, col):
    newPuzzle = copy.deepcopy(p)

    temp = newPuzzle[row][col]
    newPuzzle[row][col] = newPuzzle[row][col - 1]  # moving up
    newPuzzle[row][col - 1] = temp  # swapping

    return newPuzzle


# return new puzzle that zero has been moved right
def moveRight(p, row, col):
    newPuzzle = copy.deepcopy(p)

    temp = newPuzzle[row][col]
    newPuzzle[row][col] = newPuzzle[row][col + 1]  # moving up
    newPuzzle[row][col + 1] = temp  # swapping

    return newPuzzle


# return node that is expanded to all possible
def generateChildren(currentNode, visited):
    # list to store child nodes
    childrenNode = []
    global row, col
    # find current location of zero
    for i in range(len(currentNode.problem)):
        for j in range(len(currentNode.problem)):
            if int(currentNode.problem[i][j]) == 0:
                row = i
                col = j
    # decide where can we move zero to
    # row not 0, can go up
    if row != 0:
        newPuzzle = moveUp(currentNode.problem, row, col)
        # check if we've visited this puzzle before
        if newPuzzle not in visited:
            childrenNode.append(newPuzzle)

    # row not 2, can go down
    if row != (len(currentNode.problem) - 1):
        newPuzzle = moveDown(currentNode.problem, row, col)
        # check if we've visited this puzzle before
        if newPuzzle not in visited:
            childrenNode.append(newPuzzle)

    # col not 0, can go left
    if col != 0:
        newPuzzle = moveLeft(currentNode.problem, row, col)
        # check if we've visited this puzzle before
        if newPuzzle not in visited:
            childrenNode.append(newPuzzle)

    # col not 2, can go right
    if col != (len(currentNode.problem) - 1):
        newPuzzle = moveRight(currentNode.problem, row, col)
        # check if we've visited this puzzle before
        if newPuzzle not in visited:
            childrenNode.append(newPuzzle)

    return childrenNode


# return true if the input puzzle is the same as goal state
def checkGoal(puzzle):
    gp = (['1', '2', '3'], ['4', '5', '6'], ['7', '8', '0'])

    if puzzle == gp:
        return True
    return False


# This function is from the psuedo-code in slides provided by Prof. Keogh
def generalSearch(problem, queueingFunction):
    # record the time when generalSearch starts running
    tstart = time.time()
    # set the function only to run 1500 seconds
    t = 1500

    nodesExpnd = 0  # store number of expanded nodes
    maxQSize = 0  # keep track of the maximum queue size
    q = []  # queue
    visited = []  # store puzzle we've already visited

    # make the start node with our puzzle
    n = Node(problem)

    # put start node into queue
    q.append(n)
    maxQSize += 1
    # put this puzzle into visited list
    visited.append(n.problem)

    # loop until problem solved
    while True:
        # if queue is empty, failure
        if len(q) == 0:
            return 'Failure! !'

        # set the current node equal to head of queue
        # currentnode = Node(q[0].problem)
        # currentnode.heuristic = q[0].heuristic
        # currentnode.depth = q[0].depth

        # pop head of queue
        currentnode = q.pop(0)
        # nodesExpnd += 1

        # print which node is the best to expand
        print("Expanding note with g(n) = ", currentnode.depth,
              ", h(n) = ", currentnode.heuristic, ": \n")
        currentnode.printPuzzle()

        # sort our queue by lowest h(n) + g(n)
        # reference: https://thepythonguru.com/python-builtin-functions/sorted/
        q = sorted(q, key=lambda j: j.cost)

        # check to see if current node is same as our goal state
        if checkGoal(currentnode.problem):
            # print all data
            print("Puzzle solved!!!\n\n" + "Expanded a total of " + str(nodesExpnd) + " nodes.\n" +
                  "Maximum number of nodes in the queue was " + str(maxQSize) +
                  ".\nThe solution depth was ", str(currentnode.depth))
            return 0

        # expand all possible child nodes of the current node
        expndChildren = generateChildren(currentnode, visited)

        for i in expndChildren:
            # increment number of expended nodes
            nodesExpnd += 1

            # set every child node as a temp node
            tmp = Node(i)

            # increment depth
            tmp.depth = currentnode.depth + 1

            # set heuristic based on algoChoice
            if queueingFunction == 1:
                tmp.heuristic = 0
            if queueingFunction == 2:
                tmp.heuristic = misplacedTiles(tmp.problem)
            if queueingFunction == 3:
                tmp.heuristic = manhattanDistance(tmp.problem)

            # sum depth and heuristic for cost
            tmp.cost = tmp.depth + tmp.heuristic
            # put temp node into queue
            q.append(tmp)
            # put temp node puzzle into visited list
            visited.append(tmp.problem)

            # update max queue size
            if len(q) > maxQSize:
                maxQSize = len(q)

            # Exit the system if exceeded runtime
            if time.time() > tstart + t:
                print('Exceeded runtime..')
                sys.exit()


# Node class to store each expanded node
# problem store the 2D puzzle
# heuristic stores h(n)
# depth stores g(n)
# cost stores h(n)+g(n)
class Node:
    def __init__(self, p):
        self.problem = p
        self.heuristic = 0
        self.depth = 0
        self.cost = 0
        # self.count = 0
        # self.children = []

    def printPuzzle(self):
        print(self.problem[0][0], self.problem[0][1], self.problem[0][2])
        print(self.problem[1][0], self.problem[1][1], self.problem[1][2])
        print(self.problem[2][0], self.problem[2][1], self.problem[2][2])


if __name__ == "__main__":
    main()
