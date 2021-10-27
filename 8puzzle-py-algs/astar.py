import auxiliary as aux
import heapq as hq

class Node:
    def __init__(self):
        self.parent = None
        self.children = []
        self.state = []
        self.cost = float('inf')    # ?
        self.depth = 0
        self.f_val = 0
    # Overloading comparison operators.
    def __gt__(self, r_node):
        if self.f_val > r_node.f_val:
            return True
        return False
    def __lt__(self, r_node):
        if self.f_val < r_node.f_val:
            return True
        return False
    def __ge__(self, r_node):
        if self.f_val >= r_node.f_val:
            return True
        return False
    def __le__(self, r_node):
        if self.f_val <= r_node.f_val:
            return True
        return False
    def __eq__(self, r_node):
        if self.f_val == r_node.f_val:
            return True
        return False
    def __ne__(self, r_node):
        if self.f_val != r_node.f_val:
            return True
        return False
    # Overloading string cast.
    def __str__(self):
        pa_str = str(self.parent) + '\n'
        ch_str = str(self.children) + '\n'
        st_str = str(self.state) + '\n'
        co_str = str(self.cost) + '\n'
        de_str = str(self.depth) + '\n'
        return pa_str + ch_str + st_str + co_str + de_str

def astar_h1(init_state, goal_state):
    expanded = {}
    # Initializing diagnostic counters.
    solution_depth = 0  # Depth of solution state.
    solution_cost = 0   # Cost of solution state.
    queue_pops = 0      # Number of queue pops (time).
    queue_peak = 0      # Peak queue size (space).
    repeated_states = 0 # Repeated states pruned. (?)
    total_states = 0    # Total states considered.
    # From initial state, initializing node.
    init_node = Node()
    init_node.state = init_state
    init_node.cost = 0
    # Creating priority queue and pushing first node.
    queue = []
    hq.heappush(queue, init_node)
    backpath_node = Node()
    while queue: # While the queue is not empty:
        if (len(queue) > queue_peak):
            queue_peak = len(queue)
        # Pop the next state:
        curr = hq.heappop(queue)
        queue_pops = queue_pops + 1
        # If we haven't been to this state before:
        if tuple(curr.state) not in expanded:
            total_states += 1
            expanded[tuple(curr.state)] = True
            # Calculating successor states.
            curr.children = aux.calc_all_succ(curr.state)
            # For each successor state:
            for child_state in curr.children:
                if tuple(child_state) in expanded:
                    continue # ?
                # Creating node for successor state.
                child_node = Node()
                child_node.state = child_state
                child_node.parent = curr # ?
                # Calculating 'f_val' with heuristic 'h1'.
                child_node.cost = aux.cost_check(curr.state, child_state)
                child_node.cost += curr.cost
                h1 = aux.calc_h1(child_state, goal_state)
                child_node.f_val = child_node.cost + h1
                # Have we reached the goal state?
                if child_state == goal_state:
                    print('\nGoal reached.\n')
                    queue = [] # Emptying the queue.
                    solution_cost = child_node.cost
                    backpath_node = child_node
                    break
                hq.heappush(queue, child_node)
        else:
            repeated_states += 1
    path_stack = []
    while backpath_node:
        # print(backpath_node.state)
        path_stack.append(backpath_node.state)
        backpath_node = backpath_node.parent
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

def astar_h2(init_state, goal_state):
    expanded = {}
    # Initializing diagnostic counters.
    solution_depth = 0  # Depth of solution state.
    solution_cost = 0   # Cost of solution state.
    queue_pops = 0      # Number of queue pops (time).
    queue_peak = 0      # Peak queue size (space).
    repeated_states = 0 # Repeated states pruned. (?)
    total_states = 0    # Total states considered.
    # From initial state, initializing node.
    init_node = Node()
    init_node.state = init_state
    init_node.cost = 0
    # Creating priority queue and pushing first node.
    queue = []
    hq.heappush(queue, init_node)
    backpath_node = Node()
    while queue: # While the queue is not empty:
        if (len(queue) > queue_peak):
            queue_peak = len(queue)
        # Pop the next state:
        curr = hq.heappop(queue)
        queue_pops = queue_pops + 1
        # If we haven't been to this state before:
        if tuple(curr.state) not in expanded:
            total_states += 1
            expanded[tuple(curr.state)] = True
            # Calculating successor states.
            curr.children = aux.calc_all_succ(curr.state)
            # For each successor state:
            for child_state in curr.children:
                if tuple(child_state) in expanded:
                    continue # ?
                # Creating node for successor state.
                child_node = Node()
                child_node.state = child_state
                child_node.parent = curr # ?
                # Calculating 'f_val' with heuristic 'h1'.
                child_node.cost = aux.cost_check(curr.state, child_state)
                child_node.cost += curr.cost
                h2 = aux.calc_h2(child_state, goal_state)
                child_node.f_val = child_node.cost + h2
                # TODO - Consider path cost as in Dijkstra's. (?)
                if child_state == goal_state:
                    print('\nGoal reached.\n')
                    queue = [] # Emptying the queue.
                    solution_cost = child_node.cost
                    backpath_node = child_node
                    break
                hq.heappush(queue, child_node)
        else:
            repeated_states += 1
    path_stack = []
    while backpath_node:
        # print(backpath_node.state)
        path_stack.append(backpath_node.state)
        backpath_node = backpath_node.parent
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
