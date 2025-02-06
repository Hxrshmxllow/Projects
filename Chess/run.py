from game import Game
import pygame
from king import King
from model import predict_move

WINDOW_SIZE = 800
GRID_SIZE = 8
SQUARE_SIZE = WINDOW_SIZE // GRID_SIZE

WHITE = (240, 217, 181)
BLACK = (181, 136, 99)
RED = (255, 0, 0)
GREEN = (0, 255, 0)

pygame.init()
screen = pygame.display.set_mode((WINDOW_SIZE, WINDOW_SIZE))
pygame.display.set_caption("Chess Board")

def draw_board(game):
    for row in range(GRID_SIZE):
        for col in range(GRID_SIZE):
            if game.board[row][col].highlighted:
                color = GREEN
            elif game.board[row][col].color == "White":
                color = WHITE
            else:
                color = BLACK
            pygame.draw.rect(screen, color, (col * SQUARE_SIZE, row * SQUARE_SIZE, SQUARE_SIZE, SQUARE_SIZE))
            border_color = (0, 0, 0) 
            pygame.draw.rect(
                screen,
                border_color,
                (col * SQUARE_SIZE, row * SQUARE_SIZE, SQUARE_SIZE, SQUARE_SIZE),
                width=2,  
            )

def draw_pieces(game):
    for row in range(8):
        for col in range(8):
            square = game.board[row][col]
            piece = square.piece
            if piece: 
                if (piece.isAttacking and game.board[row][col].highlighted is False) or (isinstance(piece, King) and piece.underAttack):
                    pygame.draw.rect(screen, RED, (col * SQUARE_SIZE, row * SQUARE_SIZE, SQUARE_SIZE, SQUARE_SIZE))
                    border_color = (0, 0, 0) 
                    pygame.draw.rect(
                        screen,
                        border_color,
                        (col * SQUARE_SIZE, row * SQUARE_SIZE, SQUARE_SIZE, SQUARE_SIZE),
                        width=2,  
                    )
                imp = pygame.image.load(piece.image).convert_alpha()
                piece_image = pygame.transform.scale(imp, (SQUARE_SIZE, SQUARE_SIZE))
                screen.blit(piece_image, (col * SQUARE_SIZE, row * SQUARE_SIZE))


def main():
    game = Game()
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                mouse_x, mouse_y = event.pos
                col, row = mouse_x // SQUARE_SIZE, mouse_y // SQUARE_SIZE
                piece = game.board[row][col].piece
                if game.board[row][col].highlighted: #if player selected sqaure to move their piece to
                    piece = game.board[game.curr_player.selected_piece[0]][game.curr_player.selected_piece[1]].piece 
                    game.board[game.curr_player.selected_piece[0]][game.curr_player.selected_piece[1]].piece = None
                    game.board[row][col].piece = piece
                    game.board[row][col].piece.row = row
                    game.board[row][col].piece.col = col
                    game.curr_player.reset_possible_moves(game.board)
                    game.curr_player.reset_selected_piece()
                    game.switch_player()
                    game.remove_pieces_in_action()
                    game.curr_player.king.check_if_under_attack(game, game.board, game.curr_player)
                elif game.board[row][col].piece is not None and game.board[row][col].piece.color == game.curr_player.color and [row, col] != game.curr_player.selected_piece: #player selects a piece to move
                    game.curr_player.reset_possible_moves(game.board)
                    game.curr_player.select_piece(row, col)
                    piece = game.board[row][col].piece
                    piece.valid_moves(game.board, game.curr_player)
                    for square in game.curr_player.possible_moves:
                        game.board[square[0]][square[1]].highlighted = True
        draw_board(game)
        draw_pieces(game)
        pygame.display.flip()
    pygame.quit() 

if __name__ == '__main__':
    main()