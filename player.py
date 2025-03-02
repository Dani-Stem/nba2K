import pygame
from settings import WINDOW_WIDTH, WINDOW_HEIGHT

import pygame


class Player(pygame.sprite.Sprite):
    def __init__(self, pos, groups):
        super().__init__(groups)
        self.status = "right"
        self.import_assets()
        self.frame_index = 0
        self.image = self.animation[self.frame_index]
        self.rect = self.image.get_rect(center=pos)

        self.position = pygame.math.Vector2(self.rect.center)
        self.direction = pygame.math.Vector2(1, 0)
        self.speed = 200
        self.max_speed = 500
        self.min_speed = 200
        self.speed_decay = 100

        self.scale_factor = 1.0

    def import_assets(self):
        self.animation = []
        if self.status == "right":
            path = "images/brunson/right/"
            for frame in range(8):
                surf = pygame.image.load(f"{path}{frame}.png").convert_alpha()
                surf = pygame.transform.scale(surf, (200, 200))
                self.animation.append(surf)
        elif self.status == "left":
            path = "images/brunson/left/"
            for frame in range(7, -1, -1):
                surf = pygame.image.load(f"{path}{frame}.png").convert_alpha()
                surf = pygame.transform.scale(surf, (200, 200))
                self.animation.append(surf)

    def outofbounds(self, screen, time):
        screen.fill((0, 0, 0))
        my_font = pygame.font.Font("images/font.ttf", 100)

        message = "OUT OF BOUNDS"
        color = "red"

        downs_surface = my_font.render(message, True, color)
        downs_rect = downs_surface.get_rect(
            center=(WINDOW_WIDTH // 2, WINDOW_HEIGHT // 2)
        )
        screen.blit(downs_surface, downs_rect)
        pygame.display.flip()
        time.sleep(1)

        self.speed = 0
        self.outOfBounds = True
        self.direction = pygame.math.Vector2(1, 0)

    def reset_position(self):
        self.status = "right"
        self.speed = 0
        self.position = pygame.math.Vector2(250, 450)
        self.rect.center = round(self.position.x), round(self.position.y)

    def move(self, dt, screen, time):
        if self.direction.magnitude() != 0:
            self.direction = self.direction.normalize()

        # Gradually decrease speed
        if self.speed > self.min_speed:
            self.speed -= self.speed_decay * dt

        # Update position
        self.position += self.direction * self.speed * dt
        self.rect.center = round(self.position.x), round(self.position.y)

        # Adjust the scale factor based on the vertical position (y-coordinate)
        # The higher the y position, the smaller the sprite becomes, the lower the y position, the bigger the sprite.
        self.scale_factor = max(
            1.0, min(1.5, 1 + (self.position.y - 400) / 500)
        )  # Adjust the divisor and constants to fine-tune size changes

        self.speed = max(self.min_speed, min(self.speed, self.max_speed))

        if self.position.x < 20:
            self.position.x = 20

        if self.position.x > 2000:
            self.outofbounds(screen, time)
            self.reset_position()
            self.direction.y = 0

        if self.position.y < 350 or self.position.y > 775:
            self.outofbounds(screen, time)
            self.reset_position()
            self.direction.y = 0

    def draw(self, screen):
        screen.blit(self.image, self.rect)

    def input(self, events):
        for event in events:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    self.speed += 50

        keys = pygame.key.get_pressed()

        if keys[pygame.K_RIGHT]:
            self.status = "right"
            self.direction.x = 1
        if keys[pygame.K_LEFT]:
            self.status = "left"
            self.direction.x = -1
        if keys[pygame.K_UP]:
            self.direction.y = -1
        if keys[pygame.K_DOWN]:
            self.direction.y = 1

    def animate(self, dt):
        self.frame_index += 10 * dt
        if self.frame_index >= len(self.animation):
            self.frame_index = 0
        self.image = self.animation[int(self.frame_index)]

        # Applys the scale factor to the image
        width, height = self.image.get_size()
        new_width = int(width * self.scale_factor)
        new_height = int(height * self.scale_factor)
        self.image = pygame.transform.scale(
            self.animation[int(self.frame_index)], (new_width, new_height)
        )
        self.rect = self.image.get_rect(
            center=self.rect.center
        )  # Update rect to match the scaled image

    def draw_speed_meter(self, screen):
        bar_width = 200
        bar_height = 20
        bar_x = 170
        bar_y = 20
        pygame.draw.rect(screen, (255, 255, 255), (bar_x, bar_y, bar_width, bar_height))

        # Calculate the width of the green bar based on the player's speed
        green_bar_width = int(
            (self.speed - self.min_speed)
            / (self.max_speed - self.min_speed)
            * bar_width
        )

        pygame.draw.rect(
            screen, (0, 255, 0), (bar_x, bar_y, green_bar_width, bar_height)
        )
        my_font = pygame.font.Font("images/font.ttf", 50)
        speed_surface = my_font.render("SPEED:", True, pygame.Color(255, 255, 255))
        speed_rect = speed_surface.get_rect()
        speed_rect.midtop = (100, 10)
        screen.blit(speed_surface, speed_rect)

    def update(
        self,
        dt,
        events,
        screen,
        time,
    ):
        self.outOfBounds = False
        self.input(events)
        self.move(dt, screen, time)
        self.animate(dt)
        self.import_assets()

        return self.outOfBounds
