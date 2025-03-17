import pygame

WINDOW_WIDTH, WINDOW_HEIGHT = 1215, 812


class Background:
    def __init__(self):
        self.running = True

        # Colors for spotlight effect
        self.spotlight_center = (50, 50, 50)  # Dark Gray (center of light)
        self.spotlight_edge = (0, 0, 0)  # Black (edges and outside light area)

    def generate_background(self):
        background_surface = pygame.Surface(
            (WINDOW_WIDTH, WINDOW_HEIGHT), pygame.SRCALPHA
        )
        background_surface.fill((0, 0, 0, 190))  # Transparency level

        return background_surface

    def generate_spotlight(self):
        spotlight_surface = pygame.Surface(
            (WINDOW_WIDTH, WINDOW_HEIGHT), pygame.SRCALPHA
        )
        center_x, center_y = WINDOW_WIDTH // 2.1, WINDOW_HEIGHT // 4
        bottom_y = WINDOW_HEIGHT
        top_cone_width = WINDOW_WIDTH // 3
        bottom_cone_width = WINDOW_WIDTH // 2

        for y in range(WINDOW_HEIGHT):
            current_width = top_cone_width + (
                (bottom_cone_width - top_cone_width) * (y / WINDOW_HEIGHT)
            )
            left_x = int(center_x - current_width // 2)
            right_x = int(center_x + current_width // 1.5)

            for x in range(left_x, right_x):
                if 0 <= x < WINDOW_WIDTH:
                    distance = (y - center_y) / (bottom_y - center_y)
                    ratio = min(distance, 1)
                    color = (
                        max(
                            0,
                            min(
                                255,
                                int(
                                    (1 - ratio) * self.spotlight_center[0]
                                    + ratio * self.spotlight_edge[0]
                                ),
                            ),
                        ),
                        max(
                            0,
                            min(
                                255,
                                int(
                                    (1 - ratio) * self.spotlight_center[1]
                                    + ratio * self.spotlight_edge[1]
                                ),
                            ),
                        ),
                        max(
                            0,
                            min(
                                255,
                                int(
                                    (1 - ratio) * self.spotlight_center[2]
                                    + ratio * self.spotlight_edge[2]
                                ),
                            ),
                        ),
                        max(0, min(255, int(255 * (1 - ratio)))),
                    )
                    spotlight_surface.set_at((x, y), color)

        return spotlight_surface
