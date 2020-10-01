import sys
import pdqpq
import puzz
import solver

puzzle1 = puzz.EightPuzzleBoard("012345678")
node1 = solver.Node(puzzle1,None,None,None)
puzzle2 = puzz.EightPuzzleBoard("012345678")
node2 = solver.Node(puzzle1,None,None,None)

f = pdqpq.PriorityQueue()
f.add(node1,0)
f.add(node2,1)
print(type(node1))
print(node1)
print(node2)
print(type(puzzle1))
print(puzzle1)
print(puzzle2)
print(f.__len__())