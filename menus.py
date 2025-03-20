import pygame
import sys
import game_loop


def render_start_screen(self):
    self.screen.blit(self.background, (-462, 80))
    self.screen.blit(self.transparent_background, (0, 0))

    # Create a semi-transparent overlay
    overlay = pygame.Surface((self.WINDOW_WIDTH, self.WINDOW_HEIGHT), pygame.SRCALPHA)

    # Set the overlay color and transparency (RGBA format)
    overlay.fill((0, 0, 0, 128))  # Black with 50% transparency

    continue_font = pygame.font.Font("images/font.ttf", 120)
    select_font = pygame.font.Font("images/font.ttf", 100)

    select_font2 = pygame.font.Font("images/font.ttf", 40)

    if self.knicks_turn:
        menu_text = "GET READY!"
        menu_color = "orange"
    else:
        menu_text = "GET READY!"
        menu_color = "yellow"

    menu_surface = continue_font.render(menu_text, True, menu_color)
    menu_rect = menu_surface.get_rect(
        midtop=(self.WINDOW_WIDTH // 2, self.WINDOW_HEIGHT / 5)
    )
    self.screen.blit(overlay, (0, 0))
    self.screen.blit(menu_surface, menu_rect)

    continue_surface = select_font.render("Start", True, menu_color)
    continue_rect = continue_surface.get_rect(
        center=(self.WINDOW_WIDTH // 2, self.WINDOW_HEIGHT / 2)
    )
    continue_surface2 = select_font2.render("(Press Spacebar)", True, menu_color)
    continue_rect2 = continue_surface2.get_rect(
        center=(self.WINDOW_WIDTH // 2, self.WINDOW_HEIGHT / 1.7)
    )
    self.screen.blit(continue_surface, continue_rect)
    self.screen.blit(continue_surface2, continue_rect2)


def start_screen(self, game_loop):
    if not self.tipoff_channel.get_busy():
        self.tipoff_channel.play(self.tipoff_music, loops=-1)
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if event.type == pygame.KEYDOWN:
                pygame.K_SPACE = 32
                if event.key in (pygame.K_RETURN, pygame.K_SPACE):
                    # self.tipoff_music.stop()
                    self.tipoff_loop(game_loop)

        self.render_start_screen()
        self.win_condition()
        self.gameplay_instructions()

        pygame.display.update()

        pygame.display.flip()


def render_continue_menu(self):
    self.screen.fill("black")

    # Fonts
    continue_font = pygame.font.Font("images/font.ttf", 150)
    select_font = pygame.font.Font("images/font.ttf", 100)

    if self.winner:
        menu_text = f"{self.player_team} BALL"
        menu_color = "orange"
    elif not self.winner:
        menu_text = "LAKERS BALL"
        menu_color = "yellow"
    else:
        menu_text = "DRAW"
        menu_color = "red"

    # Render text
    menu_surface = continue_font.render(menu_text, True, menu_color)
    menu_rect = menu_surface.get_rect(
        midtop=(self.WINDOW_WIDTH // 2, self.WINDOW_HEIGHT / 5)
    )
    self.screen.blit(menu_surface, menu_rect)

    # Render menu items dynamically
    base_y = self.WINDOW_HEIGHT / 2 + 10  # Start lower on the screen
    spacing = 120  # Adjust spacing between items
    for index, item in enumerate(self.continue_item):
        text_color = (
            "red"
            if item == "Quit" and index == self.selected_index
            else "green" if index == self.selected_index else "white"
        )

        menu_text = select_font.render(item, True, text_color)
        text_rect = menu_text.get_rect(
            center=(self.WINDOW_WIDTH // 2, base_y + index * spacing)
        )
        self.screen.blit(menu_text, text_rect)


def continue_menu(self, game_loop):
    self.selected_index = 0

    if self.score[0] == 5:
        self.winner = True
    elif self.score[1] == 5:
        self.winner = False
    else:
        self.winner = None

    running = True
    while running:
        self.render_continue_menu()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP:
                    self.highlight_sound.play()
                    self.selected_index = (self.selected_index - 1) % len(
                        self.continue_item
                    )
                elif event.key == pygame.K_DOWN:
                    self.highlight_sound.play()
                    self.selected_index = (self.selected_index + 1) % len(
                        self.continue_item
                    )
                elif event.key in (pygame.K_RETURN, pygame.K_SPACE):
                    self.confirm_sound.play()
                    if self.continue_item[self.selected_index] == "Quit":
                        pygame.quit()
                        sys.exit()
                    elif self.continue_item[self.selected_index] == "Continue":
                        game_loop()

        pygame.display.flip()


def reset_game(self):
    self.start = True
    self.drop = False
    self.jumping = False
    self.landing = False
    self.score = [0, 0]

    self.player.reset()
    self.cpu.reset()
    self.dropBall.reset()

    self.start_screen()