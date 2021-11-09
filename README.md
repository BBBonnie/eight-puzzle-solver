# eight-puzzle-solver
Comparison of Algorithms: 
The three algorithms this project implemented are as follows: Uniform Cost Search, A* Misplaced Tile heuristic and A* Manhattan Distance heuristic. We use h(n) to represent the heuristic cost and g(n) to represent the depth, where we assume h(n) for Uniform Cost Search is zero.

Uniform Cost Search: 
Uniform Cost Search takes the lowest cost route everytime by expanding the cheapest node. For this project, we simply set the h(n) to zero and only use depth g(n) as cost. This searching method will lead to a large time complexity with puzzles with large depth since we are expanding every level of nodes. In this case, Breadth-First is equivalent to Uniform Cost Search. 

A* Misplaced Tile 
The A* Misplaced Tile heuristic counts the number of misplaced tiles (how many tiles are not in their spot compared with goal state, not including tile zero) and set the number as the heuristic. 
As it shows on the above figure, comparing the current state with goal state, only tile 8 is misplaced to the right. So in this case, our h(n) = 1. When writing the code for this function, I compared each tile in the current state with the corresponding tile in the goal state. If they are the same, go to the next tile, otherwise, increment heuristic by 1. This was easier to implement than the A* Manhattan Distance heuristic, since we only need to simply count the number of misplaced tiles. We also keep track of the g(n) depth. Assume a puzzle has 2 misplaced tiles and takes 3 levels of expansion to reach the goal state, then our total cost is 3+2=5.

A* Manhattan Distance
A* Manhattan Distance counts the amount of distance for every tile to move to their spots in the goal state (not including tile zero). This is similar to the A* Misplaced Tile heuristic, but more considerable for a larger future expansion. 
As it shows on the above figure, comparing the current state with goal state, tile 3, 8, 1 are misplaced. In order to put 3 in its right spot, we need to move it 2 steps to the right. In order to put 8 in its right spot, we need to move it 1 step to the left and 2 steps down, a total of 3 steps. In order to put 1 in its right spot, we need to move it 1 step to the left and 2 steps up, a total of 3 steps. So in this case, our h(n) = 3+3+2=8. For the code implementation, I looped through the puzzle and compared each tile with the goal state, and added the absolute values of row difference and column difference to get the total distance between current tile spot and goal tile spot. This was a little more complex than implementing A* Misplaced Tile, since we not only need to find the misplaced tiles, but also need to calculate the distance.

