import pygame
import time
import sys
from game_loop import game_loop
from tipoffplayer import Player
from tipoffcpu import CPU
from tipoffbackground import Background
from tipoffdrop_ball import DropBall
from menus import (
    render_start_screen,
    render_continue_menu,
    start_screen,
    continue_menu,
    reset_game,
)


class TipOff:
    def __init__(self, team, selectedplayer):
        pygame.init()

        # Constants
        self.WINDOW_WIDTH, self.WINDOW_HEIGHT = 1215, 812
        self.screen = pygame.display.set_mode((self.WINDOW_WIDTH, self.WINDOW_HEIGHT))
        pygame.display.set_caption("Tip Off")
        self.clock = pygame.time.Clock()

        # Sprite Groups
        self.player_group = pygame.sprite.Group()
        self.cpu_group = pygame.sprite.Group()
        self.dropBall_group = pygame.sprite.Group()
        self.team = team
        self.selectedplayer = selectedplayer

        self.player_team = self.team
        self.cpu_team = ""
        if self.player_team == "KNICKS":
            cpu_team = "LAKERS"
        else:
            cpu_team = "KNICKS"
        # Create Players
        self.player = Player((570, 612), self.player_group, self.player_team)
        self.cpu = CPU((670, 612), self.cpu_group, cpu_team)

        # Create DropBall
        self.dropBall = DropBall((617, -50), self.dropBall_group)

        # Sounds
        if not hasattr(self, "tipoff_channel"):
            self.tipoff_channel = pygame.mixer.Channel(0)

        self.highlight_sound = pygame.mixer.Sound("images/sounds/highlight.wav")
        self.highlight_sound.set_volume(0.05)

        self.confirm_sound = pygame.mixer.Sound("images/sounds/confirm.wav")
        self.confirm_sound.set_volume(0.05)

        self.tipoff_win_sound = pygame.mixer.Sound("images/sounds/tipoff_win.wav")
        self.tipoff_win_sound.set_volume(0.05)

        self.tipoff_lose_sound = pygame.mixer.Sound("images/sounds/tipoff_lose.wav")
        self.tipoff_lose_sound.set_volume(0.05)

        self.tipoff_music = pygame.mixer.Sound("images/sounds/tipoff_music.mp3")
        self.tipoff_music.set_volume(0.05)

        # Game state variables
        self.start = True
        self.knicks_turn = True
        self.drop = False
        self.jumping = False
        self.landing = False
        self.winner = None
        self.score = [0, 0]

        self.continue_item = ["Continue", "Quit"]
        self.selected_index = 0
        
        self.team = team
        self.selectedplayer = selectedplayer
        
    def update_team(self, team):
        self.team = team
        self.player_team = self.team
        cpu_team = ""
        if self.player_team == "KNICKS":
            cpu_team = "LAKERS"
        else:
            cpu_team = "KNICKS"
        self.player.update_team(self.player_team)
        self.cpu.update_team(cpu_team)

    def update_player(self, selectedplayer):
        self.selectedplayer = selectedplayer
        self.player_selectedplayer = self.selectedplayer
        self.selectedplayer.update_selectedplayer(self.player_selectedplayer)
        
        # Load background
        
        self.background = pygame.image.load(
            f"images/courts/{self.player_team.lower()}_court_alt.png"
        ).convert()
        self.transparent_background, self.spotlight = (
            Background().generate_background(),
            Background().generate_spotlight(),
        )


    def handle_events(self, events):
        for event in events:
            if event.type == pygame.QUIT:
                return False

        return True

    def show_score(self):
        my_font = pygame.font.Font("images/font.ttf", 60)

        score_surface = my_font.render(f"{self.score[0]}", True, "white")

        score_surface2 = my_font.render(f"{self.score[1]}", True, "white")

        score_rect = score_surface.get_rect()
        score_rect.midtop = (480, 445)

        score_rect2 = score_surface.get_rect()
        score_rect2.midtop = (748, 445)

        self.screen.blit(score_surface, score_rect)
        self.screen.blit(score_surface2, score_rect2)

    def win_condition(self):
        my_font = pygame.font.Font("images/font.ttf", 50)
        score_surface = my_font.render("First to 5 Wins", True, "white")
        score_rect = score_surface.get_rect()
        score_rect.midtop = (1030, 5)
        self.screen.blit(score_surface, score_rect)

    def gameplay_instructions(self):
        my_font = pygame.font.Font("images/font.ttf", 50)
        score_surface = my_font.render("Jump: Spacebar", True, "white")
        score_rect = score_surface.get_rect()
        score_rect.midtop = (190, 5)
        self.screen.blit(score_surface, score_rect)

    def render_start_screen(self):
        render_start_screen(self)

    def start_screen(self, game_loop):
        start_screen(self, game_loop)

    def render_continue_menu(self):
        render_continue_menu(self)

    def continue_menu(self, game_loop):
        continue_menu(self, game_loop)

    def reset_game(self):
        reset_game(self)

    def draw(self):
        self.screen.blit(self.background, (-462, 80))
        self.screen.blit(self.transparent_background, (0, 0))
        self.screen.blit(self.spotlight, (0, 0))

        self.win_condition()
        self.gameplay_instructions()

        self.show_score()

        self.player_group.draw(self.screen)
        self.cpu_group.draw(self.screen)
        self.dropBall_group.draw(self.screen)

        pygame.display.update()

    def update(self, dt, events):
        self.jumping, self.landing = self.player.update(dt, events)
        self.cpu.update(dt, self.dropBall)

        # Ball drops after the player starts the game and after jumping and landing animations complete.
        if not self.start and not self.drop and not self.jumping and not self.landing:
            self.drop = True
            self.dropBall.reset()

        elif self.drop:
            self.score = self.dropBall.update(
                dt, self.player_group, self.cpu_group, self.score
            )
            if self.dropBall.is_dropped:
                self.drop = False
                self.dropBall.reset()

    def tipoff_loop(self, game_loop):
        self.start = False
        running = True
        while running:
            dt = self.clock.tick(60) / 1000

            events = pygame.event.get()
            running = self.handle_events(events)

            self.update(dt, events)

            self.draw()

            if self.score[0] == 5 or self.score[1] == 5:
                if self.score[0] == 5:
                    self.tipoff_win_sound.play()
                elif self.score[1] == 5:
                    self.tipoff_lose_sound.play()

                time.sleep(1)
                self.continue_menu(game_loop)

        pygame.quit()

    def run(self, game_loop):
        self.start_screen(game_loop)
        self.continue_menu(game_loop)
        self.tip_off(game_loop)

if __name__ == "__main__":
    game = TipOff()
    game.run()