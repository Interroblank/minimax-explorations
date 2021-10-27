import auxiliary as aux

def dfs(init_state, goal_state):
    # Initializing diagnostic counters.
    solution_depth = 0  # Depth of solution state.
    solution_cost = 0   # Cost of solution state.
    queue_pops = 0      # Number of queue pops (time).
    queue_peak = 0      # Peak queue size (space).
    repeated_states = 0 # Repeated states pruned. (?)
    total_states = 0    # Total states considered.
    # Initializing state dictionaries.
    parents = {}    # State parents.
    children = {}   # State children.
    cost = {}       # Cost of path.
    expanded = {}   # If state has been expanded.
    depth = {}      # State depth in search tree.
    # Initializing the stack.
    stack = []
    # Pushing the initial state.
    stack.append(init_state)
    depth[tuple(init_state)] = 0
    # Calculating successors.
    init_all_succ = aux.calc_all_succ(init_state)
    # Mapping initial state to valid successor states.
    # Must cast list of children to type tuple to map.
    children[tuple(init_state)] = init_all_succ
    while stack: # While the stack is not empty:
        if (len(stack) > queue_peak):
            queue_peak = len(stack)
        curr = stack.pop() # Pop the next node in the stack.
        queue_pops = queue_pops + 1
        for neighbor in children[tuple(curr)]: # For each neighbor of 'curr':
            total_states = total_states + 1
            if tuple(neighbor) not in expanded.keys():
                # If this neighbor hasn't been expanded:
                expanded[tuple(neighbor)] = True
                # Calculating successors.
                children[tuple(neighbor)] = aux.calc_all_succ(neighbor)
                # Mapping necessary data and pushing state to stack.
                parents[tuple(neighbor)] = curr
                depth[tuple(neighbor)] = depth[tuple(curr)] + 1
                # print(neighbor)
                if neighbor == goal_state:
                    print('\nGoal reached.')
                    stack = [] # Emptying the stack.
                    break
                stack.append(neighbor)
            else:
                repeated_states = repeated_states + 1
    path_state = goal_state
    path_stack = []
    # Looping through 'parents' dict starting from goal state.
    # Pushing instructions as strings to a stack.
    # Breaking the loop when the initial state is reached.
    while (path_state != init_state):
        path_stack.append(path_state)
        path_state = parents[tuple(path_state)]
    print('\nFinished determining path.\n')
    # Popping from stack until empty and print path to goal state.
    print(init_state)
    while path_stack:
        print(path_stack.pop())
        solution_depth = solution_depth + 1
    print('\nFinished printing path.\n')
    aux.print_diagnostics( # TODO - Make this accept arguments as a tuple.
        solution_depth,
        solution_cost,
        queue_pops,
        queue_peak,
        repeated_states,
        total_states)
