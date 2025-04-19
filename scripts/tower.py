import pygame
import scripts.block as BlockModule

class Tower:
    def __init__(self, game, pos, file):
        self.game = game
        self.pos = pos
        self.grid = 1 #Import from file
        self.towerlist = [[], []]
        self.file = open(file, 'r')
        for line in self.file:
            line = line.strip()
            if line != '':
                for i in range(10):
                    self.towerlist[0].append(BlockModule.Block(game, (pos[0], pos[1] + 50*i), game.filereadhelper[line[i]]))
                    self.towerlist[1].append(BlockModule.Block(game, (pos[0] + 100, pos[1] + 50*i), game.filereadhelper[line[i+10]]))

    def check_collision(self, bird):
        for block_list in self.towerlist:
            mindistfromblock = float('inf')
            mindistblock = None
            for block in block_list:
                dist = (block.rect.centerx - bird.rect.centerx) ** 2 + (block.rect.centery - bird.rect.centery) ** 2
                if dist <= mindistfromblock:
                    mindistfromblock = dist
                    mindistblock = block
            if mindistblock and bird.rect.colliderect(mindistblock.rect):
                mindistblock.check_collision(self.game)

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
