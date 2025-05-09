import pygame


class PlayerSelect(pygame.sprite.Sprite):
    def __init__(self, pos, groups):
        super().__init__(groups)

        self.clock = pygame.time.Clock()

        self.team = "knicks"
        self.current_player = "brunson"

        self.import_assets()
        self.frame_index = 0
        self.image = self.idle_animation[self.frame_index]
        self.rect = self.image.get_rect(center=pos)
        self.pos = pygame.math.Vector2(self.rect.center)

    def import_assets(self):
        self.idle_animation = [
            pygame.transform.scale(
                pygame.image.load(
                    f"images/{self.team}/{self.current_player}/{self.current_player}_idle/{frame}.png"
                ).convert_alpha(),
                (500, 500),
            )
            for frame in range(10)
        ]

        self.animation = self.idle_animation

    def animate(self):
        dt = self.clock.tick() / 1000
        # Loop idle animation
        self.frame_index += 10 * dt
        if self.frame_index >= len(self.idle_animation):
            self.frame_index = 0

        self.image = self.idle_animation[int(self.frame_index)]

    def update(self, team, current_player):
        if self.team != team or self.current_player != current_player:
            self.current_player = current_player
            self.team = team
            self.import_assets()
        self.animate()
