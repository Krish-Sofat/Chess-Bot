import pygame
import chess
import engine # This imports the AI brain you built in your engine.py file


# --- User Input at Start ---
depth = int(input("Enter difficulty (1-4): "))
human_side = None
while human_side is None:
    player_choice = input("Do you want to play as (W)hite or (B)lack? ")
    if player_choice.upper() == 'W':
        human_side = chess.WHITE
    elif player_choice.upper() == 'B':
        human_side = chess.BLACK

# --- Pygame Setup ---
pygame.init()
SCREEN_WIDTH = 600
SCREEN_HEIGHT = 600
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("My Chess AI")
BOARD_SIZE = 8
SQUARE_SIZE = SCREEN_WIDTH // BOARD_SIZE

# Colors & Fonts
DARK_BROWN = (139, 69, 19)
LIGHT_TAN = (244, 226, 198)
HIGHLIGHT_COLOR = (255, 255, 51, 100)
FONT = pygame.font.SysFont('Arial', 32, True)

# Piece Image Loading
PIECE_IMAGES = {}
# ... (same image loading code as before) ...
PIECES = ['p', 'r', 'n', 'b', 'q', 'k', 'P', 'R', 'N', 'B', 'Q', 'K']
NAMES = ['black_pawn', 'black_rook', 'black_knight', 'black_bishop', 'black_queen', 'black_king',
         'white_pawn', 'white_rook', 'white_knight', 'white_bishop', 'white_queen', 'white_king']

for i in range(len(PIECES)):
    piece_symbol = PIECES[i]
    image_name = NAMES[i]
    try:
        image = pygame.image.load(f'images/{image_name}.png')
        PIECE_IMAGES[piece_symbol] = pygame.transform.scale(image, (SQUARE_SIZE, SQUARE_SIZE))
    except pygame.error:
        print(f"Error loading image: images/{image_name}.png. Make sure all 12 images are in the 'images' folder.")
        pygame.quit()
        exit()

# --- Drawing Functions ---
def draw_board(screen):
    for row in range(BOARD_SIZE):
        for col in range(BOARD_SIZE):
            color = LIGHT_TAN if (row + col) % 2 == 0 else DARK_BROWN
            pygame.draw.rect(screen, color, pygame.Rect(col * SQUARE_SIZE, row * SQUARE_SIZE, SQUARE_SIZE, SQUARE_SIZE))

def draw_pieces(screen, board):
    for square in chess.SQUARES:
        piece = board.piece_at(square)
        if piece:
            symbol = piece.symbol()
            image = PIECE_IMAGES[symbol]
            row, col = 7 - (square // 8), square % 8
            screen.blit(image, pygame.Rect(col * SQUARE_SIZE, row * SQUARE_SIZE, SQUARE_SIZE, SQUARE_SIZE))

def highlight_square(screen, square):
    if square is not None:
        row, col = 7 - (square // 8), square % 8
        highlight = pygame.Surface((SQUARE_SIZE, SQUARE_SIZE), pygame.SRCALPHA)
        highlight.fill(HIGHLIGHT_COLOR)
        screen.blit(highlight, (col * SQUARE_SIZE, row * SQUARE_SIZE))

def draw_game_over(screen, result):
    text = FONT.render(f"Game Over: {result}", True, (255, 0, 0))
    text_rect = text.get_rect(center=(SCREEN_WIDTH/2, SCREEN_HEIGHT/2))
    pygame.draw.rect(screen, (0,0,0,150), text_rect.inflate(20, 20)) # Semi-transparent background
    screen.blit(text, text_rect)

# --- Main Game Logic ---
def main():
    board = chess.Board()
    selected_square = None
    
    running = True
    while running:
        is_human_turn = (board.turn == human_side)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            
            if is_human_turn and event.type == pygame.MOUSEBUTTONDOWN and not board.is_game_over():
                pos = pygame.mouse.get_pos()
                col, row = pos[0] // SQUARE_SIZE, 7 - (pos[1] // SQUARE_SIZE)
                clicked_square = chess.square(col, row)

                if selected_square is None:
                    piece = board.piece_at(clicked_square)
                    if piece and piece.color == board.turn:
                        selected_square = clicked_square
                else:
                    move = chess.Move(selected_square, clicked_square)
                    if board.piece_at(selected_square).piece_type == chess.PAWN and (row == 0 or row == 7):
                        move.promotion = chess.QUEEN
                    
                    if move in board.legal_moves:
                        board.push(move)
                    selected_square = None

        if not is_human_turn and not board.is_game_over():
            pygame.display.set_caption("My Chess AI - Computer is thinking...")
            draw_board(screen); draw_pieces(screen, board); pygame.display.flip() # Update screen to show "thinking"
            
            ai_move = engine.get_ai_move(board, depth)
            if ai_move: board.push(ai_move)
            
            pygame.display.set_caption("My Chess AI")

        draw_board(screen)
        highlight_square(screen, selected_square)
        draw_pieces(screen, board)
        
        if board.is_game_over():
            draw_game_over(screen, board.result())
            running = False # Stop event loop but keep displaying result

        pygame.display.flip()

    # Keep window open after game over until user closes it
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                return

if __name__ == '__main__':
    main()