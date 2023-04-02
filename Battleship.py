import sys
import random
import pygame
from pygame.locals import *
def generate_board():
    board = [[" " for _ in range(10)] for _ in range(10)]
    return board

def print_board(board):
    print("  1 2 3 4 5 6 7 8 9 10")
    for i, row in enumerate(board):
        print(chr(65 + i) + " " + " ".join(row))

def place_ships(board, ship_sizes):
    for ship_size in ship_sizes:
        while True:
            row, col, orientation = random.randint(0, 9), random.randint(0, 9), random.choice(["horizontal", "vertical"])
            if orientation == "horizontal" and col + ship_size <= 10 and all(board[row][col + i] == " " for i in range(ship_size)):
                for i in range(ship_size):
                    board[row][col + i] = "S"
                break
            elif orientation == "vertical" and row + ship_size <= 10 and all(board[row + i][col] == " " for i in range(ship_size)):
                for i in range(ship_size):
                    board[row + i][col] = "S"
                break

def get_move():
    while True:
        try:
            move = input("Enter your move (e.g., A1): ").upper()
            row, col = ord(move[0]) - 65, int(move[1:]) - 1
            if 0 <= row < 10 and 0 <= col < 10:
                return row, col
        except ValueError:
            pass
        print("Invalid move. Please try again.")

def play_game():
    ship_sizes = [5, 4, 3, 3, 2]
    player_board = generate_board()
    enemy_board = generate_board()
    place_ships(enemy_board, ship_sizes)

    remaining_ships = len(ship_sizes)
    hits, misses = 0, 0

    while remaining_ships > 0:
        print_board(player_board)
        row, col = get_move()

        if enemy_board[row][col] == "S":
            print("Hit!")
            player_board[row][col] = "X"
            enemy_board[row][col] = " "
            hits += 1
        else:
            print("Miss.")
            player_board[row][col] = "O"
            misses += 1

        if hits == sum(ship_sizes):
            print_board(player_board)
            print(f"Congratulations! You've sunk all the enemy ships in {hits + misses} moves.")
            break

# Pygame specific functions and variables
pygame.init()
screen = pygame.display.set_mode((640, 480))
pygame.display.set_caption("Battleship")

WHITE = (255, 255, 255)
BLUE = (0, 0, 255)
RED = (255, 0, 0)
BLACK = (0, 0, 0)

def draw_board(surface, board, cell_size, top_left):
    for row in range(10):
        for col in range(10):
            rect = pygame.Rect(top_left[0] + col * cell_size, top_left[1] + row * cell_size, cell_size, cell_size)
            pygame.draw.rect(surface, WHITE, rect, 1)
            if board[row][col] == "X":
                pygame.draw.line(surface, RED, rect.topleft, rect.bottomright, 3)
                pygame.draw.line(surface, RED, rect.topright, rect.bottomleft, 3)
            elif board[row][col] == "O":
                pygame.draw.circle(surface, BLUE, rect.center, cell_size // 2 - 4, 2)

def game_loop():
    ship_sizes = [5, 4, 3, 3, 2]
    player_board = generate_board()
    enemy_board = generate_board()
    place_ships(enemy_board, ship_sizes)

    remaining_ships = len(ship_sizes)
    hits, misses = 0, 0
    cell_size = 40
    top_left = (80, 80)

    while True:
        screen.fill(BLACK)
        draw_board(screen, player_board, cell_size, top_left)
        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()

            if event.type == MOUSEBUTTONDOWN and event.button == 1:
                x, y = event.pos
                col = (x - top_left[0]) // cell_size
                row = (y - top_left[1]) // cell_size

                if 0 <= row < 10 and 0 <= col < 10:
                    if enemy_board[row][col] == "S":
                        print("Hit!")
                        player_board[row][col] = "X"
                        enemy_board[row][col] = " "
                        hits += 1
                    else:
                        print("Miss.")
                        player_board[row][col] = "O"
                        misses += 1

                    if hits == sum(ship_sizes):
                        print("Congratulations! You've sunk all the enemy ships!")
                        pygame.time.delay(3000)
                        return

if __name__ == "__main__":
    game_loop()