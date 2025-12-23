import chess
import random
depth=int(input("enter 1,2,3,4 for difficulty"))
PIECE_VALUES = {
    chess.PAWN: 100,
    chess.KNIGHT: 320,
    chess.BISHOP: 330,
    chess.ROOK: 500,
    chess.QUEEN: 900,
    chess.KING: 20000  
}
PAWN_PST = [
    0,  0,  0,  0,  0,  0,  0,  0,
    50, 50, 50, 50, 50, 50, 50, 50,
    10, 10, 20, 30, 30, 20, 10, 10,
     5,  5, 10, 25, 25, 10,  5,  5,
     0,  0,  0, 20, 20,  0,  0,  0,
     5, -5,-10,  0,  0,-10, -5,  5,
     5, 10, 10,-20,-20, 10, 10,  5,
     0,  0,  0,  0,  0,  0,  0,  0
]
KNIGHT_PST = [
    -50,-40,-30,-30,-30,-30,-40,-50,
    -40,-20,  0,  0,  0,  0,-20,-40,
    -30,  0, 10, 15, 15, 10,  0,-30,
    -30,  5, 15, 20, 20, 15,  5,-30,
    -30,  0, 15, 20, 20, 15,  0,-30,
    -30,  5, 10, 15, 15, 10,  5,-30,
    -40,-20,  0,  5,  5,  0,-20,-40,
    -50,-40,-30,-30,-30,-30,-40,-50,
]
BISHOP_PST = [
    -20,-10,-10,-10,-10,-10,-10,-20,
    -10,  0,  0,  0,  0,  0,  0,-10,
    -10,  0,  5, 10, 10,  5,  0,-10,
    -10,  5,  5, 10, 10,  5,  5,-10,
    -10,  0, 10, 10, 10, 10,  0,-10,
    -10, 10, 10, 10, 10, 10, 10,-10,
    -10,  5,  0,  0,  0,  0,  5,-10,
    -20,-10,-10,-10,-10,-10,-10,-20,
]
ROOK_PST = [
    0,  0,  0,  0,  0,  0,  0,  0,
    5, 10, 10, 10, 10, 10, 10,  5,
    -5,  0,  0,  0,  0,  0,  0, -5,
    -5,  0,  0,  0,  0,  0,  0, -5,
    -5,  0,  0,  0,  0,  0,  0, -5,
    -5,  0,  0,  0,  0,  0,  0, -5,
    -5,  0,  0,  0,  0,  0,  0, -5,
    0,  0,  0,  5,  5,  0,  0,  0
]
QUEEN_PST = [
    -20,-10,-10, -5, -5,-10,-10,-20,
    -10,  0,  0,  0,  0,  0,  0,-10,
    -10,  0,  5,  5,  5,  5,  0,-10,
    -5,  0,  5,  5,  5,  5,  0, -5,
    0,  0,  5,  5,  5,  5,  0, -5,
    -10,  5,  5,  5,  5,  5,  0,-10,
    -10,  0,  5,  0,  0,  0,  0,-10,
    -20,-10,-10, -5, -5,-10,-10,-20
]
KING_PST = [
    -30,-40,-40,-50,-50,-40,-40,-30,
    -30,-40,-40,-50,-50,-40,-40,-30,
    -30,-40,-40,-50,-50,-40,-40,-30,
    -30,-40,-40,-50,-50,-40,-40,-30,
    -20,-30,-30,-40,-40,-30,-30,-20,
    -10,-20,-20,-20,-20,-20,-20,-10,
    20, 20,  0,  0,  0,  0, 20, 20,
    20, 30, 10,  0,  0, 10, 30, 20
]

PIECE_SQUARE_TABLES={
    chess.PAWN: PAWN_PST,
    chess.KNIGHT: KNIGHT_PST,
    chess.BISHOP: BISHOP_PST,
    chess.ROOK: ROOK_PST,
    chess.QUEEN: QUEEN_PST,
    chess.KING: KING_PST}
def Score(board):
    score=0
    for square in chess.SQUARES:
        piece=board.piece_at(square)
        if piece:
            value = PIECE_VALUES[piece.piece_type]
            pst = PIECE_SQUARE_TABLES[piece.piece_type]
            if piece.color == chess.WHITE:
                positional_value = pst[square]
                score=score+value+positional_value
            else:
                positional_value = pst[chess.square_mirror(square)]
                score=score-(value+positional_value)
    return score

def minimax(board,depth):
    if depth == 0 or board.is_game_over():
        return Score(board)
    if board.turn == chess.WHITE:
        max_eval = -float('inf')
        for move in board.legal_moves:
            board.push(move)
            eval = minimax(board, depth - 1)
            board.pop()
            max_eval = max(max_eval, eval)
        return max_eval
    else:
        min_eval = float('inf')
        for move in board.legal_moves:
            board.push(move)
            eval = minimax(board, depth - 1)
            board.pop()
            min_eval = min(min_eval, eval)
        return min_eval

def get_ai_move(board, depth):
    best_moves_list = []

    if human_side == chess.BLACK:
        best_score = -float('inf')
    else:
        best_score = float('inf')

    for move in board.legal_moves:
        board.push(move)
        current_score = minimax(board, depth - 1)
        board.pop()

        if human_side == chess.BLACK:
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
human_side = None
while human_side is None:
    player_choice = input("Do you want to play as (W)hite or (B)lack? ")
    if player_choice.upper() == 'W':
        human_side = chess.WHITE
        print("You will play as White.")
    elif player_choice.upper() == 'B':
        human_side = chess.BLACK
        print("You will play as Black.")
    else:
        print("Invalid choice. Please enter 'W' or 'B'.")

board = chess.Board()
print("The initial board state is:")
print(board)
print("--------------------")
while not board.is_game_over():
    if board.turn == human_side:
        while True:
            move1=input("Enter your move:")
            try:
                move_to_make=board.parse_uci(move1)
                break
            except:
                print("please enter a legal move")
        board.push(move_to_make)
        print(f"making the move {move_to_make.uci()}")
        print("--------------------")
        print(board)
    else:
        print("computer is thinking....")
        ai_move = get_ai_move(board, depth)
        if ai_move is None:
            ai_move = random.choice(list(board.legal_moves))
        board.push(ai_move)
        print(f"computer moves {ai_move.uci()}")
        print("--------------------")
        print(board)
print(f"Game over. Result: {board.result()}")




    


