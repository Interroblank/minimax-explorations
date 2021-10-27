import bfs as alg1
import dfs as alg2
import dijkstra as alg3
import gbf as alg4
import astar as alg5

def main():
    puzzles = {
        1 : [1, 3, 4, 8, 6, 2, 7, 0, 5],
        2 : [2, 8, 1, 0, 4, 3, 7, 6, 5],
        3 : [5, 6, 7, 4, 0, 8, 3, 2, 1]
    }
    goal_state = [1, 2, 3, 8, 0, 4, 7, 6, 5]
    user_config = config()
    if user_config[1] == 1:
        print('\nExecuting a breadth-first search . . .')
        alg1.bfs(puzzles[user_config[0]], goal_state)
    if user_config[1] == 2:
        print('\nExecuting a depth-first search . . .')
        alg2.dfs(puzzles[user_config[0]], goal_state)
    if user_config[1] == 3:
        print('\nExecuting a uniform-cost search . . .')
        alg3.dijkstra(puzzles[user_config[0]], goal_state)
    if user_config[1] == 4:
        print('\nExecuting a greedy best-first search . . .')
        alg4.gbf(puzzles[user_config[0]], goal_state)
    if user_config[1] == 5:
        print('\nExecuting an A* search (h1) . . .')
        alg5.astar_h1(puzzles[user_config[0]], goal_state)
    if user_config[1] == 6:
        print('\nExecuting an A* search (h2) . . .')
        alg5.astar_h2(puzzles[user_config[0]], goal_state)

def config():
    print('Puzzle 1 (Easy)')
    print('Puzzle 2 (Medium)')
    print('Puzzle 3 (Hard)')
    diff = int(input('\nSelect a puzzle to solve (1-3): '))
    # TODO - Handle invalid input.
    print('\n1. BFS (Breadth-First Search)')
    print('2. DFS (Depth-First Search)')
    print('3. Uniform-Cost (Dijkstra)')
    print('4. GBF (Greedy Best-First)')
    print('5. A* (Heuristic 1)')
    print('6. A* (Heuristic 2)')
    alg = int(input('\nSelect an algorithm (1-6): '))
    # TODO - Handle invalid input.
    return (diff, alg)
