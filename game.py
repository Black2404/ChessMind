import pygame, sys, os, math, chess
from config import *
from ui import button, end_screen

# =============================
# LOAD IMAGES
# =============================
IMAGES = {}
pieces = ['p', 'r', 'n', 'b', 'q', 'k']
for c in ['w', 'b']:
    for p in pieces:
        path = os.path.join("images", f"{c}_{p}.png")
        img = pygame.image.load(path)
        IMAGES[f"{c}_{p}"] = pygame.transform.scale(img, (SQ_SIZE, SQ_SIZE))

# =============================
# PIECE-SQUARE TABLES + VALUES
# =============================
piece_values = {
    'P': 100, 'N': 320, 'B': 330, 'R': 500, 'Q': 900, 'K': 20000
}

PAWN_TABLE = [
    [0,0,0,0,0,0,0,0],
    [50,50,50,50,50,50,50,50],
    [10,10,20,30,30,20,10,10],
    [5,5,10,25,25,10,5,5],
    [0,0,0,20,20,0,0,0],
    [5,-5,-10,0,0,-10,-5,5],
    [5,10,10,-20,-20,10,10,5],
    [0,0,0,0,0,0,0,0]
]

KNIGHT_TABLE = [
    [-50,-40,-30,-30,-30,-30,-40,-50],
    [-40,-20,0,5,5,0,-20,-40],
    [-30,5,10,15,15,10,5,-30],
    [-30,0,15,20,20,15,0,-30],
    [-30,5,15,20,20,15,5,-30],
    [-30,0,10,15,15,10,0,-30],
    [-40,-20,0,0,0,0,-20,-40],
    [-50,-40,-30,-30,-30,-30,-40,-50]
]

BISHOP_TABLE = [
    [-20,-10,-10,-10,-10,-10,-10,-20],
    [-10,0,0,0,0,0,0,-10],
    [-10,0,5,10,10,5,0,-10],
    [-10,5,5,10,10,5,5,-10],
    [-10,0,10,10,10,10,0,-10],
    [-10,10,10,10,10,10,10,-10],
    [-10,5,0,0,0,0,5,-10],
    [-20,-10,-10,-10,-10,-10,-10,-20]
]

ROOK_TABLE = [
    [0,0,0,5,5,0,0,0],
    [-5,0,0,0,0,0,0,-5],
    [-5,0,0,0,0,0,0,-5],
    [-5,0,0,0,0,0,0,-5],
    [-5,0,0,0,0,0,0,-5],
    [-5,0,0,0,0,0,0,-5],
    [5,10,10,10,10,10,10,5],
    [0,0,0,0,0,0,0,0]
]

QUEEN_TABLE = [
    [-20,-10,-10,-5,-5,-10,-10,-20],
    [-10,0,0,0,0,0,0,-10],
    [-10,0,5,5,5,5,0,-10],
    [-5,0,5,5,5,5,0,-5],
    [0,0,5,5,5,5,0,-5],
    [-10,5,5,5,5,5,0,-10],
    [-10,0,5,0,0,0,0,-10],
    [-20,-10,-10,-5,-5,-10,-10,-20]
]

KING_TABLE = [
    [-30,-40,-40,-50,-50,-40,-40,-30],
    [-30,-40,-40,-50,-50,-40,-40,-30],
    [-30,-40,-40,-50,-50,-40,-40,-30],
    [-30,-40,-40,-50,-50,-40,-40,-30],
    [-20,-30,-30,-40,-40,-30,-30,-20],
    [-10,-20,-20,-20,-20,-20,-20,-10],
    [20,20,0,0,0,0,20,20],
    [20,30,10,0,0,10,30,20]
]

piece_tables = {
    'P': PAWN_TABLE,
    'N': KNIGHT_TABLE,
    'B': BISHOP_TABLE,
    'R': ROOK_TABLE,
    'Q': QUEEN_TABLE,
    'K': KING_TABLE
}

# =============================
# EVALUATION + AI
# =============================
def evaluate_board(board):
    if board.is_checkmate():
        return -99999 if board.turn else 99999
    if board.is_stalemate() or board.is_insufficient_material():
        return 0
    score = 0
    for square in chess.SQUARES:
        piece = board.piece_at(square)
        if piece:
            val = piece_values[piece.symbol().upper()]
            tbl = piece_tables[piece.symbol().upper()]
            row, col = divmod(square, 8)
            row = 7 - row
            pos = tbl[row][col]
            score += val + pos if piece.color == chess.WHITE else -(val + pos)
    return score

def minimax(board, depth, alpha, beta, maximizing):
    if depth == 0 or board.is_game_over():
        return evaluate_board(board), None
    best_move = None
    if maximizing:
        max_eval = -math.inf
        for move in board.legal_moves:
            board.push(move)
            eval, _ = minimax(board, depth - 1, alpha, beta, False)
            board.pop()
            if eval > max_eval:
                max_eval, best_move = eval, move
            alpha = max(alpha, eval)
            if beta <= alpha:
                break
        return max_eval, best_move
    else:
        min_eval = math.inf
        for move in board.legal_moves:
            board.push(move)
            eval, _ = minimax(board, depth - 1, alpha, beta, True)
            board.pop()
            if eval < min_eval:
                min_eval, best_move = eval, move
            beta = min(beta, eval)
            if beta <= alpha:
                break
        return min_eval, best_move

def get_ai_move(board, depth=2):
    _, move = minimax(board, depth, -math.inf, math.inf, board.turn)
    return move

# =============================
# DRAWING
# =============================
def draw_board(selected=None, valid_moves=[], check_square=None, last_move=None):
    colors = [WHITE, BLACK]
    for r in range(8):
        for c in range(8):
            color = colors[(r + c) % 2]
            pygame.draw.rect(SCREEN, color, (c * SQ_SIZE, r * SQ_SIZE, SQ_SIZE, SQ_SIZE))
            if selected == (r, c):
                pygame.draw.rect(SCREEN, RED, (c * SQ_SIZE, r * SQ_SIZE, SQ_SIZE, SQ_SIZE), 3)
            if (r, c) in valid_moves:
                pygame.draw.circle(SCREEN, HIGHLIGHT, (c * SQ_SIZE + SQ_SIZE // 2, r * SQ_SIZE + SQ_SIZE // 2), 10)
    if check_square:
        r, c = check_square
        pygame.draw.rect(SCREEN, RED, (c * SQ_SIZE, r * SQ_SIZE, SQ_SIZE, SQ_SIZE), 5)
    if last_move:
        for (r, c) in last_move:
            pygame.draw.rect(SCREEN, GREEN, (c * SQ_SIZE, r * SQ_SIZE, SQ_SIZE, SQ_SIZE), 4)

def draw_pieces(board):
    for r in range(8):
        for c in range(8):
            square = chess.square(c, 7 - r)
            piece = board.piece_at(square)
            if piece:
                key = ('w_' if piece.color == chess.WHITE else 'b_') + piece.symbol().lower()
                SCREEN.blit(IMAGES[key], (c * SQ_SIZE, r * SQ_SIZE))

# =============================
# GAME LOOP
# =============================
def play_game(vs_ai):
    board = chess.Board()
    selected = None
    valid_moves = []
    check_sq = None
    running = True
    last_move = None
    while running:
        CLOCK.tick(FPS)
        mx, my = pygame.mouse.get_pos()
        click = False
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                click = True
                if my < WIDTH:
                    c = mx // SQ_SIZE
                    r = my // SQ_SIZE
                    square = chess.square(c, 7 - r)
                    if selected is None:
                        piece = board.piece_at(square)
                        if piece and piece.color == board.turn:
                            selected = (r, c)
                            valid_moves = [(7 - (m.to_square // 8), m.to_square % 8)
                                           for m in board.legal_moves if m.from_square == square]
                    else:
                        move = chess.Move(chess.square(selected[1], 7 - selected[0]), square)
                        if move in board.legal_moves:
                            board.push(move)
                            last_move = [(selected[0], selected[1]), (r, c)]
                        selected = None
                        valid_moves = []
                if button("Restart", WIDTH // 2 - 140, 650, (mx, my), click):
                    return play_game(vs_ai)
                if button("Quit", WIDTH // 2 + 20, 650, (mx, my), click):
                    return

        if vs_ai and board.turn == chess.BLACK and not board.is_game_over():
            ai = get_ai_move(board, 2)
            if ai:
                board.push(ai)
                fr, fc = 7 - (ai.from_square // 8), ai.from_square % 8
                tr, tc = 7 - (ai.to_square // 8), ai.to_square % 8
                last_move = [(fr, fc), (tr, tc)]

        if board.is_check():
            k = board.king(board.turn)
            check_sq = (7 - (k // 8), k % 8)
        else:
            check_sq = None

        draw_board(selected, valid_moves, check_sq, last_move)
        draw_pieces(board)
        button("Restart", WIDTH // 2 - 140, 650, (mx, my), click)
        button("Quit", WIDTH // 2 + 20, 650, (mx, my), click)

        if board.is_checkmate():
            winner = "Black wins!" if board.turn == chess.WHITE else "White wins!"
            running = end_screen(board, winner, draw_board, draw_pieces, play_game, vs_ai)
            if running:
                return play_game(vs_ai)
            else:
                return
        elif board.is_stalemate() or board.is_insufficient_material():
            running = end_screen(board, "Draw!", draw_board, draw_pieces, play_game, vs_ai)
            if running:
                return play_game(vs_ai)
            else:
                return

        pygame.display.flip()
