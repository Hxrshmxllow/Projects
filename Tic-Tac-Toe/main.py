import pygame
from board import *

WINDOW_SIZE = 600
GRID_SIZE = 3
SQUARE_SIZE = WINDOW_SIZE // GRID_SIZE
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)

pygame.init()
screen = pygame.display.set_mode((WINDOW_SIZE, WINDOW_SIZE))
pygame.display.set_caption("Tic-Tac-Toe Board")

def draw_board(board):
    for row in range(GRID_SIZE):
        for col in range(GRID_SIZE):
            pygame.draw.rect(screen, WHITE, (col * SQUARE_SIZE, row * SQUARE_SIZE, SQUARE_SIZE, SQUARE_SIZE))
            pygame.draw.rect(
                screen,
                BLACK,
                (col * SQUARE_SIZE, row * SQUARE_SIZE, SQUARE_SIZE, SQUARE_SIZE),
                width=2,  
            )
            img = board.get_sqaure_img(row, col)
            if img is not None:
                imp = pygame.image.load(img).convert_alpha()
                piece_image = pygame.transform.scale(imp, (SQUARE_SIZE, SQUARE_SIZE))
                screen.blit(piece_image, (col * SQUARE_SIZE, row * SQUARE_SIZE))
        
def main():
    x = Player(1)
    o = Player(-1)
    game = Game(x, o)
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                mouse_x, mouse_y = event.pos
                col, row = mouse_x // SQUARE_SIZE, mouse_y // SQUARE_SIZE
                sqaure = game.board[row][col]
                if sqaure == 0:
                    game.change_square(row, col)
                    game.switch_curr_player()
        draw_board(game)
        if game.check_for_win():
            type = game.win[0]
            num = game.win[1]
            if type == "row":
                pygame.draw.line(screen, BLACK, (0, num * SQUARE_SIZE + SQUARE_SIZE // 2), (GRID_SIZE * SQUARE_SIZE, SQUARE_SIZE + SQUARE_SIZE // 2), width=10)
            elif type == 'col':
                    pygame.draw.line(screen, BLACK, (num * SQUARE_SIZE + SQUARE_SIZE // 2, 0), (num * SQUARE_SIZE + SQUARE_SIZE // 2, GRID_SIZE * SQUARE_SIZE), width=10)
            elif num == 0:
                    pygame.draw.line(screen, BLACK, (0, 0), (GRID_SIZE * SQUARE_SIZE, GRID_SIZE * SQUARE_SIZE), width=10)
            else:
                    pygame.draw.line(screen, BLACK, (GRID_SIZE * SQUARE_SIZE, 0), (0, GRID_SIZE * SQUARE_SIZE), width=10)
        pygame.display.flip()
    pygame.quit() 

if __name__ == '__main__':
    main()