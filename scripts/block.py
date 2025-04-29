import pygame
import time

class Block:
    def __init__(self, game, pos, block_type):
        self.game = game
        self.pos = pos
        self.health = 100
        self.block_type = block_type
        self.size = (100, 50)
        self.rect = pygame.Rect(self.pos[0], self.pos[1], self.size[0], self.size[1])
    
    def check_collision(self, game, bird, secondnearest: bool):
        # Check if the block is hit by a bird
        damaged = False
        if not bird.onground and bird.rect.colliderect(self.rect):
            if (bird.health > 0): 
                if (bird.power_activated):
                    if (bird.type == 'red'):
                        self.health -= bird.damage*2
                    elif (bird.type == 'blue'):
                        self.health -= bird.damage if self.block_type == 'ice' else bird.damage
                    elif (bird.type == 'yellow'):
                        self.health -= bird.damage*4 if self.block_type == 'wood' else 2*bird.damage
                elif ((bird.type == 'yellow' and self.block_type == 'wood') or (bird.type == 'blue' and self.block_type == 'ice') or (bird.type == 'bomb' and self.block_type == 'stone')):
                    self.health -= 2*bird.damage
                elif (bird.type == 'red'):
                    self.health -= bird.damage*2
                else:
                    self.health -= bird.damage
                bird.health -= 1
                bird.collided = True
                bird.collidingtime = time.time()
                if (not secondnearest): damaged = True

        if not secondnearest:
            # Get centers
            bird_cx, bird_cy = bird.rect.center
            block_cx, block_cy = self.rect.center
            # Find the difference in center points
            dx = bird_cx - block_cx
            dy = bird_cy - block_cy

            # Calculate how much overlap there is on x and y
            overlap_x = (self.rect.width + bird.rect.width) / 2 - abs(dx)
            overlap_y = (self.rect.height + bird.rect.height) / 2 - abs(dy)
            normal = []
            if overlap_x < overlap_y:
                # Horizontal collision
                if dx > 0:
                    # Bird hit block from the right
                    normal = [-1, 1]
                    bird.pos[0] = self.rect.right

                else:
                    # Bird hit block from the left
                    normal = [-1, 1]
                    bird.pos[0] = self.rect.left - bird.size[0]
            else:
                # Vertical collision
                if dy > 0:
                    # Bird hit block from below
                    normal = [1, -1]
                    bird.pos[1] = self.rect.bottom
                else:
                    # Bird hit block from above
                    normal = [1, -1]
                    bird.pos[1] = self.rect.top - bird.size[1]
                    if abs(bird.velocity[1]) < 2:
                        bird.velocity[1] = 0
                        bird.pos[1] = self.rect.top - bird.size[1]
                        bird.rect.y = int(bird.pos[1])
                        bird.onground = True
            bird.velocity = [bird.velocity[i]*normal[i]*0.5 for i in range(2)]

        return damaged

    def render(self, surf):
        if self.health > 75:
            surf.blit(self.game.images[self.block_type][self.block_type + '100'], self.pos)
        elif self.health > 50:
            surf.blit(self.game.images[self.block_type][self.block_type + '75'], self.pos)
        elif self.health > 25:
            surf.blit(self.game.images[self.block_type][self.block_type + '50'], self.pos)
        elif self.health > 0:
            surf.blit(self.game.images[self.block_type][self.block_type + '25'], self.pos)
        else:
            self.rect = pygame.Rect(0, 0, 0, 0)
