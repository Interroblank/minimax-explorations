import random as rand
import math
import copy
rand.seed()

class Node:
    def __init__(self, name, weight):
        self.name = name        # Name of node.
        self.weight = weight    # Weight of node (if core node).
        self.adj_list = []      # Adjacency list of node.
        self.cmp_list = []      # Compliments list of node.
        self.claimed = False    # Has the node been claimed?
        self.claimed_by = ''    # Which player claimed the node.

class StateNode:
    def __init__(self, board):
        self.board = board          # The board state itself.
        self.score_A = 0            # Player A's score in this state.
        self.score_B = 0            # Player B's score in this state.
        self.to_move = 'A'          # Current player's turn to move.
        self.children = []          # This children states of this state.
        self.last_move = ('', '')   # The last edge drawn to reach this state.

# Game state variables.
board = []
board_total = 0
player_score_A = 0
player_score_B = 0
current_move = 'A'
versus_computer = False
max_depth = 0

def main():
    global versus_computer
    global max_depth
    print('\nSelect opponent.')
    print('1. Human Opponent')
    print('2. Computer Opponent\n')
    versus = input('')
    build_board()
    if versus == '2':
        versus_computer = True
        print('\nSelect maximum depth.\n')
        max_depth = int(input(''))
        print('\nStarting game . . .')
        turn_cycle_H()
    else:
        print('\nStarting game . . .')
        turn_cycle_H()

def turn_cycle_H():
    # Print the current board state, the score, and the current player.
    print('\n- - - - - - - - - -\n')
    print_board()
    print_score()
    print_current_move()
    # Accept input from the player for their move.
    move1 = input('Draw a line from which node? ')
    move2 = input('Draw a line to which node? ')
    draw_edge(move1, move2)
    # Assign points accordingly, move to a new board state.
    assess_move()
    # Check if the game is over.
    end_game()
    # If not, cycle to the next player's turn.
    next_move()
    if versus_computer == True:
        turn_cycle_C()
    else:
        turn_cycle_H()

def turn_cycle_C():
    # Print the current board state, the score, and the current player.
    print('\n- - - - - - - - - -\n')
    print_board()
    print_score()
    print_current_move()
    # Translate the current board state into a state node.
    state_init = create_init_state()
    # Execute a minimax search on the state node.
    minimax_res = minimax(state_init, max_depth, True)
    # Evaluate each child state of the state node.
    for child in state_init.children:
        if child != None:
            if state_eval(child) == minimax_res:
                # Draw the edge specified by the minimax result.
                draw_edge(child.last_move[0], child.last_move[1])
                break
    # Assign points accordingly.
    assess_move()
    # Check if the game is over.
    end_game()
    # If not, cycle back to the human player's turn.
    next_move()
    turn_cycle_H()

def minimax(curr_state, ply, maxim):
    if ply == 0 or end_game_check(curr_state):
        return state_eval(curr_state)
    if maxim:
        eval_max = -math.inf
        curr_state.children = calc_all_succ_states(copy.deepcopy(curr_state))
        for child in curr_state.children:
            if child != None:
                eval_new = minimax(child, ply - 1, False)
                eval_max = max(eval_max, eval_new)
        return eval_max
    else:
        eval_min = math.inf
        curr_state.children = calc_all_succ_states(copy.deepcopy(curr_state))
        for child in curr_state.children:
            if child != None:
                eval_new = minimax(child, ply - 1, True)
                eval_min = min(eval_min, eval_new)
        return eval_min
    
def create_init_state():
    # Will generate a state node from the current board.
    state_node = StateNode(board)
    state_node.score_A = player_score_A
    state_node.score_B = player_score_B
    state_node.to_move = current_move
    return state_node

def calc_all_succ_states(state_node):
    # Given a state node, will generate four successor states.
    succ_states = []
    for i in range(1, 5):
        temp_state = calc_succ_state(state_node, i)
        if temp_state != None:
            succ_states.append(temp_state)
    return succ_states

def calc_succ_state(state_node, row):
    # Given a state node and a board row, will generate a successor state.
    succ_state = copy.deepcopy(state_node)
    curr_index = 0
    if row == 2:
        curr_index += 4
    if row == 3:
        curr_index += 8
    if row == 4:
        curr_index += 12
    # Checking all core nodes for potential cycle states.
    if row != 4:
        for i in range(curr_index, curr_index + 3):
            if check_cycle_edge(succ_state.board[i]):
                draw_cycle_edge(succ_state.board[i], succ_state)
                return succ_state
    edges_checked = 0
    # If no cycle states were found, pick a random node in the row.
    while(True):
        index_rand = rand.randint(curr_index, curr_index + 3)
    # Inspect its compliment nodes. If an edge can be drawn, draw it.
        node_rand = succ_state.board[index_rand]
        for comp in node_rand.cmp_list:
            # If the node is last on the board:
            if len(node_rand.cmp_list) == 0:
                break
            # If the node is a core node:
            if len(node_rand.cmp_list) == 3:
                if comp != node_rand.cmp_list[1]:
                    if comp not in node_rand.adj_list:
                        node_rand.adj_list.append(comp)
                        comp.adj_list.append(node_rand)
                        succ_state.last_move = (node_rand.name, comp.name)
                        if succ_state.to_move == 'A':
                            succ_state.to_move = 'B'
                        else:
                            succ_state.to_move = 'A'
                        return succ_state
                    else:
                        edges_checked += 1
            # If the node is last in the row:
            elif len(node_rand.cmp_list) == 1:
                if comp not in node_rand.adj_list:
                    node_rand.adj_list.append(comp)
                    comp.adj_list.append(node_rand)
                    succ_state.last_move = (node_rand.name, comp.name)
                    if succ_state.to_move == 'A':
                        succ_state.to_move = 'B'
                    else:
                         succ_state.to_move = 'A'
                    return succ_state
                else:
                    # If no edge can be drawn, tick the checked edges counter.
                    edges_checked += 1
        if edges_checked >= 7:
            break
    # No edges can be drawn; return a null object.
    return None

def check_cycle_edge(core):
    # Given a core node, will check if any nodes are one edge away from a cycle.
    edge_count = 0
    if core.cmp_list[0] in core.adj_list:
        edge_count += 1
    if core.cmp_list[1] in core.cmp_list[0].adj_list:
        edge_count += 1
    if core.cmp_list[2] in core.cmp_list[1].adj_list:
        edge_count += 1
    if core in core.cmp_list[2].adj_list:
        edge_count += 1
    if edge_count == 3:
        return True
    return False

def draw_cycle_edge(core, state_node):
    # Given a core node and a state node, will draw a cycle-completing edge.
    if core.cmp_list[0] not in core.adj_list:
        core.adj_list.append(core.cmp_list[0])
        core.cmp_list[0].adj_list.append(core)
        state_node.last_move = (core.name, core.cmp_list[0].name)
    if core.cmp_list[1] not in core.cmp_list[0].adj_list:
        core.cmp_list[0].adj_list.append(core.cmp_list[1])
        core.cmp_list[1].adj_list.append(core.cmp_list[0])
        state_node.last_move = (core.cmp_list[0].name, core.cmp_list[1].name)
    if core.cmp_list[2] not in core.cmp_list[1].adj_list:
        core.cmp_list[1].adj_list.append(core.cmp_list[2])
        core.cmp_list[2].adj_list.append(core.cmp_list[1])
        state_node.last_move = (core.cmp_list[1].name, core.cmp_list[2].name)
    if core not in core.cmp_list[2].adj_list:
        core.cmp_list[2].adj_list.append(core)
        core.adj_list.append(core.cmp_list[2])
        state_node.last_move = (core.cmp_list[2].name, core.name)
    core.claimed = True
    core.claimed_by = state_node.to_move
    # Adjusting state node fields to reflect move.
    if state_node.to_move == 'A':
        state_node.score_A += core.weight
        state_node.to_move = 'B'
    else:
        state_node.score_B += core.weight
        state_node.to_move = 'A'

def state_eval(state_node):
    # Given a state, will determine by how many points player B is winning.
    return state_node.score_B - state_node.score_A

def build_board():
    # An initializer for a 4x4 board.
    global board
    global board_total
    board = [
        Node('a1', 0), Node('a2', 0),  Node('a3', 0),  Node('a4', 0),
        Node('b1', 0), Node('b2', 0),  Node('b3', 0),  Node('b4', 0),
        Node('c1', 0), Node('c2', 0),  Node('c3', 0),  Node('c4', 0),
        Node('d1', 0), Node('d2', 0),  Node('d3', 0),  Node('d4', 0) 
    ]
    # Assigning compliment nodes to core nodes.
    for i in range(0, 3):
        board[i].weight = rand.randint(1, 5)
        board_total += board[i].weight
        board[i].cmp_list = [board[i + 1], board[i + 5], board[i + 4]]
    for i in range(4, 7):
        board[i].weight = rand.randint(1, 5)
        board_total += board[i].weight
        board[i].cmp_list = [board[i + 1], board[i + 5], board[i + 4]]
    for i in range(8, 11):
        board[i].weight = rand.randint(1, 5)
        board_total += board[i].weight
        board[i].cmp_list = [board[i + 1], board[i + 5], board[i + 4]]
    # Assigning compliment nodes to compliment nodes.
    for i in range(3, 12, 4):
        board[i].cmp_list = [board[i + 4]]
    for i in range(12, 15):
        board[i].cmp_list = [board[i + 1]]

def print_board():
    # Iterating through the board.
    for i in range(0, 16, 4):
        # Initializing two output strings for current row.
        output_hori = ''
        output_vert = ''
        for j in range(4):
            curr_node = board[i + j]
            output_hori += curr_node.name
            # If the current node is core:
            if curr_node.weight > 0:
                if curr_node.cmp_list[0] in curr_node.adj_list:
                    output_hori += ' \u2014 '
                else:
                    output_hori += '   '
                if curr_node.cmp_list[2] in curr_node.adj_list:
                    output_vert += ' \uFF5C '
                else:
                    output_vert += '   '
                if curr_node.claimed == False:
                    output_vert += ' ' + str(curr_node.weight)
                else:
                    output_vert += ' ' + curr_node.claimed_by
            else:
                # If the current node is not core but has compliments:
                if len(curr_node.cmp_list) > 0:
                    curr_ind = board.index(curr_node)
                    temp_ind = board.index(curr_node.cmp_list[0])
                    if temp_ind == curr_ind + 1:
                        if curr_node.cmp_list[0] in curr_node.adj_list:
                            output_hori += ' \u2014 '
                        else:
                            output_hori += '   '
                    if temp_ind == curr_ind + 4:
                        if curr_node.cmp_list[0] in curr_node.adj_list:
                            output_vert += ' \uFF5C '
                        else:
                            output_vert += '   '
        print(output_hori)
        print(output_vert)

def print_score():
    print('Player A: ' + str(player_score_A))
    print('Player B: ' + str(player_score_B))

def print_current_move():
    print("It is currently Player " + current_move + "'s turn to move.\n")

def next_move():
    global current_move
    if current_move == 'A':
        current_move = 'B'
    else:
        current_move = 'A'

def draw_edge(node1, node2):
    # Given two node names, will draw an edge between them.
    index1 = 0
    index2 = 0
    global board
    for n in board:
        if n.name == node1:
            index1 = board.index(n)
        if n.name == node2:
            index2 = board.index(n)
    board[index1].adj_list.append(board[index2])
    board[index2].adj_list.append(board[index1])
    return True

def assess_move():
    # Will check for newly claimed nodes and assign points accordingly.
    global player_score_A
    global player_score_B
    for i in range(16):
        core = board[i]
        if core.weight > 0 and core.claimed == False:
            verify1 = core.cmp_list[0] in core.adj_list
            verify2 = core.cmp_list[1] in core.cmp_list[0].adj_list
            verify3 = core.cmp_list[2] in core.cmp_list[1].adj_list
            verify4 = core in core.cmp_list[2].adj_list
            if verify1 and verify2 and verify3 and verify4:
                core.claimed = True
                core.claimed_by = current_move
                if current_move == 'A':
                    player_score_A += core.weight
                if current_move == 'B':
                    player_score_B += core.weight
                    
def end_game_check(state_node):
    # Will check if the game end state has been reached.
    end = True
    for i in state_node.board:
        if i.claimed == False:
            end = False
    return end

def end_game():
    # Will end the game, determine the winner, and exit the program.
    if player_score_A + player_score_B == board_total:
        if player_score_A > player_score_B:
            print('Player A wins with a score of ' + str(player_score_A) + '.')
            quit()
        if player_score_A < player_score_B:
            print('Player B wins with a score of ' + str(player_score_B) + '.')
            quit()
        print('Both players tie with scores of ' + str(player_score_A) + '.')
        quit()
