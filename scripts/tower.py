import pygame
from scripts.block import Block

class Tower:
    def __init__(self, game, pos, file):
        self.game = game
        self.pos = pos
        self.towerlist = [[], []]
        self.file = open(file, 'r')
        for line in self.file:
            line = line.strip()
            if line != '':
                for i in range(10):
                    self.towerlist[0].append(Block(game, (pos[0], pos[1] + 50*i), game.filereadhelper[line[i]]))
                    self.towerlist[1].append(Block(game, (pos[0] + 100, pos[1] + 50*i), game.filereadhelper[line[i+10]]))

    def check_collision(self, bird):
        for block_list in self.towerlist:
            mindistfromblock = float('inf')
            mindistfromblock2 = float('inf')
            mindistblock = None
            mindistblock2 = None
            for block in block_list:
                dist = (block.rect.centerx - bird.rect.centerx) ** 2 + (block.rect.centery - bird.rect.centery) ** 2
                if dist < mindistfromblock:
                    mindistfromblock2 = mindistfromblock
                    mindistblock2 = mindistblock
                    mindistfromblock = dist
                    mindistblock = block
                elif dist < mindistfromblock2:
                    mindistfromblock2 = dist
                    mindistblock2 = block
            
            damagedfromfirstcollision = None
            if mindistblock and bird.rect.colliderect(mindistblock.rect):
                damagedfromfirstcollision = mindistblock.check_collision(self.game, bird, False)
            # if mindistblock2 != mindistblock and abs(mindistfromblock2 - mindistfromblock) < 1000:
            #     if (damagedfromfirstcollision): bird.health += 1
            #     mindistblock2.check_collision(self.game, bird, True)

    def checkifdestroyed(self):
        towerdestroyed = [True, True]
        for i in range(2):
            for block in self.towerlist[i]:
                if block.rect.size != (0,0):
                    towerdestroyed[i] = False
        return all(towerdestroyed)

    def render(self, surf):
        for list in self.towerlist:
            for block in list:
                block.render(self.game.screen)
