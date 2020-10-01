import sys
import puzz
import pdqpq
import random

class Node:
    def __init__(self, val, move, parent, pathCost = 0):
        self.val = val
        self.move = move
        self.parent = parent
        self.pathCost = pathCost

    def __hash__(self):
        return hash("".join(self.val._board))

    def __eq__(self, other):
        return "".join(self.val._board) == "".join(other.val._board)


class LinkedList:
    def __init__(self):
        self.root = None

    def print(self):
        print("printing")
        node = self.root
        print(node.val)
        print(node.move)
        for i in node.nextNode:
            node = i


def generate(puzz, count, arr):
    if count > 0:
        dict = puzz.successors()
        puzz = random.choice(list(dict.values()))
        if puzz in arr:
            puzz = random.choice(list(dict.value()))
        count = count - 1
        generate(puzz, count, arr)
    return puzz


def expand(node):
    succ = node.successors()
    arr = []
    for i in succ:
        arr.append(succ[i])
    return succ


def complete(state):
    if state == puzz.EightPuzzleBoard('012345678'):
        return True
    else:
        return False


def movedTile(curr, child):
    childCoord = child.val.find('0')
    childX = childCoord[0]
    childY = childCoord[1]
    tile = int(curr.val._get_tile(childX, childY))
    return tile


def h(node, flag):
    heuristic = 0
    goal = puzz.EightPuzzleBoard('012345678')
    puz = puzz.EightPuzzleBoard(str(node.val))

    for i in range(1, 9):
        goalCoord = goal.find(str(i))
        goalX = goalCoord[0]
        goalY = goalCoord[1]

        childCoord = puz.find(str(i))
        childX = childCoord[0]
        childY = childCoord[1]

        mX = abs(goalX - childX)
        mY = abs(goalY - childY)
        m = mX + mY
        if flag is None:
            heuristic = heuristic + m * pow(i, 2)
        else:
            heuristic = heuristic + m

    return heuristic


def moveCost(tile):
    return pow(tile, 2)


def currPathCost(node):
    path = 0
    curr = node
    while curr is not None:
        path = path
        node = curr.parent


def metrics(node, solutionNode, moveCount, cost, fCount, expanded):
    solution = []
    while node.parent is not None:
        solution.append(str(node.parent.move) + " " + str(node.parent.val))
        node = node.parent
    solution.reverse()
    for j in range(len(solution)):
        print(moveCount, solution[j])
        moveCount = moveCount + 1

    print(moveCount, str(solutionNode.move), str(solutionNode.val))
    print("Cost:", cost)
    print("Nodes in Frontier:", fCount)
    print("Nodes Expanded:", expanded)


def bfs(start, flag):
    expanded = 0
    cost = 0
    moveCount = 0

    llist = LinkedList()
    b = puzz.EightPuzzleBoard(start)
    f = pdqpq.PriorityQueue()

    root = Node(b, "start", None)
    f.add(root)
    fCount = 1
    explored = []

    if complete(root.val):
        cost = 0
        print("start", root.val)
        print("Cost:", cost)
        print("Nodes in Frontier:", fCount)
        print("Nodes Expanded:", expanded)
        return 1

    while not f.empty() and expanded < 100000:
        currNode = f.pop()

        while currNode is None:
            currNode = f.pop()

        dic = expand(currNode.val)
        expanded = expanded + 1
        explored.append(currNode)

        if llist.root is None:
            llist.root = currNode

        for i in dic:
            child = dic[i]
            move = i
            childNode = Node(child, move, currNode)

            # compare currNode.val to childNode.val and determine which tile is swapped
            if childNode not in f and childNode not in explored:
                if complete(childNode.val):
                    NodeChild = childNode
                    while NodeChild.parent is not None:
                        tile = movedTile(NodeChild, NodeChild.parent)
                        if flag == "--noweight":
                            tile = 1
                        cost = cost + pow(tile, 2)
                        NodeChild = NodeChild.parent
                    node = childNode
                    metrics(node, childNode, moveCount, cost,  fCount, expanded)

                    return 1
                f.add(childNode)
                fCount = fCount + 1
    print("100,000 nodes expanded, please try another start state.")
    print("Nodes in Frontier:", fCount)
    print("Nodes Expanded:", expanded)
    return -1


def ucost(start, flag):
    expanded = 0
    cost = 0
    moveCount = 0
    explored = []

    llist = LinkedList()
    b = puzz.EightPuzzleBoard(start)
    f = pdqpq.PriorityQueue()

    root = Node(b, "start", None)
    f.add(root, 0)
    fCount = 1

    if complete(root.val):
        cost = 0
        print("start", root.val)
        print("Cost:", cost)
        print("Nodes in Frontier:", fCount)
        print("Nodes Expanded:", expanded)
        return 1

    while not f.empty() and expanded < 100000:
        currNode = f.pop()

        if complete(currNode.val):
            NodeChild = currNode
            while NodeChild.parent is not None:
                tile = movedTile(NodeChild, NodeChild.parent)
                if flag == "--noweight":
                    tile = 1
                cost = cost + pow(tile, 2)
                NodeChild = NodeChild.parent
            node = currNode
            metrics(node, currNode, moveCount, cost, fCount, expanded)
            return 1

        explored.append(currNode)

        while currNode is None:
            currNode = f.pop()

        dic = expand(currNode.val)
        expanded = expanded + 1
        print(expanded)

        if llist.root is None:
            llist.root = currNode

        for i in dic:
            path = 0
            child = dic[i]
            move = i
            childNode = Node(child, move, currNode)
            tile = movedTile(currNode, childNode)
            if flag == "--noweight":
                tile = 1
            c = moveCost(tile)
            childNode.pathCost = c + childNode.parent.pathCost
            # node = childNode
            # while node.parent is not None:
            #     path = moveCost(tile, path) + node.parent.pathCost
            #     node.pathCost = path
            #     node = node.parent
            # childNode.pathCost = path

            # have to add in explored so that repeat states arent counted
            if not f.__contains__(childNode) and childNode not in explored:
                f.add(childNode, childNode.pathCost)
                fCount = fCount + 1
            elif f.__contains__(childNode):
                if f.get(childNode) > childNode.pathCost:
                    f.add(childNode, childNode.pathCost)
    print("100,000 nodes expanded, please try another start state.")
    print("Nodes in Frontier:", fCount)
    print("Nodes Expanded:", expanded)
    return -1


def greedy(start, flag):
    expanded = 0
    cost = 0
    moveCount = 0
    explored = []
    solution = []

    llist = LinkedList()
    b = puzz.EightPuzzleBoard(start)
    f = pdqpq.PriorityQueue()

    root = Node(b, "start", None)
    f.add(root)
    fCount = 1

    if complete(root.val):
        cost = 0
        print("start", root.val)
        print("Cost:", cost)
        print("Nodes in Frontier:", fCount)
        print("Nodes Expanded:", expanded)
        return 1

    while not f.empty() and expanded < 100000:
        currNode = f.pop()
        solution.append(currNode)
        # print(currNode)
        explored.append(currNode)

        while currNode is None:
            currNode = f.pop()
        if complete(currNode.val):
            NodeChild = currNode
            while NodeChild.parent is not None:
                tile = movedTile(NodeChild, NodeChild.parent)
                if flag == "--noweight":
                    tile = 1
                cost = cost + pow(tile, 2)
                NodeChild = NodeChild.parent
            NodeChild = childNode
            metrics(NodeChild, childNode, moveCount, cost, fCount, expanded)
            # for i in range(len(solution)):
            #     print(str(i+1), solution[i].move, solution[i].val)
            # print("Cost:", cost)
            # print("Nodes in Frontier:", fCount)
            # print("Nodes Expanded:", expanded)
            return 1
        dic = expand(currNode.val)
        expanded = expanded + 1

        if llist.root is None:
            llist.root = currNode
        childDict = []
        for i in dic:
            child = dic[i]
            move = i
            childNode = Node(child, move, currNode)
            if not f.__contains__(childNode) and childNode not in explored:

                # tile = movedTile(currNode, childNode)
                # cost = cost + moveCost(tile)
                f.add(childNode, h(childNode, flag))
                fCount = fCount + 1
                # print(childNode.val)
            # print(childNode)
            # print(childNode.val, h(childNode))
        #     childDict.append((childNode, h(childNode, flag)))
        #     lowest = h(childNode, flag)
        #     val = childNode
        # # print(childDict[2][0].val, childDict[1])
        #
        # # print(childDict)
        # for i in childDict:
        #     if i[1] < lowest:
        #         val = i[0]
        #         # print(val)
        #         lowest = i[1]
        # tile = movedTile(currNode, val)
        # cost = cost + moveCost(tile)
        # if not f.__contains__(val) and val not in explored:
        #     # print(val.val)
        #     f.add(val)
        #     fCount = fCount + 1
        #     solution.append(val)

    print("100,000 nodes expanded, please try another start state.")
    print("Nodes in Frontier:", fCount)
    print("Nodes Expanded:", expanded)
    return -1


def astar(start, flag):
    expanded = 0
    cost = 0
    moveCount = 0
    explored = []

    llist = LinkedList()
    b = puzz.EightPuzzleBoard(start)
    f = pdqpq.PriorityQueue()

    root = Node(b, "start", None)
    f.add(root, 0)
    fCount = 1

    if complete(root.val):
        cost = 0
        print("start", root.val)
        print("Cost:", cost)
        print("Nodes in Frontier:", fCount)
        print("Nodes Expanded:", expanded)
        return 1

    while not f.empty() and expanded < 100000:
        currNode = f.pop()
        explored.append(currNode)

        while currNode is None:
            currNode = f.pop()

        dic = expand(currNode.val)
        expanded = expanded + 1

        if llist.root is None:
            llist.root = currNode

        for i in dic:
            path = 0
            child = dic[i]
            move = i
            childNode = Node(child, move, currNode)
            tile = movedTile(currNode, childNode)
            if flag == "--noweight":
                tile = 1
            c = moveCost(tile)
            heuristic = h(childNode, flag)
            childNode.pathCost = c + childNode.parent.pathCost
            if not f.__contains__(childNode) and childNode not in explored:
                # print(heuristic)
                f.add(childNode, heuristic + childNode.pathCost)
                fCount = fCount + 1
            elif f.__contains__(childNode):
                if f.get(childNode) > childNode.pathCost + heuristic:
                    f.add(childNode, childNode.pathCost + heuristic)
            if complete(childNode.val):
                NodeChild = childNode
                while NodeChild.parent is not None:
                    tile = movedTile(NodeChild, NodeChild.parent)
                    if flag == "--noweight":
                        tile = 1
                    cost = cost + pow(tile, 2)
                    NodeChild = NodeChild.parent
                node = childNode
                metrics(node, childNode, moveCount, cost, fCount, expanded)

                return 1
    print("100,000 nodes expanded, please try another start state.")
    print("Nodes in Frontier:", fCount)
    print("Nodes Expanded:", expanded)
    return -1


if __name__ == '__main__':
    goal = puzz.EightPuzzleBoard('012345678')
    arr = []
    generate(goal, 9, arr)

    search = sys.argv[1]            # stores algorithm name in easy to read variable
    start = sys.argv[2]             # stores start state in easy to read variable
    if len(sys.argv) < 4:           # checks length of argv array
        flag = None                 # if < 3 we know --noweight flag was NOT entered
    else:
        flag = sys.argv[3]          # else we can pass on the flag

    if flag is not None and flag != "--noweight":
        print("Please try again with a valid flag.")
        quit()

    if search == 'bfs':
        # print(bfs(start, flag))
        bfs(start, flag)
    elif search == 'ucost':
        ucost(start, flag)
    elif search == 'greedy':
        greedy(start, flag)
    elif search == 'astar':
        astar(start, flag)
    else:
        print("Please enter valid search algorithm")
