import math
import copy

X = "X"
O = "O"
EMPTY = None

def initial_state():
    return [[EMPTY, EMPTY, EMPTY],
            [EMPTY, EMPTY, EMPTY],
            [EMPTY, EMPTY, EMPTY]]

def player(board):
    # Count X and O to determine whose turn it is
    x_count = sum(row.count(X) for row in board)
    o_count = sum(row.count(O) for row in board)
    return O if x_count > o_count else X

def actions(board):
    possible_actions = set()
    for i in range(3):
        for j in range(3):
            if board[i][j] == EMPTY:
                possible_actions.add((i, j))
    return possible_actions

def result(board, action):
    if board[action[0]][action[1]] is not EMPTY:
        raise Exception("Invalid action")
    
    # Create a deep copy to keep the original board unmodified
    new_board = copy.deepcopy(board)
    new_board[action[0]][action[1]] = player(board)
    return new_board

def winner(board):
    # Check rows, columns, and diagonals
    for i in range(3):
        if board[i][0] == board[i][1] == board[i][2] and board[i][0] is not EMPTY:
            return board[i][0]
        if board[0][i] == board[1][i] == board[2][i] and board[0][i] is not EMPTY:
            return board[0][i]
            
    if board[0][0] == board[1][1] == board[2][2] and board[0][0] is not EMPTY:
        return board[0][0]
    if board[0][2] == board[1][1] == board[2][0] and board[0][2] is not EMPTY:
        return board[0][2]
        
    return None

def terminal(board):
    if winner(board) is not None:
        return True
    return all(cell is not EMPTY for row in board for cell in row)

def utility(board):
    win = winner(board)
    if win == X: return 1
    elif win == O: return -1
    return 0

def minimax(board):
    if terminal(board):
        return None

    curr_player = player(board)
    
    if curr_player == X:
        # Maximize for X
        v = -math.inf
        best_action = None
        for action in actions(board):
            val = min_value(result(board, action))
            if val > v:
                v = val
                best_action = action
        return best_action
    else:
        # Minimize for O
        v = math.inf
        best_action = None
        for action in actions(board):
            val = max_value(result(board, action))
            if val < v:
                v = val
                best_action = action
        return best_action

def max_value(board):
    if terminal(board): return utility(board)
    v = -math.inf
    for action in actions(board):
        v = max(v, min_value(result(board, action)))
    return v

def min_value(board):
    if terminal(board): return utility(board)
    v = math.inf
    for action in actions(board):
        v = min(v, max_value(result(board, action)))
    return v
