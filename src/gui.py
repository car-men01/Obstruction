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
        title_text = "Welcome to Obstruction"
        rendered_title = self.title_font.render(title_text, True, (0, 0, 0))
        title_rect = rendered_title.get_rect(center=(window_width // 2, 80))
        self.screen.blit(rendered_title, title_rect)

    # def draw_main_menu(self, clicked_button=None):
    #     """Draw the main menu with board size and difficulty selection."""
    #     self.screen.fill((255, 255, 255))
    #     self.draw_title()
    #
    #     # Get current window dimensions for dynamic positioning
    #     window_width = self.screen.get_width()
    #     window_height = self.screen.get_height()
    #     margin = window_width // 8
    #     button_width, button_height = 100, 50
    #
    #     # Draw board size options
    #     self.draw_text("Choose Board Size:", margin, 215, (0, 0, 0))
    #     for i, size in enumerate(range(4, 9)):
    #         button_x = margin + 300 + i * (button_width + 10)
    #         button_y = 200
    #         color = (200, 200, 200)
    #         if clicked_button == f"size_{size}":
    #             color = (150, 150, 250)  # Highlight color
    #         pygame.draw.rect(self.screen, color, (button_x, button_y, button_width, button_height))
    #         self.draw_text(f"{size}x{size}", button_x + button_width // 2, button_y + button_height // 2, (0, 0, 0),
    #                        center=True)
    #
    #     # Draw difficulty options
    #     self.draw_text("Choose Difficulty:", margin, 315, (0, 0, 0))
    #     difficulties = ["Easy", "Hard"]
    #     for i, diff in enumerate(difficulties):
    #         button_x = margin + 300 + i * (button_width + 10)
    #         button_y = 300
    #         color = (200, 200, 200)
    #         if clicked_button == f"difficulty_{diff.lower()}":
    #             color = (150, 250, 150)  # Highlight color
    #         pygame.draw.rect(self.screen, color, (button_x, button_y, button_width, button_height))
    #         self.draw_text(diff, button_x + button_width // 2, button_y + button_height // 2, (0, 0, 0), center=True)
    #
    #     # Draw "Let's Play!" button
    #     button_x = window_width // 2 - 100
    #     button_y = window_height - 150
    #     button_color = (100, 255, 100) if clicked_button == "play" else (200, 200, 200)
    #     pygame.draw.rect(self.screen, button_color, (button_x, button_y, 200, 80))
    #     self.draw_text("Let's Play!", button_x + 100, button_y + 40, (0, 0, 0), center=True)
    #
    #     pygame.display.flip()

    def draw_main_menu(self, clicked_button=None):
        """Draw the main menu with board size and difficulty selection."""
        self.screen.fill((255, 255, 255))
        self.draw_title()

        # Get current window dimensions for dynamic positioning
        window_width = self.screen.get_width()
        window_height = self.screen.get_height()
        margin = window_width // 8
        button_width, button_height = 100, 50

        # Draw board size options
        self.draw_text("Choose Board Size:", margin, 215, (0, 0, 0))
        for i, size in enumerate(range(4, 9)):
            button_x = margin + 300 + i * (button_width + 10)
            button_y = 200
            # Highlight the selected board size
            color = (150, 150, 250) if self.selected_board_size == size else (200, 200, 200)
            pygame.draw.rect(self.screen, color, (button_x, button_y, button_width, button_height))
            self.draw_text(f"{size}x{size}", button_x + button_width // 2, button_y + button_height // 2, (0, 0, 0),
                           center=True)

        # Draw difficulty options
        self.draw_text("Choose Difficulty:", margin, 315, (0, 0, 0))
        difficulties = ["easy", "hard"]
        for i, diff in enumerate(difficulties):
            button_x = margin + 300 + i * (button_width + 10)
            button_y = 300
            # Highlight the selected difficulty
            color = (150, 250, 150) if self.selected_difficulty == diff else (200, 200, 200)
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

    # def handle_main_menu_events(self):
    #     """Handle clicks on the main menu."""
    #     window_width = self.screen.get_width()
    #     window_height = self.screen.get_height()
    #     for event in pygame.event.get():
    #         if event.type == pygame.QUIT:
    #             pygame.quit()
    #             sys.exit()
    #         elif event.type == pygame.MOUSEBUTTONDOWN:
    #             x, y = event.pos
    #
    #             # Check board size selection
    #             for i, size in enumerate(range(4, 9)):
    #                 button_x = 200 + 300 + i * (100 + 10)
    #                 button_y = 200
    #                 if button_x <= x <= button_x + 100 and button_y <= y <= button_y + 50:
    #                     self.board_size = size
    #                     self.draw_main_menu(clicked_button=f"size_{size}")
    #                     return False  # Continue displaying menu
    #
    #             # Check difficulty selection
    #             difficulties = ["easy", "hard"]
    #             for i, diff in enumerate(difficulties):
    #                 button_x = 200 + 300 + i * (100 + 10)
    #                 button_y = 300
    #                 if button_x <= x <= button_x + 100 and button_y <= y <= button_y + 50:
    #                     self.difficulty = diff.lower()
    #                     self.draw_main_menu(clicked_button=f"difficulty_{diff.lower()}")
    #                     return False  # Continue displaying menu
    #
    #             # Check "Let's Play!" button
    #             button_x = window_width // 2 - 100
    #             button_y = window_height - 150
    #             if button_x <= x <= button_x + 200 and button_y <= y <= button_y + 80:
    #                 self.draw_main_menu(clicked_button="play")
    #                 pygame.time.wait(200)
    #                 return True  # Proceed to game
    #
    #     return False

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
        self.screen.fill((255, 255, 255))

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

        # Decorative flowers
        # for _ in range(10):
        #     flower_x = randint(0, board_start_x - 50)
        #     flower_y = randint(0, self.WINDOW_HEIGHT)
        #     pygame.draw.circle(self.screen, (255, 0, 255), (flower_x, flower_y), 20)
        # for _ in range(10):
        #     flower_x = randint(board_start_x + self.CELL_SIZE * self.board_size + 50, self.WINDOW_WIDTH)
        #     flower_y = randint(0, self.WINDOW_HEIGHT)
        #     pygame.draw.circle(self.screen, (255, 0, 255), (flower_x, flower_y), 20)

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
                    self.draw_text(message, window_width // 2, window_height // 2, (0, 0, 0), center=True)

                    pygame.display.flip()  # Update the display
                    pygame.time.wait(3000)  # Pause for 3 seconds
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
        # while True:
        #     self.draw_main_menu()
        #     if self.handle_main_menu_events():
        #         self.setup_game()
        #         self.run_game()

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
