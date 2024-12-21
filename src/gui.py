import random

import pygame
import sys
from board import Board
from game import Game, ComputerRandomMoves, ComputerAIMoves


class ObstructionGame:
    def __init__(self):
        pygame.init()
        self.WINDOW_WIDTH, self.WINDOW_HEIGHT = 1280, 720  # Default resolution
        self.screen = pygame.display.set_mode((self.WINDOW_WIDTH, self.WINDOW_HEIGHT), pygame.RESIZABLE)
        pygame.display.set_caption("Obstruction Game")
        self.font = pygame.font.Font(None, 36)
        self.title_font = pygame.font.Font(None, 80)
        self.board_size = 6
        self.difficulty = "easy"
        self.selected_board_size = 6  # Default selected size
        self.selected_difficulty = "easy"  # Default selected difficulty
        self.board = None
        self.game = None
        self.user_turn = True
        self.CELL_SIZE = 0

    def draw_text(self, text, x, y, color=(0, 0, 0), center=False):
        """Helper to draw text on the screen."""
        rendered_text = self.font.render(text, True, color)
        text_rect = rendered_text.get_rect()
        if center:
            text_rect.center = (x, y)
        else:
            text_rect.topleft = (x, y)
        self.screen.blit(rendered_text, text_rect)

    def draw_title(self):
        """Draw the title of the game, centered at the top."""
        # Dynamically calculate the center based on current window size
        window_width = self.screen.get_width()
        title_text = "Welcome to Obstruction!"
        rendered_title = self.title_font.render(title_text, True, (0, 0, 0))
        title_rect = rendered_title.get_rect(center=(window_width // 2, 80))
        self.screen.blit(rendered_title, title_rect)

    def draw_menu_background(self):
        """Draws a resizable pixelated background with flowers, grass, sun, and clouds."""
        window_width = self.screen.get_width()
        window_height = self.screen.get_height()
        self.screen.fill((255, 255, 204))

        # Grass Area (Bottom of the Screen)
        grass_height = window_height // 4

        c = 4
        for x in range(0, window_width, 20):
            if c == 4:
                for y in range(window_height - grass_height - 60, window_height - grass_height, 20):
                    pygame.draw.rect(self.screen, (63, 210, 63), (x, y, 20, 20))  # Green grass
            if c == 3 or c == 1:
                for y in range(window_height - grass_height - 40, window_height - grass_height, 20):
                    pygame.draw.rect(self.screen, (63, 210, 63), (x, y, 20, 20))  # Green grass
            if c == 2:
                pygame.draw.rect(self.screen, (63, 210, 63), (x, window_height - grass_height - 20, 20, 20))  # Green grass
            c -= 1
            if c == 0:
                c = 4

        for x in range(0, window_width, 20):
            for y in range(window_height - grass_height, window_height, 20):
                pygame.draw.rect(self.screen, (63, 210, 63), (x, y, 20, 20))  # Green grass

        # Flower 1: Pink Flower (Left Side)
        flower1_x = 120  # X-coordinate for flower 1
        flower1_y = window_height - grass_height - 200  # Y-coordinate for flower top

        # Stem
        for y in range(flower1_y + 40, window_height - grass_height - 20, 20):
            pygame.draw.rect(self.screen, (34, 139, 34), (flower1_x, y, 20, 20))  # Green stem
            # pygame.draw.rect(self.screen, (0, 0, 0), (flower1_x, y, 20, 20), 1)  # Outline

        # Leaves
        pygame.draw.rect(self.screen, (34, 139, 34), (flower1_x - 20, flower1_y + 80, 20, 20))  # Left leaf
        pygame.draw.rect(self.screen, (34, 139, 34), (flower1_x + 20, flower1_y + 100, 20, 20))  # Right leaf
        # pygame.draw.rect(self.screen, (0, 0, 0), (flower1_x - 20, flower1_y + 80, 20, 20),
        #                  1)  # Outline for left leaf
        # pygame.draw.rect(self.screen, (0, 0, 0), (flower1_x + 20, flower1_y + 100, 20, 20),
        #                  1)  # Outline for right leaf

        # Center
        pygame.draw.rect(self.screen, (255, 255, 0), (flower1_x, flower1_y, 20, 20))  # Yellow center
        pygame.draw.rect(self.screen, (0, 0, 0), (flower1_x, flower1_y, 20, 20), 1)  # Outline

        # Petals
        petal_offsets = [(-20, -20), (20, -20), (-20, 20), (20, 20), (0, -40), (0, 40), (20, 0), (-40, 0), (40, 0), (-20, 0), (0, 20), (0, -20)]
        for offset in petal_offsets:
            petal_x = flower1_x + offset[0]
            petal_y = flower1_y + offset[1]
            pygame.draw.rect(self.screen, (255, 105, 180), (petal_x, petal_y, 20, 20))  # Pink petal
            # pygame.draw.rect(self.screen, (0, 0, 0), (petal_x, petal_y, 20, 20), 1)  # Outline

        # Flower 2: Red Flower (Right Side)
        flower2_x = window_width - 120  # X-coordinate for flower 2
        flower2_y = window_height - grass_height - 200  # Y-coordinate for flower top

        # Stem
        for y in range(flower2_y + 40, window_height - grass_height - 20, 20):
            pygame.draw.rect(self.screen, (34, 139, 34), (flower2_x, y, 20, 20))  # Green stem

        # Leaves
        pygame.draw.rect(self.screen, (34, 139, 34), (flower2_x - 20, flower2_y + 80, 20, 20))  # Left leaf
        pygame.draw.rect(self.screen, (34, 139, 34), (flower2_x + 20, flower2_y + 100, 20, 20))  # Right leaf

        # Center
        pygame.draw.rect(self.screen, (255, 255, 0), (flower2_x, flower2_y, 20, 20))  # Yellow center
        pygame.draw.rect(self.screen, (0, 0, 0), (flower2_x, flower2_y, 20, 20), 1)  # Outline

        # Petals
        for offset in petal_offsets:
            petal_x = flower2_x + offset[0]
            petal_y = flower2_y + offset[1]
            pygame.draw.rect(self.screen, (255, 0, 0), (petal_x, petal_y, 20, 20))  # Red petal


        # Sun (Top-right Corner)
        sun_size = window_width // 15
        sun_x = window_width - sun_size - 35
        sun_y = 20
        for x in range(sun_x, sun_x + sun_size, 20):
            for y in range(sun_y, sun_y + sun_size, 20):
                pygame.draw.rect(self.screen, (255, 223, 0), (x, y, 20, 20))  # Yellow sun


        # # Clouds (Top-left Corner)
        # cloud_start_x = 50
        # cloud_start_y = 50
        # for offset in [(0, 0), (20, 0), (40, 0), (10, 20), (30, 20)]:
        #     x = cloud_start_x + offset[0]
        #     y = cloud_start_y + offset[1]
        #     pygame.draw.rect(self.screen, (255, 255, 255), (x, y, 20, 20))  # White cloud

    def draw_main_menu(self, clicked_button=None):
        """Draw the main menu with board size and difficulty selection."""
        # self.screen.fill((255, 255, 255))
        self.draw_menu_background()
        self.draw_title()

        # Get current window dimensions for dynamic positioning
        window_width = self.screen.get_width()
        window_height = self.screen.get_height()
        margin_x = window_width // 6
        margin_y = window_height // 3
        button_width, button_height = 100, 50

        # Draw board size options
        self.draw_text("Choose Board Size:", margin_x, margin_y, (0, 0, 0))
        for i, size in enumerate(range(4, 9)):
            button_x = margin_x + 300 + i * (button_width + 10)
            button_y = margin_y - 10
            # Highlight the selected board size
            color = (252, 155, 242) if self.selected_board_size == size else (200, 200, 200)
            pygame.draw.rect(self.screen, color, (button_x, button_y, button_width, button_height))
            self.draw_text(f"{size}x{size}", button_x + button_width // 2, button_y + button_height // 2, (0, 0, 0),
                           center=True)

        # Draw difficulty options
        self.draw_text("Choose Difficulty:", margin_x, margin_y + 100, (0, 0, 0))
        difficulties = ["easy", "hard"]
        for i, diff in enumerate(difficulties):
            button_x = margin_x + 300 + i * (button_width + 10)
            button_y = margin_y + 100 - 10
            # Highlight the selected difficulty
            color = (255, 117, 117) if self.selected_difficulty == diff else (200, 200, 200)
            pygame.draw.rect(self.screen, color, (button_x, button_y, button_width, button_height))
            self.draw_text(diff.capitalize(), button_x + button_width // 2, button_y + button_height // 2, (0, 0, 0),
                           center=True)

        # Draw "Let's Play!" button
        button_x = window_width // 2 - 100
        button_y = window_height - 150
        button_color = (100, 255, 100) if clicked_button == "play" else (200, 200, 200)
        pygame.draw.rect(self.screen, button_color, (button_x, button_y, 200, 80))
        self.draw_text("Let's Play!", button_x + 100, button_y + 40, (0, 0, 0), center=True)

        pygame.display.flip()

    def handle_resize_event(self):
        """Recalculate positions after a resize event."""
        # Re-render the main menu with new dimensions
        self.draw_main_menu()

    def handle_main_menu_events(self):
        """Handle clicks on the main menu."""
        window_width = self.screen.get_width()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                x, y = event.pos

                # Check board size selection
                for i, size in enumerate(range(4, 9)):
                    button_x = window_width // 8 + 300 + i * (100 + 10)
                    button_y = 200
                    if button_x <= x <= button_x + 100 and button_y <= y <= button_y + 50:
                        self.selected_board_size = size  # Update selected board size
                        self.draw_main_menu()  # Redraw menu
                        return False

                # Check difficulty selection
                difficulties = ["easy", "hard"]
                for i, diff in enumerate(difficulties):
                    button_x = window_width // 8 + 300 + i * (100 + 10)
                    button_y = 300
                    if button_x <= x <= button_x + 100 and button_y <= y <= button_y + 50:
                        self.selected_difficulty = diff  # Update selected difficulty
                        self.draw_main_menu()  # Redraw menu
                        return False

                # Check "Let's Play!" button
                button_x = window_width // 2 - 100
                button_y = self.screen.get_height() - 150
                if button_x <= x <= button_x + 200 and button_y <= y <= button_y + 80:
                    self.board_size = self.selected_board_size  # Apply selected board size
                    self.difficulty = self.selected_difficulty  # Apply selected difficulty
                    return True  # Proceed to game

        return False


    def setup_game(self):
        """Set up the game based on menu choices."""
        window_width = self.screen.get_width()
        window_height = self.screen.get_height()
        self.board = Board(self.board_size)
        self.CELL_SIZE = min(window_width, window_height - 100) // self.board_size
        if self.difficulty == "easy":
            computer_player = ComputerRandomMoves()
        else:
            computer_player = ComputerAIMoves()
        self.game = Game(self.board, computer_player)

    def draw_game_screen(self):
        """Draw the game board and UI elements."""
        window_width = self.screen.get_width()
        window_height = self.screen.get_height()
        self.screen.fill((255, 255, 204))

        # Title
        title = f"You are playing on a {self.board_size} x {self.board_size} board, difficulty: {self.difficulty}"
        self.draw_text(title, window_width // 2, window_height // 30, (0, 0, 0), center=True)

        # Draw the board
        board_start_x = (window_width - self.CELL_SIZE * self.board_size) // 2
        board_start_y = (window_height - self.CELL_SIZE * self.board_size) // 2
        for row in range(self.board_size):
            for col in range(self.board_size):
                rect = pygame.Rect(board_start_x + col * self.CELL_SIZE, board_start_y + row * self.CELL_SIZE,
                                   self.CELL_SIZE, self.CELL_SIZE)
                pygame.draw.rect(self.screen, (0, 0, 0), rect, 1)

                # Draw symbols
                symbol = self.board.get_board()[row][col]
                if symbol == 'X':
                    self.draw_text('X', rect.centerx, rect.centery, (255, 0, 0), center=True)
                elif symbol == 'O':
                    self.draw_text('O', rect.centerx, rect.centery, (0, 0, 255), center=True)
                elif symbol == '/':
                    self.draw_text('/', rect.centerx, rect.centery, (0, 255, 0), center=True)

        # Flower 1: Pink Flower (Left Side)
        flower1_x = 120  # X-coordinate for flower 1
        flower1_y = window_height - 200  # Y-coordinate for flower top

        # Stem
        for y in range(flower1_y + 40, window_height - 20, 20):
            pygame.draw.rect(self.screen, (34, 139, 34), (flower1_x, y, 20, 20))  # Green stem
            # pygame.draw.rect(self.screen, (0, 0, 0), (flower1_x, y, 20, 20), 1)  # Outline

        # Leaves
        pygame.draw.rect(self.screen, (34, 139, 34), (flower1_x - 20, flower1_y + 80, 20, 20))  # Left leaf
        pygame.draw.rect(self.screen, (34, 139, 34), (flower1_x + 20, flower1_y + 100, 20, 20))  # Right leaf
        # pygame.draw.rect(self.screen, (0, 0, 0), (flower1_x - 20, flower1_y + 80, 20, 20),
        #                  1)  # Outline for left leaf
        # pygame.draw.rect(self.screen, (0, 0, 0), (flower1_x + 20, flower1_y + 100, 20, 20),
        #                  1)  # Outline for right leaf

        # Center
        pygame.draw.rect(self.screen, (255, 255, 0), (flower1_x, flower1_y, 20, 20))  # Yellow center
        pygame.draw.rect(self.screen, (0, 0, 0), (flower1_x, flower1_y, 20, 20), 1)  # Outline

        # Petals
        petal_offsets = [(-20, -20), (20, -20), (-20, 20), (20, 20), (0, -40), (0, 40), (20, 0), (-40, 0), (40, 0),
                         (-20, 0), (0, 20), (0, -20)]
        for offset in petal_offsets:
            petal_x = flower1_x + offset[0]
            petal_y = flower1_y + offset[1]
            pygame.draw.rect(self.screen, (255, 105, 180), (petal_x, petal_y, 20, 20))  # Pink petal
            # pygame.draw.rect(self.screen, (0, 0, 0), (petal_x, petal_y, 20, 20), 1)  # Outline

        # Flower 2: Red Flower (Right Side)
        flower2_x = window_width - 120  # X-coordinate for flower 2
        flower2_y = window_height - 200  # Y-coordinate for flower top

        # Stem
        for y in range(flower2_y + 40, window_height - 20, 20):
            pygame.draw.rect(self.screen, (34, 139, 34), (flower2_x, y, 20, 20))  # Green stem

        # Leaves
        pygame.draw.rect(self.screen, (34, 139, 34), (flower2_x - 20, flower2_y + 80, 20, 20))  # Left leaf
        pygame.draw.rect(self.screen, (34, 139, 34), (flower2_x + 20, flower2_y + 100, 20, 20))  # Right leaf

        # Center
        pygame.draw.rect(self.screen, (255, 255, 0), (flower2_x, flower2_y, 20, 20))  # Yellow center
        pygame.draw.rect(self.screen, (0, 0, 0), (flower2_x, flower2_y, 20, 20), 1)  # Outline

        # Petals
        for offset in petal_offsets:
            petal_x = flower2_x + offset[0]
            petal_y = flower2_y + offset[1]
            pygame.draw.rect(self.screen, (255, 0, 0), (petal_x, petal_y, 20, 20))  # Red petal


        for x in range(0, window_width, 20):
            pygame.draw.rect(self.screen, (63, 210, 63), (x, window_height - 20, 20, 20))  # Green grass


        pygame.display.flip()

    def make_user_move(self, row, column, symbol):
        try:
            self.board.update_position(row, column, symbol)
        except Exception as e:
            print(f"Error in make_user_move: {e}")
            raise


    def handle_game_events(self):
        """Handle events during the game."""
        window_width = self.screen.get_width()
        window_height = self.screen.get_height()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif self.user_turn and event.type == pygame.MOUSEBUTTONDOWN:
                board_start_x = (window_width - self.CELL_SIZE * self.board_size) // 2
                board_start_y = (window_height - self.CELL_SIZE * self.board_size) // 2
                x, y = event.pos
                col = (x - board_start_x) // self.CELL_SIZE + 1
                row = (y - board_start_y) // self.CELL_SIZE + 1
                try:
                    self.game.make_user_move(row, col, 'X')
                    self.user_turn = False
                except ValueError:
                    pass

    def display_victory_screen(self, message):
        """Show a victory screen with confetti."""
        confetti = []  # Store confetti particles
        self.screen.fill((255, 255, 204))
        window_width = self.screen.get_width()
        window_height = self.screen.get_height()
        clock = pygame.time.Clock()

        # Generate initial confetti
        for _ in range(100):  # Adjust number of confetti particles
            confetti.append({
                "x": random.randint(0, window_width),
                "y": random.randint(-window_height, 0),
                "color": (random.randint(0, 255), random.randint(0, 255), random.randint(0, 255)),
                "speed": random.randint(2, 7),
                "size": random.randint(5, 15),
            })

        # Victory screen loop
        start_time = pygame.time.get_ticks()
        while pygame.time.get_ticks() - start_time < 5000:  # Show for 5 seconds
            self.screen.fill((255, 255, 204))

            # Draw the victory message
            large_font = pygame.font.Font(None, 100)
            rendered_text = large_font.render(message, True, (0, 0, 0))
            text_rect = rendered_text.get_rect(center=(window_width // 2, window_height // 2))
            self.screen.blit(rendered_text, text_rect)

            # Update and draw confetti
            for particle in confetti:
                pygame.draw.rect(
                    self.screen,
                    particle["color"],
                    (particle["x"], particle["y"], particle["size"], particle["size"])
                )
                particle["y"] += particle["speed"]  # Move confetti down
                if particle["y"] > window_height:  # Reset confetti to the top
                    particle["y"] = random.randint(-window_height, 0)
                    particle["x"] = random.randint(0, window_width)
                    particle["color"] = (random.randint(0, 255), random.randint(0, 255), random.randint(0, 255))

            pygame.display.flip()
            clock.tick(30)

    def run_game(self):
        """Main game loop."""
        window_width = self.screen.get_width()
        window_height = self.screen.get_height()
        clock = pygame.time.Clock()
        while True:
            try:
                # Handle user events
                self.handle_game_events()
                status = self.board.get_board_status()

                # If it's the AI's turn, make its move
                if not self.user_turn and status == "playing":
                    pygame.time.wait(500)  # AI delay
                    self.game.make_computer_move()
                    self.user_turn = True
                    self.draw_game_screen()  # Ensure board is updated after the AI's move

                # Check the game status
                status = self.board.get_board_status()
                if status != "playing":
                    # Render the final board state
                    self.draw_game_screen()

                    # Display the win/lose message
                    message = "You Win!" if status == "human" else "Computer Wins!"
                    self.display_victory_screen(message)
                    pygame.quit()
                    sys.exit()

                # Render the current game state
                self.draw_game_screen()
                clock.tick(30)

            except Exception as e:
                print(f"An error occurred: {e}")
                pygame.quit()
                sys.exit()

    def main(self):
        """Run the game."""

        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                elif event.type == pygame.VIDEORESIZE:
                    self.WINDOW_WIDTH, self.WINDOW_HEIGHT = event.w, event.h
                    self.screen = pygame.display.set_mode((self.WINDOW_WIDTH, self.WINDOW_HEIGHT), pygame.RESIZABLE)
                    self.handle_resize_event()

            self.draw_main_menu()
            if self.handle_main_menu_events():
                self.setup_game()
                self.run_game()

if __name__ == "__main__":
    game = ObstructionGame()
    game.main()
