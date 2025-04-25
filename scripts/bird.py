import pygame

class Bird():
    def __init__(self, game, bird_type, pos, size):
        self.health = 1
        self.game = game
        self.type = bird_type
        self.pos = list(pos)
        self.size = size
        self.velocity = [0, 0]
        self.rect = pygame.Rect(self.pos[0], self.pos[1], self.size[0], self.size[1])
        self.justbelowrect = pygame.Rect(self.rect.x, self.rect.bottom, self.rect.width, 2)
        self.onground = False
        self.collided = False
        self.collidingtime = 3
        self.trail = []  # List of (x, y, alpha) tuples
        self.trail_timer = 0

    def update(self, movement=(0, 0)):
        if not self.onground:
            self.velocity[1] += 0.3

            self.trail_timer += 1
            if self.trail_timer >= 3:
                self.trail.append([
                    int(self.pos[0] + self.size[0] // 2),
                    int(self.pos[1] + self.size[1] // 2),
                    255
                ])
                self.trail_timer = 0
        else:
            self.velocity[1] = 0
            self.velocity[0] = self.velocity[0] * 0.93
            self.trail_timer = 0

        # Fade out older trail points
        for dot in self.trail:
            dot[2] -= 5  # reduce alpha

        # Remove invisible dots
        self.trail = [dot for dot in self.trail if dot[2] > 0]

        frame_movement = (movement[0] + self.velocity[0], movement[1] + self.velocity[1])

        self.pos[0] += frame_movement[0]
        self.pos[1] += frame_movement[1]
        self.rect = pygame.Rect(self.pos[0], self.pos[1], self.size[0], self.size[1])
        self.justbelowrect = pygame.Rect(int(self.pos[0]), int(self.pos[1]) + 50, self.size[0], 10)

    def render(self, surf, invert):
        if not self.game.mainmenu:
            for x, y, alpha in self.trail:
                trail_dot = pygame.Surface((16, 16), pygame.SRCALPHA)
                pygame.draw.circle(trail_dot, (255, 255, 255, alpha), (8, 8), 8)
                surf.blit(trail_dot, (x - 8, y - 8))

        if invert:
            surf.blit(pygame.transform.flip(self.game.images[self.type], True, False), self.pos)
        else:
            surf.blit(self.game.images[self.type], self.pos)
