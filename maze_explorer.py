import os
os.environ["PYGAME_HIDE_SUPPORT_PROMPT"] = "1"
import pygame
import random
import sys
import time
from highscores import get_high_score, save_high_score

GAME_NAME = "maze_explorer"

# Initialize pygame
pygame.init()

# Screen settings
CELL_SIZE = 40
MAZE_WIDTH, MAZE_HEIGHT = 15, 15
WIDTH, HEIGHT = CELL_SIZE * MAZE_WIDTH, CELL_SIZE * MAZE_HEIGHT + 50  # Extra bar at top
MAZE_OFFSET_Y = 50  # Maze drawn below HUD
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Maze Explorer")
_icon_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "icon.png")
if os.path.exists(_icon_path):
    pygame.display.set_icon(pygame.image.load(_icon_path))

# Colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GREEN = (0, 200, 0)
RED = (200, 0, 0)
BLUE = (0, 0, 200)
GOLD = (255, 215, 0)
GRAY = (100, 100, 100)
DARK_RED = (180, 0, 0)
LIGHT_RED = (255, 50, 50)
DARK_GREEN = (0, 120, 0)
LIGHT_GREEN = (0, 255, 0)

# Game variables
clock = pygame.time.Clock()
font = pygame.font.SysFont(None, 36)
small_font = pygame.font.SysFont(None, 26)

class Button:
    def __init__(self, x, y, width, height, text, action=None, colors=(DARK_GREEN, LIGHT_GREEN)):
        self.rect = pygame.Rect(x, y, width, height)
        self.text = text
        self.action = action
        self.is_hovered = False
        self.colors = colors  # (normal_color, hover_color)
    
    def draw(self):
        # Draw the button
        color = self.colors[1] if self.is_hovered else self.colors[0]
        pygame.draw.rect(screen, color, self.rect, border_radius=10)
        pygame.draw.rect(screen, WHITE, self.rect, 2, border_radius=10)
        
        # Draw the text
        text_surf = small_font.render(self.text, True, WHITE)
        text_rect = text_surf.get_rect(center=self.rect.center)
        screen.blit(text_surf, text_rect)
    
    def check_hover(self, mouse_pos):
        self.is_hovered = self.rect.collidepoint(mouse_pos)
        return self.is_hovered
    
    def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            if self.is_hovered and self.action:
                return self.action()
        return False

class Cell:
    def __init__(self, row, col):
        self.row = row
        self.col = col
        self.visited = False
        self.walls = {"top": True, "right": True, "bottom": True, "left": True}
    
    def draw(self):
        x, y = self.col * CELL_SIZE, self.row * CELL_SIZE + MAZE_OFFSET_Y
        
        if self.visited:
            pygame.draw.rect(screen, BLACK, (x, y, CELL_SIZE, CELL_SIZE))
            
        if self.walls["top"]:
            pygame.draw.line(screen, WHITE, (x, y), (x + CELL_SIZE, y), 2)
        if self.walls["right"]:
            pygame.draw.line(screen, WHITE, (x + CELL_SIZE, y), (x + CELL_SIZE, y + CELL_SIZE), 2)
        if self.walls["bottom"]:
            pygame.draw.line(screen, WHITE, (x, y + CELL_SIZE), (x + CELL_SIZE, y + CELL_SIZE), 2)
        if self.walls["left"]:
            pygame.draw.line(screen, WHITE, (x, y), (x, y + CELL_SIZE), 2)

def remove_wall(current, next_cell):
    # Calculate which walls need to be removed
    dx = current.col - next_cell.col
    dy = current.row - next_cell.row
    
    if dx == 1:  # current is to the right of next_cell
        current.walls["left"] = False
        next_cell.walls["right"] = False
    elif dx == -1:  # current is to the left of next_cell
        current.walls["right"] = False
        next_cell.walls["left"] = False
    if dy == 1:  # current is below next_cell
        current.walls["top"] = False
        next_cell.walls["bottom"] = False
    elif dy == -1:  # current is above next_cell
        current.walls["bottom"] = False
        next_cell.walls["top"] = False

def generate_maze():
    # Create grid of cells
    grid = [[Cell(row, col) for col in range(MAZE_WIDTH)] for row in range(MAZE_HEIGHT)]
    
    # Pick a random starting cell
    current = grid[0][0]
    current.visited = True
    stack = [current]
    
    # Continue until all cells have been visited
    while stack:
        current = stack[-1]
        # Get unvisited neighbors
        neighbors = []
        row, col = current.row, current.col
        
        # Check each direction
        if row > 0 and not grid[row - 1][col].visited:
            neighbors.append(grid[row - 1][col])
        if col < MAZE_WIDTH - 1 and not grid[row][col + 1].visited:
            neighbors.append(grid[row][col + 1])
        if row < MAZE_HEIGHT - 1 and not grid[row + 1][col].visited:
            neighbors.append(grid[row + 1][col])
        if col > 0 and not grid[row][col - 1].visited:
            neighbors.append(grid[row][col - 1])
            
        if neighbors:
            # Choose a random neighbor
            next_cell = random.choice(neighbors)
            next_cell.visited = True
            
            # Remove walls between current cell and chosen neighbor
            remove_wall(current, next_cell)
            
            # Push the chosen cell to the stack
            stack.append(next_cell)
        else:
            # Backtrack
            stack.pop()
    
    return grid

def can_move(player, direction, grid):
    row, col = player
    if direction == "up" and not grid[row][col].walls["top"]:
        return True
    if direction == "right" and not grid[row][col].walls["right"]:
        return True
    if direction == "down" and not grid[row][col].walls["bottom"]:
        return True
    if direction == "left" and not grid[row][col].walls["left"]:
        return True
    return False

def reset_game():
    grid = generate_maze()
    player = [0, 0]
    return grid, player, False, time.time(), 0

def draw_hud(moves, elapsed, best_score):
    pygame.draw.rect(screen, (0, 0, 40), (0, 0, WIDTH, MAZE_OFFSET_Y))
    pygame.draw.line(screen, GRAY, (0, MAZE_OFFSET_Y - 1), (WIDTH, MAZE_OFFSET_Y - 1), 1)
    moves_text = small_font.render(f"Moves: {moves}", True, WHITE)
    screen.blit(moves_text, (10, 14))
    time_text = small_font.render(f"Time: {elapsed:.1f}s", True, WHITE)
    screen.blit(time_text, (WIDTH // 2 - time_text.get_width() // 2, 14))
    if best_score > 0:
        best_text = small_font.render(f"Best: {best_score} moves", True, GOLD)
        screen.blit(best_text, (WIDTH - best_text.get_width() - 10, 14))

def main():
    grid = generate_maze()
    player = [0, 0]
    goal = [MAZE_HEIGHT - 1, MAZE_WIDTH - 1]
    win = False
    start_time = time.time()
    moves = 0
    best_score = get_high_score(GAME_NAME)
    new_best = False

    button_width = 180
    button_height = 50
    win_overlay_y = HEIGHT // 2

    def do_restart():
        nonlocal grid, player, win, start_time, moves, new_best
        grid, player, win, start_time, moves = reset_game()
        new_best = False
        return True

    restart_button = Button(WIDTH//2 - button_width - 10, win_overlay_y + 70,
                            button_width, button_height, "Restart", do_restart)
    quit_button = Button(WIDTH//2 + 10, win_overlay_y + 70,
                         button_width, button_height, "Quit Game",
                         lambda: pygame.event.post(pygame.event.Event(pygame.QUIT)),
                         colors=(DARK_RED, LIGHT_RED))

    running = True
    while running:
        mouse_pos = pygame.mouse.get_pos()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    running = False

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_r and win:
                    do_restart()
                elif not win:
                    moved = False
                    if event.key == pygame.K_UP and can_move(player, "up", grid):
                        player[0] -= 1; moved = True
                    elif event.key == pygame.K_RIGHT and can_move(player, "right", grid):
                        player[1] += 1; moved = True
                    elif event.key == pygame.K_DOWN and can_move(player, "down", grid):
                        player[0] += 1; moved = True
                    elif event.key == pygame.K_LEFT and can_move(player, "left", grid):
                        player[1] -= 1; moved = True
                    if moved:
                        moves += 1

            if win:
                if restart_button.handle_event(event):
                    pass
                quit_button.handle_event(event)

        if player == goal and not win:
            win = True
            new_best = save_high_score(GAME_NAME, moves)
            best_score = get_high_score(GAME_NAME)

        elapsed = (time.time() - start_time) if not win else elapsed

        # Drawing
        screen.fill(BLACK)

        # HUD
        draw_hud(moves, elapsed, best_score)

        # Maze
        for row in grid:
            for cell in row:
                cell.draw()

        # Goal
        goal_x = goal[1] * CELL_SIZE + CELL_SIZE // 2
        goal_y = goal[0] * CELL_SIZE + CELL_SIZE // 2 + MAZE_OFFSET_Y
        pygame.draw.circle(screen, GOLD, (goal_x, goal_y), CELL_SIZE // 3)

        # Player
        player_x = player[1] * CELL_SIZE + CELL_SIZE // 2
        player_y = player[0] * CELL_SIZE + CELL_SIZE // 2 + MAZE_OFFSET_Y
        pygame.draw.circle(screen, RED, (player_x, player_y), CELL_SIZE // 3)

        if win:
            overlay = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)
            overlay.fill((0, 0, 0, 180))
            screen.blit(overlay, (0, 0))

            win_text = font.render("You Win!", True, GREEN)
            screen.blit(win_text, win_text.get_rect(center=(WIDTH // 2, win_overlay_y - 20)))

            stats_text = small_font.render(f"{moves} moves  |  {elapsed:.1f}s", True, WHITE)
            screen.blit(stats_text, stats_text.get_rect(center=(WIDTH // 2, win_overlay_y + 20)))

            if new_best:
                nb_text = small_font.render("New Best!", True, GOLD)
                screen.blit(nb_text, nb_text.get_rect(center=(WIDTH // 2, win_overlay_y + 44)))

            r_text = small_font.render("Press R to restart", True, WHITE)
            screen.blit(r_text, r_text.get_rect(center=(WIDTH // 2, win_overlay_y + 140)))

            restart_button.check_hover(mouse_pos)
            quit_button.check_hover(mouse_pos)
            restart_button.draw()
            quit_button.draw()

        pygame.display.flip()
        clock.tick(60)

    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main()
