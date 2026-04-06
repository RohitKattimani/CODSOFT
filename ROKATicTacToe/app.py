from flask import Flask, render_template, request, jsonify
import math

app = Flask(__name__)

def check_winner(board):
    """Checks if there is a winner on the board."""
    win_states = [
        (0, 1, 2), (3, 4, 5), (6, 7, 8), # Rows
        (0, 3, 6), (1, 4, 7), (2, 5, 8), # Columns
        (0, 4, 8), (2, 4, 6)             # Diagonals
    ]
    for a, b, c in win_states:
        if board[a] == board[b] == board[c] and board[a] != '':
            return board[a]
    if '' not in board:
        return 'Tie'
    return None

def minimax(board, depth, alpha, beta, is_maximizing):
    """Minimax algorithm with Alpha-Beta pruning."""
    winner = check_winner(board)
    
    # Base cases: return scores based on depth to prefer faster wins
    if winner == 'O': return 10 - depth
    if winner == 'X': return depth - 10
    if winner == 'Tie': return 0

    if is_maximizing:
        max_eval = -math.inf
        for i in range(9):
            if board[i] == '':
                board[i] = 'O'
                eval = minimax(board, depth + 1, alpha, beta, False)
                board[i] = ''
                max_eval = max(max_eval, eval)
                alpha = max(alpha, eval)
                if beta <= alpha:
                    break # Prune
        return max_eval
    else:
        min_eval = math.inf
        for i in range(9):
            if board[i] == '':
                board[i] = 'X'
                eval = minimax(board, depth + 1, alpha, beta, True)
                board[i] = ''
                min_eval = min(min_eval, eval)
                beta = min(beta, eval)
                if beta <= alpha:
                    break # Prune
        return min_eval

def get_best_move(board):
    """Calculates the best move for the AI ('O')."""
    best_score = -math.inf
    move = -1
    for i in range(9):
        if board[i] == '':
            board[i] = 'O'
            score = minimax(board, 0, -math.inf, math.inf, False)
            board[i] = ''
            if score > best_score:
                best_score = score
                move = i
    return move

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/move', methods=['POST'])
def make_move():
    data = request.get_json()
    board = data.get('board')
    
    # If the board is already full or won, don't calculate
    if check_winner(board):
        return jsonify({'move': -1})
        
    best_move = get_best_move(board)
    return jsonify({'move': best_move})

if __name__ == '__main__':
    app.run(debug=True)