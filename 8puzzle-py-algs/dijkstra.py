import auxiliary as aux
import heapq as hq

class Node:
    def __init__(self):
        self.parent = None
        self.children = []
        self.state = []
        self.cost = float('inf')
        self.depth = 0
    # Overloading comparison operators.
    def __gt__(self, r_node):
        if self.cost > r_node.cost:
            return True
        return False
    def __lt__(self, r_node):
        if self.cost < r_node.cost:
            return True
        return False
    def __ge__(self, r_node):
        if self.cost >= r_node.cost:
            return True
        return False
    def __le__(self, r_node):
        if self.cost <= r_node.cost:
            return True
        return False
    def __eq__(self, r_node):
        if self.cost == r_node.cost:
            return True
        return False
    def __ne__(self, r_node):
        if self.cost != r_node.cost:
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

def dijkstra(init_state, goal_state):
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
            expanded[tuple(curr.state)] = True
            # Calculating successor states.
            curr.children = aux.calc_all_succ(curr.state)
            # Pushing all children to queue.
            for child_state in curr.children:
                total_states += 1
                # Creating node for successor state.
                child_node = Node()
                child_node.state = child_state
                # Calculating new path cost.
                child_node.cost = aux.cost_check(curr.state, child_state)
                child_node.cost += curr.cost # Path cost added to child cost.
                child_node.parent = curr
                # print(child_node.state)
                # Checking if 'child_state' matches 'goal_state'.
                if child_state == goal_state:
                    print('\nGoal reached.\n')
                    queue = [] # Emptying the queue.
                    solution_cost = child_node.cost
                    backpath_node = child_node
                    break
                # Checking for new minimum distance.
                if curr.cost + child_node.cost < child_node.cost:
                    # print('Checking for new minimum distance.')
                    child_node.cost = curr.cost + child_node.cost
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
        solution_depth += 1
    print('\nFinished printing path.\n')
    aux.print_diagnostics( # TODO - Make this accept arguments as a tuple.
        solution_depth,
        solution_cost,
        queue_pops,
        queue_peak,
        repeated_states,
        total_states)
        
