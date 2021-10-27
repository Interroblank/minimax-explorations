# A collection of auxiliary functions utilized by the search algorithms.

def calc_succ(state, move_dir):
    # Given a state and a direction, will calculate a successor state.
    curr_pos = state.index(0)
    new_state = state.copy()
    # print(curr_pos)
    if move_dir == 'U': # Move up.
        if curr_pos in range(3):        # Out-of-bounds check.
            # print('Invalid movement.')
            return None
        # Swapping tiles after verifying validity of move.
        temp_tile = new_state[curr_pos - 3]
        new_state[curr_pos - 3] = new_state[curr_pos]
        new_state[curr_pos] = temp_tile
    if move_dir == 'D': # Move down.
        if curr_pos in range(6, 10):    # Out-of-bounds check.
            # print('Invalid movement.')
            return None
        # Swapping tiles after verifying validity of move.
        temp_tile = new_state[curr_pos + 3]
        new_state[curr_pos + 3] = new_state[curr_pos]
        new_state[curr_pos] = temp_tile
    if move_dir == 'L': # Move left.
        if curr_pos in range(0, 9, 3):  # Out-of-bounds check.
            # print('Invalid movement.')
            return None
        # Swapping tiles after verifying validity of move.
        temp_tile = new_state[curr_pos - 1]
        new_state[curr_pos - 1] = new_state[curr_pos]
        new_state[curr_pos] = temp_tile
    if move_dir == 'R': # Move right.
        if curr_pos in range(2, 9, 3):  # Out-of-bounds check.
            # print('Invalid movement.')
            return None
        # Swapping tiles after verifying validity of move.
        temp_tile = new_state[curr_pos + 1]
        new_state[curr_pos + 1] = new_state[curr_pos]
        new_state[curr_pos] = temp_tile
    # print(new_state)
    return new_state

def calc_all_succ(state):
    # Given a state, will return a list of all valid successor states.
    dirs = ['U', 'D', 'L', 'R']
    all_succ = []
    for d in dirs:
        temp_state = calc_succ(state, d)
        if temp_state != None:
            all_succ.append(temp_state)
    return all_succ

def move_check(state1, state2): # TODO.
    # Given two states, will return the move from 'state1' to 'state2'.
    pass

def cost_check(state1, state2):
    # Given two states, will return the cost of the move between them.
    return state2[state1.index(0)]

def calc_h1(curr_state, goal_state):
    # Given a state and goal, will calculate heuristic 'h1'.
    h1 = 0
    for tile in goal_state:
        if curr_state.index(tile) != goal_state.index(tile):
            h1 += 1
    return h1

def calc_h2(curr_state, goal_state):
    # Given a state and goal, will calculate heuristic 'h2'.
    h2 = 0
    for i in range(0, 9):
        h2 =+ calc_man_dist(i, curr_state, goal_state)
    return h2

def calc_man_dist(tile, curr_state, goal_state):
    # Will calculate a given tile in a given state's Manhattan distance.
    curr_index = curr_state.index(tile)
    goal_index = goal_state.index(tile)
    # Determining tile positions relative to puzzle rows and columns.
    curr_row = row_check(curr_index)
    curr_col = col_check(curr_index)
    targ_row = row_check(goal_index)
    targ_col = col_check(goal_index)
    # Calculating and returning Manhattan distance.
    return (abs(curr_row - targ_row) + abs(curr_col - targ_col))

def row_check(tile_index):
    # Given a tile index, will return the tile's location by row.
    if tile_index in range(0, 3):
        return 1
    if tile_index in range(3, 6):
        return 2
    if tile_index in range(6, 9):
        return 3
    return 0

def col_check(tile_index):
    # Given a tile index, will return the tile's location by column.
    if tile_index in range(0, 9, 3):
        return 1
    if tile_index in range(1, 9, 3):
        return 2
    if tile_index in range(2, 9, 3):
        return 3
    return 0

def print_diagnostics(depth, cost, pops, peak, repeats, total):
    # Given diagnostic data, will cleanly output diagnostics.
    # TODO - Make this accept arguments as a tuple.
    print('Diagnostics:')
    print(' Solution Path Length:    ' + str(depth))
    if cost == 0:
        print(' Solution Path Cost:      N/A')
    else:
        print(' Solution Path Cost:      ' + str(cost))
    print(' Queue Nodes Popped:      ' + str(pops))
    print(' Queue Peak Size:         ' + str(peak))
    # print(' Repeated States Pruned:  ' + str(repeats))
    # print(' Total States Considered: ' + str(total))
    print('\n')
