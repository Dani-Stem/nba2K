import pygame
from settings import WINDOW_WIDTH, WINDOW_HEIGHT
import time
from player import Player
from inbounder import Inbounder
from tipoff import TipOff
from game_loop import game_loop
from all_sprites import AllSprites

from start import start_menu, render_teamselect_menu, teamselect_menu, howto_menu, playerselect_menu, render_playerselect_menu
from main_menu import main_menu, render_menu

class Game:
    def __init__(self):
        pygame.init()
        pygame.mixer.init()
        self.screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
        pygame.display.set_caption("NBA 2K25")
        self.clock = pygame.time.Clock()
        
        #groups
        self.player_group = AllSprites()
        self.inbounder_group = pygame.sprite.Group()

        #variables
        self.outOfBounds = False
        self.inbounder_is_active = True
        self.snap = False
        self.menu = False
        self.team = "NONE"
        self.keypressed = ""

        # Colors
        self.WHITE = (255, 255, 255)
        self.BLACK = (0, 0, 0)
        self.HIGHLIGHT = "green"
        self.start = True

        #fonts
        self.font = pygame.font.Font("images/font.ttf", 74)

        #data
        self.qtr = 1
        self.score = [0, 0]
        self.white = pygame.Color(255, 255, 255)
        self.knicksbackground = pygame.image.load("images/knicks_court_alt.png").convert()
        self.lakersbackground = pygame.image.load("images/lakers_court_alt.png").convert()
        self.background = None
        self.tipoff = TipOff(self.team)

        self.player = Player((250, 450), self.player_group, self.team)
        self.inbounder = Inbounder(
            (250, 350),
            self.inbounder_group,
            self.inbounder_is_active,
            self.snap,
            self.team
        )

        #channels
        if not hasattr(self, "start_channel"):
            self.start_channel = pygame.mixer.Channel(2)

        # Instructions
        self.instructions = [
            "HOW TO PLAY:",
            "",
            "OFFENSIVE MOVES:",
            "-PASS | A KEY",
            "-SHOOT | W KEY",
            "-JUMP | SPACE KEY",
            "-SPIN | S AND LEFT OR RIGHT ARROW KEYS",
            "-HALF SPIN | AS AND LEFT OR RIGHT ARROW KEYS",
            "-PUMP | SHIFT KEY",
            "-DUNK | D KEY",
            "-EUROSTEP | SPACEBAR AND SHIFT KEYS",
            "-FLOP | WAD KEYS",
            "-BALL BEHIND THE BACK | SA KEYS",
            "-SWITCH HANDS | SD KEYS"
            "",
            "DEFENSIVE MOVES:",
            "-JUMP | SPACE KEY",
            "-BLOCK | W KEY",
            "-SUMMON 2ND MAN | A KEY",
            "-STEAL | D AND LEFT OR RIGHT ARROW KEYS",
            "-DRAYMOND | S KEY"
            "-FLOP | WAD KEYS",

        ]


        self.teamselect_menu_items = ["KNICKS", "LAKERS"]


        self.playerselect_menu_items = ["BRUNSON", "LEBRON"]


        #Sounds
        self.start_music = pygame.mixer.Sound("images/sounds/start.mp3")
        self.start_music.set_volume(0.2)

        self.player_music = pygame.mixer.Sound("images/sounds/player.mp3")
        self.player_music.set_volume(0.04)

        self.opp_music = pygame.mixer.Sound("images/sounds/opp.mp3")
        self.opp_music.set_volume(0.1)

        self.highlight_sound = pygame.mixer.Sound("images/sounds/highlight.wav")
        self.highlight_sound.set_volume(0.05)

        self.confirm_sound = pygame.mixer.Sound("images/sounds/confirm.wav")
        self.confirm_sound.set_volume(0.05)

        self.coin_sound = pygame.mixer.Sound("images/sounds/coin.wav")
        self.coin_sound.set_volume(0.05)

        self.win_music = pygame.mixer.Sound("images/sounds/win.mp3")
        self.win_music.set_volume(0.05)

        self.lose_music = pygame.mixer.Sound("images/sounds/lose.mp3")
        self.lose_music.set_volume(0.2)

        self.start_sound = pygame.mixer.Sound("images/sounds/start.wav")
        self.start_sound.set_volume(0.05)


    def show_qtr(self, qtr, screen):
        self.qtr = qtr % 4
        my_font = pygame.font.Font("images/font.ttf", 50)
        if self.qtr == 1:
            down_surface = my_font.render("1ST QTR", True, "white")
        elif self.qtr == 2:
            down_surface = my_font.render("2ND QTR", True, "white")
        elif self.qtr == 3:
            down_surface = my_font.render("3RD QTR", True, "white")
        elif self.qtr == 0:
            down_surface = my_font.render("4TH QTR", True, "white")

        down_rect = down_surface.get_rect()
        down_rect.midtop = (615, 5)
        screen.blit(down_surface, down_rect)

        return self.qtr

    def show_score(self):
        my_font = pygame.font.Font("images/font.ttf", 50)
        score_surface = my_font.render(
            f"SCORE: {self.score[0]} vs {self.score[1]}", True, self.white
        )
        score_rect = score_surface.get_rect()
        score_rect.midtop = (1050, 5)
        self.screen.blit(score_surface, score_rect)
        

    def show_startscreen(self):

        my_font = pygame.font.Font("images/font.ttf", 45)
        speed_surface = my_font.render("NBA 2K25", True, "yellow")
        speed_rect = speed_surface.get_rect()
        speed_rect.midtop = (320, 480)
        self.screen.blit(speed_surface, speed_rect)

    def show_startscreensub(self):

        my_font = pygame.font.Font("images/font.ttf", 30)
        speed_surface = my_font.render("A DN INDUSTRIES PRODUCT", True, "yellow")
        speed_rect = speed_surface.get_rect()
        speed_rect.midtop = (320, 515)
        self.screen.blit(speed_surface, speed_rect)

    def show_startscreensub1(self):
        # Use time to determine if the text should be visible
        if int(time.time() * 2) % 2 == 0:  # Blink every 0.5 seconds
            my_font = pygame.font.Font("images/font.ttf", 55)
            speed_surface = my_font.render("PRESS S TO START THE GAME", True, "white")
            speed_rect = speed_surface.get_rect()
            speed_rect.midtop = (806, 605)
            self.screen.blit(speed_surface, speed_rect)

    def logo(self):
        implogo = pygame.image.load("images/logo.png").convert_alpha()
        self.screen.blit(
            implogo,
            pygame.Rect(105, 100, 10, 10),
        )

    def logolakers(self):
        implogolakers = pygame.image.load("images/logolakers.png").convert_alpha()
        self.screen.blit(
            implogolakers,
            pygame.Rect(777, 225, 40, 10),
        )
        
    def logolakers1(self):
        implogolakers = pygame.image.load("images/logolakers.png").convert_alpha()
        self.screen.blit(
            implogolakers,
            pygame.Rect(180, 175, 10, 10),
        )

    def logoknx(self):
        implogoknx = pygame.image.load("images/logoknx.png").convert_alpha()
        self.screen.blit(
            implogoknx,
            pygame.Rect(290, 225, 10, 10),
        )

    def logoknx1(self):
        implogoknx = pygame.image.load("images/logoknx.png").convert_alpha()
        self.screen.blit(
            implogoknx,
            pygame.Rect(170, 125, 10, 10),
        )    

    def howto(self, lines, color, start_pos, line_spacing=5):
        font = pygame.font.Font("images/font.ttf", 30)
        x, y = start_pos
        for line in lines:
            text_surface = font.render(line, True, color)
            self.screen.blit(text_surface, (x, y))
            y += font.get_height() + line_spacing      

    def game_loop(self):
        game_loop(self)


    def start_menu(self):
        start_menu(self)

    def render_menu(self, selected_index, menu):
        render_menu(self, selected_index, menu)

    def main_menu(self):
        main_menu(self)

    def teamselect_menu(self):
        teamselect_menu(self)

    def render_teamselect_menu(self, selected_index2): 
        render_teamselect_menu(self, selected_index2)   

    def playerselect_menu(self):
        playerselect_menu(self)

    def render_playerselect_menu(self, selected_index3):
        render_playerselect_menu(self, selected_index3)

    def howto_menu(self):
        howto_menu(self)  

    def run(self):
        self.start_menu()
        """
        self.coin_menu()
        self.teamselect_menu()
        self.howto_menu()
        self.main_menu()
        self.player_loop()
        self.stop_opp()
        self.opp_loop()
        self.game_loop()
        """


if __name__ == "__main__":
    game = Game()
    game.run()
