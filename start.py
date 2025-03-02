import pygame, sys
import random
from pygame.sprite import Sprite
from pygame.rect import Rect

WINDOW_WIDTH, WINDOW_HEIGHT = 1368, 712

team = ""

def start_menu(self):
    self.win_music.stop()
    self.lose_music.stop()
    if not self.start_channel.get_busy():
        self.start_channel.play(self.start_music, loops=-1)
    while True:

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_s:
                    self.start_sound.play()
                    self.teamselect_menu()

        self.screen.fill(self.BLACK)
        self.logo()
        self.howto(self.instructions, self.WHITE, (575, 50), line_spacing=5)

        self.show_startscreen()
        self.show_startscreensub()
        self.show_startscreensub1()
        pygame.display.flip()


def render_teamselect_menu(self, selected_index2):
    self.screen.fill(self.BLACK)
    teamselect_font = pygame.font.Font("images/font.ttf", 150)
    select_font = pygame.font.Font("images/font.ttf", 100)

    score_surface = teamselect_font.render("PICK UR TEAM", True, "yellow")
    score_rect = score_surface.get_rect()
    score_rect.midtop = (WINDOW_WIDTH // 2, WINDOW_HEIGHT / 10)
    self.screen.blit(score_surface, score_rect)
    for index, item in enumerate(self.teamselect_menu_items):
        if index == selected_index2:
            text_color = self.HIGHLIGHT
            if self.teamselect_menu_items[selected_index2] == "LAKERS":
                text_color = "purple"
            elif self.teamselect_menu_items[selected_index2] == 'KNICKS':
                text_color = "blue"
        else:
            text_color = self.WHITE

        menu_text = select_font.render(item, True, text_color)

        text_rect = menu_text.get_rect(
            center=(
                WINDOW_WIDTH / 1.48 + (index - len(self.teamselect_menu_items) // 2) * 480,
                WINDOW_HEIGHT // 1.2,
            )
        )
        self.screen.blit(menu_text, text_rect)
        self.logoknx()
        self.logolakers()



def teamselect_menu(self):
    selected_index2 = 0
    running = True

    # Disable spacebar for a few seconds when the menu is rendered
    self.spacebar_enabled = False
    pygame.time.set_timer(pygame.USEREVENT, 100)

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if event.type == pygame.USEREVENT:
                self.spacebar_enabled = True
                pygame.time.set_timer(pygame.USEREVENT, 0)  # Stop the timer

            if event.type == pygame.KEYDOWN:
                if not self.spacebar_enabled and event.key == pygame.K_SPACE:
                    continue  # Ignore spacebar presses if disabled

                self.highlight_sound.play()
                if event.key == pygame.K_LEFT:
                    self.highlight_sound.play()
                    selected_index2 = (selected_index2 - 1) % len(self.teamselect_menu_items)
                elif event.key == pygame.K_RIGHT:
                    self.highlight_sound.play()
                    selected_index2 = (selected_index2 + 1) % len(self.teamselect_menu_items)
                elif event.key == pygame.K_RETURN or event.key == pygame.K_SPACE:
                    self.confirm_sound.play()
                    self.howto_menu()
                    self.confirm_sound.play()

                    if self.teamselect_menu_items[selected_index2] == "KNICKS":
                        team = "KNICKS"
            
                    elif self.teamselect_menu_items[selected_index2] == "LAKERS":
                        team = "LAKERS"



        self.render_teamselect_menu(selected_index2)
        pygame.display.flip()

def howto_menu(self):
    if not self.start_channel.get_busy():
        self.start_channel.play(self.start_music, loops=-1)
    while True:

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_s:
                    self.start_sound.play()
                    self.game_loop()

        self.screen.fill(self.BLACK)
        
        if team == "KNICKS": 
            self.logoknx1()
        elif team == "LAKERS": 
            self.logolakers1()

        self.howto(self.instructions, self.WHITE, (575, 50), line_spacing=5)
        self.show_startscreen()
        self.show_startscreensub()
        self.show_startscreensub1()
        pygame.display.flip()


