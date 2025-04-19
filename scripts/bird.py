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
        self.onground = False
        self.collided = False
        self.collidingtime = 3

    def update(self, movement=(0, 0)):
        frame_movement = (movement[0] + self.velocity[0], movement[1] + self.velocity[1])
        
        if not self.onground:
            self.velocity[1] = self.velocity[1] + 0.3

        self.pos[0] += frame_movement[0]
        self.pos[1] += frame_movement[1]
        self.rect = pygame.Rect(self.pos[0], self.pos[1], self.size[0], self.size[1])

    def render(self, surf):
        surf.blit(self.game.images[self.type], self.pos)
