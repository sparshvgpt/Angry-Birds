import dis
import pygame
import math
from scripts.utils import distance

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
        self.power_activated = False
        self.damage = 25

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

        # Add movement due to wind
        if not self.game.mainmenu and pygame.time.get_ticks() % 10 == 0:
            self.velocity[0] += math.cos(pygame.time.get_ticks()/1000) if self.game.wind else 0

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

    def activate_power(self, player_index, game):
        if self.type == 'blue':
            newbird1 = Bird(game, 'blue', (self.pos[0], self.pos[1]), (50, 50))
            newbird2 = Bird(game, 'blue', (self.pos[0], self.pos[1]), (50, 50))
            newbird1.velocity = [self.velocity[0], self.velocity[1] + 3]
            newbird2.velocity = [self.velocity[0], self.velocity[1] - 3]
            newbird1.power_activated = True
            newbird2.power_activated = True
            game.birds[player_index].append(newbird1)
            game.birds[player_index].append(newbird2)
            game.sfx['bluepower'].play()
        if self.type == 'yellow':
            self.velocity[0] *= 1.6
            self.velocity[1] *= 1.6
            game.sfx['yellowpower'].play()
        if self.type == 'bomb':
            self.velocity[0] = 0
            for tower_obj in game.towers:
                for block in tower_obj.towerlist[0] + tower_obj.towerlist[1]:
                    if distance(self.rect.centerx, self.rect.centery, block.rect.centerx, block.rect.centery) < 175:
                        block.health -= 25
            game.sfx['bombpower'].play()
        self.power_activated = True
