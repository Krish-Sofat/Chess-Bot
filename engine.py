import chess
import random

# --- EVALUATION DATA ---
PIECE_VALUES = {
    chess.PAWN: 100,
    chess.KNIGHT: 320,
    chess.BISHOP: 330,
    chess.ROOK: 500,
    chess.QUEEN: 900,
    chess.KING: 20000
}

PAWN_PST = [
    0,  0,  0,  0,  0,  0,  0,  0, 50, 50, 50, 50, 50, 50, 50, 50, 10, 10, 20, 30, 30, 20, 10, 10,
    5,  5, 10, 25, 25, 10,  5,  5, 0,  0,  0, 20, 20,  0,  0,  0, 5, -5,-10,  0,  0,-10, -5,  5,
    5, 10, 10,-20,-20, 10, 10,  5, 0,  0,  0,  0,  0,  0,  0,  0
]
KNIGHT_PST = [
    -50,-40,-30,-30,-30,-30,-40,-50, -40,-20,  0,  0,  0,  0,-20,-40, -30,  0, 10, 15, 15, 10,  0,-30,
    -30,  5, 15, 20, 20, 15,  5,-30, -30,  0, 15, 20, 20, 15,  0,-30, -30,  5, 10, 15, 15, 10,  5,-30,
    -40,-20,  0,  5,  5,  0,-20,-40, -50,-40,-30,-30,-30,-30,-40,-50
]
BISHOP_PST = [
    -20,-10,-10,-10,-10,-10,-10,-20, -10,  0,  0,  0,  0,  0,  0,-10, -10,  0,  5, 10, 10,  5,  0,-10,
    -10,  5,  5, 10, 10,  5,  5,-10, -10,  0, 10, 10, 10, 10,  0,-10, -10, 10, 10, 10, 10, 10, 10,-10,
    -10,  5,  0,  0,  0,  0,  5,-10, -20,-10,-10,-10,-10,-10,-10,-20
]
ROOK_PST = [
    0,  0,  0,  0,  0,  0,  0,  0, 5, 10, 10, 10, 10, 10, 10,  5, -5,  0,  0,  0,  0,  0,  0, -5,
    -5,  0,  0,  0,  0,  0,  0, -5, -5,  0,  0,  0,  0,  0,  0, -5, -5,  0,  0,  0,  0,  0,  0, -5,
    -5,  0,  0,  0,  0,  0,  0, -5, 0,  0,  0,  5,  5,  0,  0,  0
]
QUEEN_PST = [
    -20,-10,-10, -5, -5,-10,-10,-20, -10,  0,  0,  0,  0,  0,  0,-10, -10,  0,  5,  5,  5,  5,  0,-10,
    -5,  0,  5,  5,  5,  5,  0, -5, 0,  0,  5,  5,  5,  5,  0, -5, -10,  5,  5,  5,  5,  5,  0,-10,
    -10,  0,  5,  0,  0,  0,  0,-10, -20,-10,-10, -5, -5,-10,-10,-20
]
KING_PST = [
    -30,-40,-40,-50,-50,-40,-40,-30, -30,-40,-40,-50,-50,-40,-40,-30, -30,-40,-40,-50,-50,-40,-40,-30,
    -30,-40,-40,-50,-50,-40,-40,-30, -20,-30,-30,-40,-40,-30,-30,-20, -10,-20,-20,-20,-20,-20,-20,-10,
    20, 20,  0,  0,  0,  0, 20, 20, 20, 40, 10,  0,  0, 10, 40, 20
]

PIECE_SQUARE_TABLES = {
    chess.PAWN: PAWN_PST, chess.KNIGHT: KNIGHT_PST, chess.BISHOP: BISHOP_PST,
    chess.ROOK: ROOK_PST, chess.QUEEN: QUEEN_PST, chess.KING: KING_PST
}

# --- AI FUNCTIONS ---

def evaluate_board(board):
    if board.is_checkmate():
        return -float('inf') if board.turn == chess.WHITE else float('inf')
    if board.is_game_over():
        return 0
    
    score = 0
    for square in chess.SQUARES:
        piece = board.piece_at(square)
        if piece:
            material_value = PIECE_VALUES[piece.piece_type]
            pst = PIECE_SQUARE_TABLES[piece.piece_type]
            positional_value = pst[square] if piece.color == chess.WHITE else pst[chess.square_mirror(square)]
            
            if piece.color == chess.WHITE:
                score += material_value + positional_value
            else:
                score -= material_value + positional_value
    return score

def minimax(board, depth, alpha,beta):
    if depth == 0 or board.is_game_over():
        return evaluate_board(board)

    if board.turn==chess.WHITE:
        max_eval = -float('inf')
        for move in board.legal_moves:
            board.push(move)
            eval = minimax(board, depth - 1,alpha,beta)
            board.pop()
            max_eval = max(max_eval, eval)
            alpha = max(alpha, eval)
            if beta <= alpha:
                break
        return max_eval
    else:
        min_eval = float('inf')
        for move in board.legal_moves:
            board.push(move)
            eval = minimax(board, depth - 1, alpha,beta)
            board.pop()
            min_eval = min(min_eval, eval)
            beta = min(beta, eval)
            if beta <= alpha:
                break
        return min_eval

def get_ai_move(board, depth):
    best_moves_list = []
    best_score = -float('inf') if board.turn == chess.WHITE else float('inf')

    for move in board.legal_moves:
        board.push(move)
        current_score = minimax(board, depth - 1, -float('inf'),float('inf'))
        board.pop()

        if board.turn == chess.WHITE:
            if current_score > best_score:
                best_score = current_score
                best_moves_list = [move]
            elif current_score == best_score:
                best_moves_list.append(move)
        else:
            if current_score < best_score:
                best_score = current_score
                best_moves_list = [move]
            elif current_score == best_score:
                best_moves_list.append(move)
    
    return random.choice(best_moves_list) if best_moves_list else None