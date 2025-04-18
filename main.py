import pygame
import sys
import os
import math
import numpy as np
import scripts.utils as utils
import scripts.bird as BirdModule
import scripts.block as BlockModule
import scripts.tower as TowerModule
import time

class Game:
    def __init__(self):
        pygame.init()

        pygame.display.set_caption('Angry Birds')
        self.screen = pygame.display.set_mode((1440, 810))

        self.clock = pygame.time.Clock()
        self.game_bg = utils.LoadScaledImage('game_bg.png')

        self.images = {
            'red': utils.LoadScaledImage('birds/red.png'),
            'yellow': utils.LoadScaledImage('birds/yellow.png'),
            'blue': utils.LoadScaledImage('birds/blue.png'),
            'bomb': utils.LoadScaledImage('birds/bomb.png'),
            'ground': utils.LoadScaledImage('ground.png'),
            'sling1': utils.LoadScaledImage('sling1.png', removebg=False),
            'sling2': utils.LoadScaledImage('sling2.png', removebg=False),
            'ice': {'ice100': utils.LoadScaledImage('blocks/ice100.png'),
                    'ice75': utils.LoadScaledImage('blocks/ice75.png'),
                    'ice50': utils.LoadScaledImage('blocks/ice50.png'),
                    'ice25': utils.LoadScaledImage('blocks/ice25.png'),},
            'wood': {'wood100': utils.LoadScaledImage('blocks/wood100.png'),
                     'wood75': utils.LoadScaledImage('blocks/wood75.png'),
                     'wood50': utils.LoadScaledImage('blocks/wood50.png'),
                     'wood25': utils.LoadScaledImage('blocks/wood25.png'),},
            'stone': {'stone100': utils.LoadScaledImage('blocks/stone100.png'),
                      'stone75': utils.LoadScaledImage('blocks/stone75.png'),
                      'stone50': utils.LoadScaledImage('blocks/stone50.png'),
                      'stone25': utils.LoadScaledImage('blocks/stone25.png'),},
        }

        self.groundrect = self.images['ground'].get_rect(topleft=(0, self.screen.get_height() - 100))

        self.sling_x1, self.sling_y1 = [310, 1138], [530, 530]
        self.sling_x2, self.sling_y2 = [370, 1206], [530, 530]
        self.mouse_distance = [0, 0]
        self.rope_length = 90
        self.angle = [0, 0]
        self.x_mouse = 0
        self.y_mouse = 0
        self.count = [0, 0]
        self.mouse_pressed = False
        self.number_of_birds = [10, 10]
        self.birds = [[], []]
        self.birds_waiting = utils.InitialiseBirdsWaiting()
        self.current_bird = [np.random.choice(['red', 'blue', 'yellow', 'blue']), np.random.choice(['red', 'blue', 'yellow', 'blue'])]
        print(self.current_bird)
        print(self.birds_waiting)
        self.t1 = [0, 0]
        self.t2 = [0, 0]
        self.mouse_distance = [0, 0]
        self.player1_active = True
        self.block1 = BlockModule.Block(self, (600, 330), 'ice')
        # self.towers = [Tower(), Tower()]

    def run(self):
        while True:
            for event in pygame.event.get():
                # Quit Game
                if event.type == pygame.QUIT:
                    utils.QuitGame()
                # Check mouse pressed in sling 1 area when player 1 active
                if (pygame.mouse.get_pressed()[0] and self.x_mouse > 230 and
                    self.x_mouse < 430 and self.y_mouse > 430 and self.y_mouse < 630 and self.player1_active):
                    self.mouse_pressed = True
                # Check mouse pressed in sling 2 area when player 2 active
                if (pygame.mouse.get_pressed()[0] and self.x_mouse > 1060 and
                    self.x_mouse < 1260 and self.y_mouse > 430 and self.y_mouse < 630 and not self.player1_active):
                    self.mouse_pressed = True
                # Release new bird for player 1
                if (event.type == pygame.MOUSEBUTTONUP and
                        event.button == 1 and self.mouse_pressed and self.player1_active):
                    self.mouse_pressed = False
                    if self.number_of_birds[0] > 0:
                        self.number_of_birds[0] -= 1
                        self.t1[0] = time.time()*1000
                        xo = 310
                        yo = 510
                        if self.mouse_distance[0] > self.rope_length:
                            self.mouse_distance[0] = self.rope_length
                        bird1 = BirdModule.Bird(self, self.current_bird[0], (xo, yo), (50, 50))
                        bird1.velocity[0] = -self.mouse_distance[0]*math.cos(self.angle[0])*0.25
                        bird1.velocity[1] = -self.mouse_distance[0]*math.sin(self.angle[0])*0.25
                        self.birds[0].append(bird1)
                        if self.number_of_birds[0] == 0:
                            self.t2[0] = time.time()
                        utils.NextBirdGenerator(self)
                        self.player1_active = not self.player1_active
                # Release new bird for player 2
                if (event.type == pygame.MOUSEBUTTONUP and
                        event.button == 1 and self.mouse_pressed and not self.player1_active):
                    self.mouse_pressed = False
                    if self.number_of_birds[1] > 0:
                        self.number_of_birds[1] -= 1
                        self.t1[1] = time.time()*1000
                        xo = 1138
                        yo = 510
                        if self.mouse_distance[1] > self.rope_length:
                            self.mouse_distance[1] = self.rope_length
                        bird2 = BirdModule.Bird(self, self.current_bird[1], (xo, yo), (50, 50))
                        bird2.velocity[0] = -self.mouse_distance[1]*math.cos(self.angle[1])*0.25
                        bird2.velocity[1] = -self.mouse_distance[1]*math.sin(self.angle[1])*0.25
                        self.birds[1].append(bird2)
                        if self.number_of_birds[1] == 0:
                            self.t2[1] = time.time()
                        utils.NextBirdGenerator(self)
                        self.player1_active = not self.player1_active

            self.x_mouse, self.y_mouse = pygame.mouse.get_pos()

            self.screen.blit(self.game_bg, (0,0))
            self.screen.blit(self.images['ground'], self.groundrect)
            self.screen.blit(self.images['sling1'], (302, 510))
            self.screen.blit(self.images['sling2'], (1138, 510))

            # Draw not flying birds for player 1
            if self.mouse_pressed and self.number_of_birds[0] > 0 and self.player1_active:
                utils.sling_action(self, self.player1_active)
            else:
                if time.time()*1000 - self.t1[0] > 300 and self.number_of_birds[0] > 0:
                    self.screen.blit(self.images[self.current_bird[0]], (310, 510))
                else:
                    pygame.draw.line(self.screen, (0, 0, 0), (self.sling_x1[0], self.sling_y1[0]-8),
                                    (self.sling_x2[0], self.sling_y2[0]-7), 5)
                    
            # Draw not flying birds for player 2
            if self.mouse_pressed and self.number_of_birds[1] > 0 and not self.player1_active:
                utils.sling_action(self, self.player1_active)
            else:
                if time.time()*1000 - self.t1[1] > 300 and self.number_of_birds[1] > 0:
                    self.screen.blit(self.images[self.current_bird[1]], (1138, 510))
                else:
                    pygame.draw.line(self.screen, (0, 0, 0), (self.sling_x1[1], self.sling_y1[1]-8),
                                    (self.sling_x2[1], self.sling_y2[1]-7), 5)
                    
            for bird in self.birds[0]:
                # if bird.shape.body.position.y < 0:
                #     birds_to_remove.append(bird)
                p = bird.pos
                x, y = p
                x -= 50
                y -= 50
                if self.groundrect.colliderect(pygame.Rect(*bird.pos, *bird.size)) and bird.velocity[1] > 0:
                    if abs(bird.velocity[1]) < 2:
                        bird.velocity[1] = 0
                        bird.onground = True
                    else:
                        bird.velocity[1] = -bird.velocity[1]*0.5
                    bird.velocity[0] = bird.velocity[0]*0.5

                    bird.pos[1] = self.groundrect.top - bird.size[1]
                    if abs(bird.velocity[0]) < 0.5:
                        bird.velocity[0] = 0
                bird.update()
                bird.render(self.screen)

            for bird in self.birds[1]:
                # if bird.shape.body.position.y < 0:
                #     birds_to_remove.append(bird)
                p = bird.pos
                x, y = p
                x -= 50
                y -= 50
                if self.groundrect.colliderect(pygame.Rect(*bird.pos, *bird.size)):
                    if abs(bird.velocity[1]) < 2:
                        bird.velocity[1] = 0
                        bird.onground = True
                    else:
                        bird.velocity[1] = -bird.velocity[1]*0.5            
                    bird.velocity[0] = bird.velocity[0]*0.8

                    bird.pos[1] = self.groundrect.top - bird.size[1]

                    if abs(bird.velocity[0]) < 0.5:
                        bird.velocity[0] = 0
                bird.update()
                bird.render(self.screen)

            utils.printWaitingList(self)

            self.block1.check_collision(self)
            self.block1.render(self.screen)
            
            pygame.display.update()
            self.clock.tick(60)

Game().run()
