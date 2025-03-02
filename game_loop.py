import pygame, sys
import time


def game_loop(self):
    while True:

        events = pygame.event.get()
        for event in events:
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        dt = self.clock.tick() / 1000

        self.screen.blit(self.knicksbackground, (0, 0))

        self.qtr = self.show_qtr(self.qtr, self.screen)

        self.show_score()

        if self.inbounder_is_active:
            (
                self.inbounder_is_active,
                self.snap,
                self.outOfBounds,
            ) = self.inbounder.update(
                dt,
                events,
                self.outOfBounds,
            )

            self.inbounder.snap_throw_instructions(self.screen)

        else:
            (
                self.inbounder_is_active,
                self.snap,
                self.outOfBounds,
            ) = self.inbounder.update(
                dt,
                events,
                self.outOfBounds,
            )

            self.player_group.customize_draw(
                self.player,
                self.screen,
                self.knicksbackground,
                self.qtr,
                self.show_qtr,
                self.show_score,
            )

            self.outOfBounds = self.player.update(
                dt,
                events,
                self.screen,
                time,
            )

        if self.outOfBounds:
            self.snap = False
            self.qtr += 1

        pygame.display.update()
