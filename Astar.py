from queue import PriorityQueue
import random

# The EightQueensState class represents the state of the chess board with queens placed on it.
class EightQueensState:
    # The constructor initializes a state with a given list of queen positions and depth.
    def __init__(self, queens=None, depth=0):
        if queens is None:
            queens = []  # No queens on the board by default
        self.queens = queens  # List of queen positions, index is row, value is column
        self.depth = depth  # The number of moves to reach the current state

    # This method checks if placing a queen in the given row and column will not cause conflicts.
    def is_valid_move(self, row, col):
        for r, c in enumerate(self.queens):
            # Check for column or diagonal conflicts
            if c == col or abs(row - r) == abs(col - c):
                return False
        return True  # Return true if no conflicts

    # This method generates all possible valid next states from the current state.
    def next_states(self):
        if len(self.queens) == 8:
            return []  # No next moves if the board is full (eight queens already placed)
        next_row = len(self.queens)  # The row we're trying to place a queen on
        # Return a list of new states with the new queen added in a valid column
        return [EightQueensState(self.queens + [col], self.depth + 1) for col in range(8) if
                self.is_valid_move(next_row, col)]

    # This method checks if the state is a goal state (a solution).
    def is_goal_state(self):
        return len(self.queens) == 8  # We reach the goal when 8 queens are placed without conflict

    # This heuristic function counts the number of pairs of queens that are attacking each other.
    def heuristic(self):
        attacking_pairs = 0  # Start with zero attacking pairs
        # Calculate the number of attacking pairs based on current placements
        for i in range(len(self.queens)):
            for j in range(i + 1, len(self.queens)):
                if abs(i - j) == abs(self.queens[i] - self.queens[j]):
                    attacking_pairs += 1
        return attacking_pairs  # Return the total number of attacking pairs

    # This method calculates and returns the f-score for the A* search algorithm.
    def f_score(self):
        return self.depth + self.heuristic()  # F-score = depth + heuristic value

    # This method defines comparison between two states based on their f-scores.
    def __lt__(self, other):
        return self.f_score() < other.f_score()  # For Priority Queue ordering

    # A class method to initialize a state with a single queen placed randomly.
    @classmethod
    def initialize_random(cls):
        col = random.randint(0, 7)  # Random column for the first queen
        return cls([col], 0)  # Return an instance with one queen placed

# The A* search algorithm implementation.
def a_star_search(initial_state):
    open_set = PriorityQueue()  # Open set for keeping track of the frontier
    open_set.put(initial_state)  # Start with the initial state
    came_from = {}  # Dictionary to reconstruct the path to the current state
    came_from[initial_state] = None  # Initial state has no predecessor
    total_moves = 0  # Counter for the total number of moves considered

    # Main loop that continues until there are no states to consider
    while not open_set.empty():
        current = open_set.get()  # Get the state with the lowest f-score

        # If the current state is the goal, reconstruct and return the path
        if current.is_goal_state():
            path = reconstruct_path(came_from, current)
            return path, current.depth, total_moves  # Return the path, depth, and total moves

        # For each valid next state, add it to the open set and keep track of its predecessor
        for next_state in current.next_states():
            if next_state not in came_from:
                open_set.put(next_state)
                came_from[next_state] = current
                total_moves += 1  # Increment the number of total moves

    return None, 0, 0  # If no solution, return None

# Function to reconstruct the path from the goal state to the initial state using the `came_from` dictionary.
def reconstruct_path(came_from, current):
    total_path = [current]  # Start with the goal state
    # Trace back the path from the goal state to the initial state
    while current in came_from and came_from[current] is not None:
        current = came_from[current]
        total_path.insert(0, current)  # Insert the predecessor at the beginning of the path
    return total_path  # Return the reconstructed path

# Initialize the initial state with one randomly placed queen.
initial_state = EightQueensState.initialize_random()
# Perform A* search algorithm to find a path to the solution.
path, depth, total_moves = a_star_search(initial_state)

# If a path is found, print the states along the path and the depth and total number of moves.
if path:
    for state in path:
     print(f"Depth {state.depth}: {state.queens} (Heuristic: {state.heuristic()})")
    print(f"Total path length: {len(path)}, reaching depth: {depth}")
    print(f"Total moves: {total_moves}")
else:
    print("No solution found.")  # Notify if no solution was found