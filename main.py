import pygame
import sys
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
        pygame.mixer.init()

        pygame.display.set_caption('Angry Birds')
        self.screen = pygame.display.set_mode((1440, 810))

        self.clock = pygame.time.Clock()
        self.game_bg = {'bg': {'day': utils.LoadScaledImage('bg.png', removebg=False), 'night': utils.LoadScaledImage('bgnight.png', removebg=False)},
                        'mainmenu': {'day': utils.LoadScaledImage('mainmenuhover.png', removebg=False), 'night': utils.LoadScaledImage('mainmenuhovernight.png', removebg=False)}}

        self.sfx = {
            'slingshot': pygame.mixer.Sound("data/audio/slingshot.mp3"),
            'redlaunch': pygame.mixer.Sound("data/audio/redlaunch.wav"),
            'bluelaunch': pygame.mixer.Sound("data/audio/bluelaunch.wav"),
            'bluepower': pygame.mixer.Sound("data/audio/bluepower.wav"),
            'yellowlaunch': pygame.mixer.Sound("data/audio/yellowlaunch.wav"),
            'yellowpower': pygame.mixer.Sound("data/audio/yellowpower.wav"),
            'bomblaunch': pygame.mixer.Sound("data/audio/bomblaunch.wav"),
            'bombpower': pygame.mixer.Sound("data/audio/bombpower.wav")
        }

        for value in self.sfx.values():
            value.set_volume(0.5)

        self.images = {
            'tick': utils.LoadScaledImage('tick.png', removebg=False),
            'cloudbig': utils.LoadScaledImage('cloudbig.png', removebg=True, bgcolorkey=(60, 188, 252)),
            'cloudsmall': utils.LoadScaledImage('cloudsmall.png', removebg=True, bgcolorkey=(60, 188, 252)),
            'loadingscreen': utils.LoadScaledImage('loadingbg.png', removebg=False),
            'mainmenu': {'bg': {'day': utils.LoadScaledImage('mainmenu/mainmenu.png', removebg=False), 'night': utils.LoadScaledImage('mainmenu/mainmenunight.png', removebg=False)},
                        'play': {'day': utils.LoadScaledImage('mainmenu/playhover.png', removebg=False), 'night': utils.LoadScaledImage('mainmenu/playhovernight.png', removebg=False)},
                        'leaderboard': {'day': utils.LoadScaledImage('mainmenu/leaderboardhover.png', removebg=False), 'night': utils.LoadScaledImage('mainmenu/leaderboardhovernight.png', removebg=False)},
                        'settings': {'day': utils.LoadScaledImage('mainmenu/settingshover.png', removebg=False), 'night': utils.LoadScaledImage('mainmenu/settingshovernight.png', removebg=False)},
                        'quit': {'day': utils.LoadScaledImage('mainmenu/quithover.png', removebg=False), 'night': utils.LoadScaledImage('mainmenu/quithovernight.png', removebg=False)}},
            'modeselect': {'bg': {'day': utils.LoadScaledImage('modeselect/modeselect.png', removebg=False), 'night': utils.LoadScaledImage('modeselect/modeselectnight.png', removebg=False)},
                        'mainmenu': {'day': utils.LoadScaledImage('modeselect/mainmenuhover.png', removebg=False), 'night': utils.LoadScaledImage('modeselect/mainmenuhovernight.png', removebg=False)},
                        'one': {'day': utils.LoadScaledImage('modeselect/onetowerhover.png', removebg=False), 'night': utils.LoadScaledImage('modeselect/onetowerhovernight.png', removebg=False)},
                        'two': {'day': utils.LoadScaledImage('modeselect/twotowerhover.png', removebg=False), 'night': utils.LoadScaledImage('modeselect/twotowerhovernight.png', removebg=False)}},
            'leaderboardselect': {'bg': {'day': utils.LoadScaledImage('leaderboardselect/bg.png', removebg=False), 'night': utils.LoadScaledImage('leaderboardselect/bgnight.png', removebg=False)},
                                'one': {'day': utils.LoadScaledImage('leaderboardselect/one.png', removebg=False), 'night': utils.LoadScaledImage('leaderboardselect/onenight.png', removebg=False)},
                                'two': {'day': utils.LoadScaledImage('leaderboardselect/two.png', removebg=False), 'night': utils.LoadScaledImage('leaderboardselect/twonight.png', removebg=False)},
                                'back': {'day': utils.LoadScaledImage('leaderboardselect/back.png', removebg=False), 'night': utils.LoadScaledImage('leaderboardselect/backnight.png', removebg=False)}},
            'leaderboard': {1: {'bg': {'day': utils.LoadScaledImage('leaderboardone/bg.png', removebg=False), 'night': utils.LoadScaledImage('leaderboardone/bgnight.png', removebg=False)}, 
                                'back': {'day': utils.LoadScaledImage('leaderboardone/back.png', removebg=False), 'night': utils.LoadScaledImage('leaderboardone/backnight.png', removebg=False)}},
                            2: {'bg': {'day': utils.LoadScaledImage('leaderboardtwo/bg.png', removebg=False), 'night': utils.LoadScaledImage('leaderboardtwo/bgnight.png', removebg=False)},
                                'back': {'day': utils.LoadScaledImage('leaderboardtwo/back.png', removebg=False), 'night': utils.LoadScaledImage('leaderboardtwo/backnight.png', removebg=False)}}},
            'settings': {'bg': {'day': utils.LoadScaledImage('settings/bg.png', removebg=False), 'night': utils.LoadScaledImage('settings/bgnight.png', removebg=False)},
                         'back': {'day': utils.LoadScaledImage('settings/back.png', removebg=False), 'night': utils.LoadScaledImage('settings/backnight.png', removebg=False)}},
            'entername': {'none': {'day': utils.LoadScaledImage('enterplayername/none.png', removebg=False), 'night': utils.LoadScaledImage('enterplayername/nonenight.png', removebg=False)},
                        '1': {'day': utils.LoadScaledImage('enterplayername/1.png', removebg=False), 'night': utils.LoadScaledImage('enterplayername/1night.png', removebg=False)},
                        '2': {'day': utils.LoadScaledImage('enterplayername/2.png', removebg=False), 'night': utils.LoadScaledImage('enterplayername/2night.png', removebg=False)},
                        'continue': {'day': utils.LoadScaledImage('enterplayername/continue.png', removebg=False), 'night': utils.LoadScaledImage('enterplayername/continuenight.png', removebg=False)},
                        '1continue': {'day': utils.LoadScaledImage('enterplayername/1continue.png', removebg=False), 'night': utils.LoadScaledImage('enterplayername/1continuenight.png', removebg=False)},
                        '2continue': {'day': utils.LoadScaledImage('enterplayername/2continue.png', removebg=False), 'night': utils.LoadScaledImage('enterplayername/2continuenight.png', removebg=False)},
                        'mainmenu': {'day': utils.LoadScaledImage('enterplayername/mainmenu.png', removebg=False), 'night': utils.LoadScaledImage('enterplayername/mainmenunight.png', removebg=False)},
                        '1mainmenu': {'day': utils.LoadScaledImage('enterplayername/1mainmenu.png', removebg=False), 'night': utils.LoadScaledImage('enterplayername/1mainmenunight.png', removebg=False)},
                        '2mainmenu': {'day': utils.LoadScaledImage('enterplayername/2mainmenu.png', removebg=False), 'night': utils.LoadScaledImage('enterplayername/2mainmenunight.png', removebg=False)}},
            'red': utils.LoadScaledImage('birds/red.png'),
            'yellow': utils.LoadScaledImage('birds/yellow.png'),
            'blue': utils.LoadScaledImage('birds/blue.png'),
            'bomb': utils.LoadScaledImage('birds/bomb.png'),
            'ground': utils.LoadScaledImage('ground.png'),
            'sling1': utils.LoadScaledImage('sling1.png', removebg=False),
            'sling2': utils.LoadScaledImage('sling2.png', removebg=False),
            'ice': {'ice100': utils.LoadScaledImage('blocks/ice100.png', removebg=False),
                    'ice75': utils.LoadScaledImage('blocks/ice75.png', removebg=False),
                    'ice50': utils.LoadScaledImage('blocks/ice50.png', removebg=False),
                    'ice25': utils.LoadScaledImage('blocks/ice25.png', removebg=False),},
            'wood': {'wood100': utils.LoadScaledImage('blocks/wood100.png', removebg=False),
                    'wood75': utils.LoadScaledImage('blocks/wood75.png', removebg=False),
                    'wood50': utils.LoadScaledImage('blocks/wood50.png', removebg=False),
                    'wood25': utils.LoadScaledImage('blocks/wood25.png', removebg=False)},
            'stone': {'stone100': utils.LoadScaledImage('blocks/stone100.png', removebg=False),
                    'stone75': utils.LoadScaledImage('blocks/stone75.png', removebg=False),
                    'stone50': utils.LoadScaledImage('blocks/stone50.png', removebg=False),
                    'stone25': utils.LoadScaledImage('blocks/stone25.png', removebg=False)},
            'nametile': utils.LoadScaledImage('nametile.png')
        }

        self.filereadhelper = {
            'I': 'ice',
            'W': 'wood',
            'S': 'stone'
        }

        self.groundrect = pygame.Rect(0, self.screen.get_height() - 100, 1440, 100)

        self.sling_x1, self.sling_y1 = [310, 1130], [545, 545]
        self.sling_x2, self.sling_y2 = [360, 1075], [545, 545]
        self.mouse_distance = [0, 0]
        self.rope_length = 60
        self.angle = [0, 0]
        self.x_mouse = 0
        self.y_mouse = 0
        self.count = [0, 0]
        self.mouse_pressed = False
        self.number_of_birds = [0, 0]
        self.birds = [[], []]
        self.birds_waiting = utils.InitialiseBirdsWaiting()
        self.current_bird = [np.random.choice(['red', 'blue', 'yellow', 'blue']), np.random.choice(['red', 'blue', 'yellow', 'blue'])]
        self.t1 = [0, 0]
        self.t2 = [0, 0]
        self.mouse_distance = [0, 0]
        self.player1_active = np.random.choice([True, False])
        self.towers = [TowerModule.Tower(self, (20, 210), 'data/tower1.txt'), TowerModule.Tower(self, (1220, 210), 'data/tower2.txt')]
        self.loadingscreen = True
        self.mainmenu = False
        self.modeselect = False
        self.leaderboardselect = False
        self.leaderboard = False
        self.settings = False
        self.enter_name_screen_active = False
        self.gamerunning = False
        self.someonewon = False
        self.winner_index = -1
        self.gamefont = pygame.font.Font("data/font/PixelifySans-VariableFont_wght.ttf", 30)
        self.hoversound = pygame.mixer.Sound("data/audio/hover.wav")
        self.hoversound.set_volume(1.0)
        self.hovering = False
        self.jumping_bird = BirdModule.Bird(self, 'red', (1440, 0), (50, 50))
        self.mode = None
        self.time_for_delay = 0
        self.player_names = ['', '']
        self.name_entry_active = [False, False]
        self.names_are_empty = [True, True, False] # 3rd boolean value indicates continue once pressed or not
        self.leaderboardfile = open('data/leaderboard.txt', 'a')
        self.wind = False
        self.windeffect = 0
        self.backgroundmode = 'day'
        self.bgm = True
        self.trajdots = False
        

    def run(self):
        self.windeffect = 0

        while True:
            self.game_ticks = pygame.time.get_ticks()
            while self.loadingscreen:
                for event in pygame.event.get():
                    # Quit Game
                    if event.type == pygame.QUIT:
                        utils.QuitGame()
                milpassed = pygame.time.get_ticks()
                if milpassed / 1000 - self.game_ticks / 1000 < 10:
                    self.screen.blit(self.images['loadingscreen'], (0,0))
                    self.screen.blit(self.images['ground'], (0, self.screen.get_height() - 100))
                    barlength = min(500 * 8350/(7.33*1000), 528 * milpassed / ((7.33) * 1000))
                    IntroLoadingBar = utils.LoadScaledImage("loadingbar.png", scaling_dim=(barlength, 46))
                    IntroLoadingBar_rect = IntroLoadingBar.get_rect()
                    self.screen.blit(IntroLoadingBar, (427, 532))

                    redbird = utils.LoadScaledImage('birds/red.png', 1.8)
                    redbird_x = min(400 + barlength, 980)
                    self.screen.blit(redbird, (redbird_x, 510))

                    if not pygame.mixer.music.get_busy():
                        pygame.mixer.music.load('data/audio/loading_screen.wav')
                        pygame.mixer.music.set_volume(0.5)
                        pygame.mixer.music.play()

                    if milpassed / 1000 - self.game_ticks / 1000 > 8:
                        self.loadingscreen = False
                        self.mainmenu = True
                        self.time_for_delay = pygame.time.get_ticks()

                    pygame.display.update()
                    self.clock.tick(60)

            
            while self.mainmenu:
                for event in pygame.event.get():
                    # Quit Game
                    if event.type == pygame.QUIT:
                        utils.QuitGame()
                self.x_mouse, self.y_mouse = pygame.mouse.get_pos()
                hoverbuttonlist = utils.hoverbutton(self.x_mouse, self.y_mouse, 'mainmenu')

                self.screen.blit(self.images['mainmenu'][hoverbuttonlist[0]][self.backgroundmode], (0, 0))
                self.screen.blit(self.images['ground'], (0, self.screen.get_height() - 100))

                if not pygame.mixer.music.get_busy():
                    pygame.mixer.music.load('data/audio/theme.mp3')
                    pygame.mixer.music.set_volume(0.5 if self.bgm else 0)
                    pygame.mixer.music.play()

                if hoverbuttonlist[1] and not self.hovering:
                    self.hovering = True
                    self.hoversound.play()
                    self.jumping_bird.pos = [hoverbuttonlist[2], 447]
                    self.jumping_bird.type = hoverbuttonlist[3]
                    self.jumping_bird.velocity[1] = -6

                if not hoverbuttonlist[1]:
                    self.hovering = False
                    self.jumping_bird.pos = [1440, 0]
                    self.screen.blit(self.images['red'], (314, 447))
                    self.screen.blit(self.images['blue'], (514, 447))
                    self.screen.blit(self.images['yellow'], (714, 447))
                    self.screen.blit(self.images['bomb'], (914, 447))

                if self.hovering:
                    if (self.jumping_bird.pos[1] > 447):
                        self.jumping_bird.velocity[1] = 0
                        self.jumping_bird.pos[1] = 447
                    self.jumping_bird.update()
                    self.jumping_bird.render(self.screen, False)
                    birdstoblit = ['red', 'blue', 'yellow', 'bomb']
                    positions = {'red': 314,
                                 'blue': 514,
                                 'yellow': 714,
                                 'bomb': 914
                    }
                    birdstoblit.remove(hoverbuttonlist[3])
                    for bird in birdstoblit:
                        self.screen.blit(self.images[bird], (positions[bird], 447))

                if pygame.time.get_ticks() - self.time_for_delay > 500:
                    if (pygame.mouse.get_pressed()[0] and hoverbuttonlist[0] == 'play'):
                        self.mainmenu = False
                        self.enter_name_screen_active = True
                        self.time_for_delay = pygame.time.get_ticks()
                        self.player_names = ['', '']
                        self.name_entry_active = [False, False]

                    if (pygame.mouse.get_pressed()[0] and hoverbuttonlist[0] == 'leaderboard'):
                        self.mainmenu = False
                        self.leaderboardselect = True
                        self.time_for_delay = pygame.time.get_ticks()

                    if (pygame.mouse.get_pressed()[0] and hoverbuttonlist[0] == 'settings'):
                        self.mainmenu = False
                        self.settings = True
                        self.time_for_delay = pygame.time.get_ticks()

                    if (pygame.mouse.get_pressed()[0] and hoverbuttonlist[0] == 'quit'):
                        utils.QuitGame()

                pygame.display.update()
                self.clock.tick(60)


            while self.leaderboardselect:
                for event in pygame.event.get():
                    # Quit Game
                    if event.type == pygame.QUIT:
                        utils.QuitGame()

                self.x_mouse, self.y_mouse = pygame.mouse.get_pos()
                hoverbuttonlist = utils.hoverbutton(self.x_mouse, self.y_mouse, 'leaderboardselect')

                self.screen.blit(self.images['leaderboardselect'][hoverbuttonlist[0]][self.backgroundmode], (0, 0))
                self.screen.blit(self.images['ground'], (0, self.screen.get_height() - 100))

                if not pygame.mixer.music.get_busy():
                    pygame.mixer.music.load('data/audio/theme.mp3')
                    pygame.mixer.music.set_volume(0.5 if self.bgm else 0)
                    pygame.mixer.music.play()

                if hoverbuttonlist[1] and not self.hovering:
                    self.hovering = True
                    self.hoversound.play()

                if not hoverbuttonlist[1]:
                    self.hovering = False

                if (pygame.time.get_ticks() - self.time_for_delay > 500):
                    if (pygame.mouse.get_pressed()[0] and hoverbuttonlist[0] == 'back'):
                        self.mainmenu = True
                        self.leaderboardselect = False

                    if (pygame.mouse.get_pressed()[0] and hoverbuttonlist[0] == 'one'):
                        self.leaderboard = True
                        self.leaderboardselect = False
                        self.mode = 1

                    if (pygame.mouse.get_pressed()[0] and hoverbuttonlist[0] == 'two'):
                        self.leaderboard = True
                        self.leaderboardselect = False
                        self.mode = 2

                pygame.display.update()
                self.clock.tick(60)

            while self.leaderboard:
                for event in pygame.event.get():
                    # Quit Game
                    if event.type == pygame.QUIT:
                        utils.QuitGame()

                top3list = utils.get_top_players('data/leaderboard.txt', self.mode)

                self.x_mouse, self.y_mouse = pygame.mouse.get_pos()
                hoverbuttonlist = utils.hoverbutton(self.x_mouse, self.y_mouse, 'leaderboard')

                self.screen.blit(self.images['leaderboard'][self.mode][hoverbuttonlist[0]][self.backgroundmode], (0, 0))
                self.screen.blit(self.images['ground'], (0, self.screen.get_height() - 100))

                for i in range(len(top3list)):
                    nametext = self.gamefont.render(top3list[i][0], True, (0, 0, 0))
                    birdsusedtext = self.gamefont.render(str(top3list[i][1]), True, (0, 0, 0))
                    self.screen.blit(nametext, (489, 414 + 70*i))
                    self.screen.blit(birdsusedtext, (1000 - birdsusedtext.get_width(), 414 + 70*i))

                if not pygame.mixer.music.get_busy():
                    pygame.mixer.music.load('data/audio/theme.mp3')
                    pygame.mixer.music.set_volume(0.5 if self.bgm else 0)
                    pygame.mixer.music.play()

                if hoverbuttonlist[1] and not self.hovering:
                    self.hovering = True
                    self.hoversound.play()

                if not hoverbuttonlist[1]:
                    self.hovering = False

                if (pygame.mouse.get_pressed()[0] and hoverbuttonlist[0] == 'back'):
                    self.leaderboardselect = True
                    self.leaderboard = False
                    self.mode = None
                    self.time_for_delay = pygame.time.get_ticks()

                pygame.display.update()
                self.clock.tick(60)

            while self.settings:
                for event in pygame.event.get():
                    # Quit Game
                    if event.type == pygame.QUIT:
                        utils.QuitGame()

                self.x_mouse, self.y_mouse = pygame.mouse.get_pos()
                hoverbuttonlist = utils.hoverbutton(self.x_mouse, self.y_mouse, 'settings')

                if hoverbuttonlist[0] == 'back':
                    self.screen.blit(self.images['settings']['back'][self.backgroundmode], (0, 0))
                else:
                    self.screen.blit(self.images['settings']['bg'][self.backgroundmode], (0, 0))
                self.screen.blit(self.images['ground'], (0, self.screen.get_height() - 100))

                if not pygame.mixer.music.get_busy():
                    pygame.mixer.music.load('data/audio/theme.mp3')
                    pygame.mixer.music.set_volume(0.5 if self.bgm else 0)
                    pygame.mixer.music.play()

                if hoverbuttonlist[1] and not self.hovering:
                    self.hovering = True
                    self.hoversound.play()

                if not hoverbuttonlist[1]:
                    self.hovering = False

                if (pygame.time.get_ticks() - self.time_for_delay > 500):
                    if pygame.mouse.get_pressed()[0] and not self.mouse_pressed:
                        self.mouse_pressed = True
                        if hoverbuttonlist[0] == 'back':
                            self.mainmenu = True
                            self.settings = False
                            self.time_for_delay = pygame.time.get_ticks()
                            self.mouse_pressed = False
                        if hoverbuttonlist[0] == 'bgm':
                            self.bgm = not self.bgm
                        if hoverbuttonlist[0] == 'day':
                            self.backgroundmode = 'day'
                        if hoverbuttonlist[0] == 'night':
                            self.backgroundmode = 'night'
                        if hoverbuttonlist[0] == 'wind':
                            self.wind = not self.wind
                        if hoverbuttonlist[0] == 'dots':
                            self.trajdots = not self.trajdots
                    if not pygame.mouse.get_pressed()[0]:
                        self.mouse_pressed = False

                if not self.bgm: 
                    pygame.mixer.music.set_volume(0)
                else: 
                    self.screen.blit(self.images['tick'], (975, 300))
                    pygame.mixer.music.set_volume(0.5)

                if self.backgroundmode == 'day':
                    self.screen.blit(self.images['tick'], (775, 370))
                else:
                    self.screen.blit(self.images['tick'], (975, 370))

                if self.wind:
                    self.screen.blit(self.images['tick'], (975, 440))

                if self.trajdots:
                    self.screen.blit(self.images['tick'], (975, 510))

                pygame.display.update()
                self.clock.tick(60)

            while self.enter_name_screen_active:
                for event in pygame.event.get():
                    # Quit Game
                    if event.type == pygame.QUIT:
                        utils.QuitGame()

                if not pygame.mixer.music.get_busy():
                    pygame.mixer.music.load('data/audio/theme.mp3')
                    pygame.mixer.music.set_volume(0.5 if self.bgm else 0)
                    pygame.mixer.music.play()
                
                self.x_mouse, self.y_mouse = pygame.mouse.get_pos()
                hoverbuttonlist = utils.hoverbutton(self.x_mouse, self.y_mouse, 'entername')

                if hoverbuttonlist[1] and not self.hovering:
                    self.hovering = True
                    self.hoversound.play()

                if not hoverbuttonlist[1]:
                    self.hovering = False

                self.screen.blit(self.images['entername']['none'][self.backgroundmode], (0,0))
                self.screen.blit(self.images['ground'], (0, self.screen.get_height() - 100))

                if not self.name_entry_active[0] and not self.name_entry_active[1]:
                    if hoverbuttonlist[1]:
                        self.screen.blit(self.images['entername'][hoverbuttonlist[0]][self.backgroundmode], (0, 0))

                if pygame.time.get_ticks() - self.time_for_delay > 500:
                    if pygame.mouse.get_pressed()[0]:
                        if hoverbuttonlist[0] == '1': self.name_entry_active[0] = True
                        else: self.name_entry_active[0] = False
                    if pygame.mouse.get_pressed()[0]:
                        if hoverbuttonlist[0] == '2': self.name_entry_active[1] = True
                        else: self.name_entry_active[1] = False

                    if self.name_entry_active[0]:
                        if hoverbuttonlist[0] in ['none', '1', '2']:
                            self.screen.blit(self.images['entername']['1'][self.backgroundmode], (0, 0))
                        elif hoverbuttonlist[0] == 'mainmenu':
                            self.screen.blit(self.images['entername']['1mainmenu'][self.backgroundmode], (0, 0))
                        elif hoverbuttonlist[0] == 'continue':
                            self.screen.blit(self.images['entername']['1continue'][self.backgroundmode], (0, 0))
                        for event in pygame.event.get():
                            # Quit Game
                            if event.type == pygame.QUIT:
                                utils.QuitGame()
                            if event.type == pygame.KEYDOWN:
                                if event.key == pygame.K_BACKSPACE:
                                    self.player_names[0] = self.player_names[0][:-1]
                                else:
                                    self.player_names[0] += event.unicode
                        
                    if self.name_entry_active[1]:
                        if hoverbuttonlist[0] in ['none', '1', '2']:
                            self.screen.blit(self.images['entername']['2'][self.backgroundmode], (0, 0))
                        elif hoverbuttonlist[0] == 'mainmenu':
                            self.screen.blit(self.images['entername']['2mainmenu'][self.backgroundmode], (0, 0))
                        elif hoverbuttonlist[0] == 'continue':
                            self.screen.blit(self.images['entername']['2continue'][self.backgroundmode], (0, 0))
                        for event in pygame.event.get():
                            # Quit Game
                            if event.type == pygame.QUIT:
                                utils.QuitGame()
                            if event.type == pygame.KEYDOWN:
                                if event.key == pygame.K_BACKSPACE:
                                    self.player_names[1] = self.player_names[1][:-1]
                                else:
                                    self.player_names[1] += event.unicode

                    for i in range(2):
                        self.player_names[i] = self.player_names[i].strip().upper()

                    if (len(self.player_names[0])) >= 15:
                        errortext1 = self.gamefont.render('NAME LENGTH SHOULD BE < 15!', True, (255, 0, 0))
                        self.screen.blit(errortext1, (420, 302))
                        self.player_names[0] = self.player_names[0][0:15]
                    if (len(self.player_names[1])) >= 15:
                        errortext2 = self.gamefont.render('NAME LENGTH SHOULD BE < 15!', True, (255, 0, 0))
                        self.screen.blit(errortext2, (420, 472))
                        self.player_names[1] = self.player_names[1][0:15]

                    player1name = self.gamefont.render(self.player_names[0], True, (0, 0, 0))
                    self.screen.blit(player1name, (485,249))
                    player2name = self.gamefont.render(self.player_names[1], True, (0, 0, 0))
                    self.screen.blit(player2name, (485,419))

                    self.names_are_empty[0] = not bool(self.player_names[0])
                    self.names_are_empty[1] = not bool(self.player_names[1])

                    self.screen.blit(self.images['ground'], (0, self.screen.get_height() - 100))

                    if pygame.mouse.get_pressed()[0] and hoverbuttonlist[0] == 'continue':
                        if not self.names_are_empty[0] and not self.names_are_empty[1] and len(self.player_names[0]) < 15 and len(self.player_names[1]) < 15 and self.player_names[0] != self.player_names[1]:
                            self.modeselect = True
                            self.enter_name_screen_active = False
                            self.time_for_delay = pygame.time.get_ticks()
                        else:
                            self.names_are_empty[2] = True

                    if self.names_are_empty[2]:
                        if not self.player_names[0]:
                            emptyerrortext1 = self.gamefont.render('PLAYER NAME 1 CANNOT BE EMPTY!', True, (255, 0, 0))
                            self.screen.blit(emptyerrortext1, (485, 249))
                        if not self.player_names[1]:
                            emptyerrortext2 = self.gamefont.render('PLAYER NAME 2 CANNOT BE EMPTY!', True, (255, 0, 0))
                            self.screen.blit(emptyerrortext2, (485, 419))
                        if self.player_names[0] and self.player_names[1] and len(self.player_names[0]) < 15 and len(self.player_names[1]) < 15:
                            if self.player_names[0] == self.player_names[1]:
                                errortext3 = self.gamefont.render('PLAYER NAMES SHOULD BE DIFFERENT!', True, (255, 0, 0))
                                self.screen.blit(errortext3, (420, 302))
                        if self.name_entry_active[0] or self.name_entry_active[1]:
                            self.names_are_empty[2] = False

                    if pygame.mouse.get_pressed()[0] and hoverbuttonlist[0] == 'mainmenu':
                        self.mainmenu = True
                        self.enter_name_screen_active = False

                pygame.display.update()
                self.clock.tick(60)


            while self.modeselect:
                for event in pygame.event.get():
                    # Quit Game
                    if event.type == pygame.QUIT:
                        utils.QuitGame()

                self.x_mouse, self.y_mouse = pygame.mouse.get_pos()
                hoverbuttonlist = utils.hoverbutton(self.x_mouse, self.y_mouse, 'modeselect')

                self.screen.blit(self.images['modeselect'][hoverbuttonlist[0]][self.backgroundmode], (0, 0))
                self.screen.blit(self.images['ground'], (0, self.screen.get_height() - 100))

                if not pygame.mixer.music.get_busy():
                    pygame.mixer.music.load('data/audio/theme.mp3')
                    pygame.mixer.music.set_volume(0.5 if self.bgm else 0)
                    pygame.mixer.music.play()

                if hoverbuttonlist[1] and not self.hovering:
                    self.hovering = True
                    self.hoversound.play()

                if not hoverbuttonlist[1]:
                    self.hovering = False

                if (pygame.time.get_ticks() - self.time_for_delay > 500):
                    if (pygame.mouse.get_pressed()[0] and hoverbuttonlist[0] == 'mainmenu'):
                        self.mainmenu = True
                        self.modeselect = False

                    if (pygame.mouse.get_pressed()[0] and hoverbuttonlist[0] == 'one'):
                        self.gamerunning = True
                        self.modeselect = False
                        self.mode = 1
                        self.time_for_delay = pygame.time.get_ticks()

                    if (pygame.mouse.get_pressed()[0] and hoverbuttonlist[0] == 'two'):
                        self.gamerunning = True
                        self.modeselect = False
                        self.mode = 2
                        self.time_for_delay = pygame.time.get_ticks()

                pygame.display.update()
                self.clock.tick(60)


            while self.someonewon:
                for event in pygame.event.get():
                    # Quit Game
                    if event.type == pygame.QUIT:
                        utils.QuitGame()

                self.x_mouse, self.y_mouse = pygame.mouse.get_pos()
                hoverbuttonlist = utils.hoverbutton(self.x_mouse, self.y_mouse, 'game')

                self.screen.blit(self.game_bg[hoverbuttonlist[0]][self.backgroundmode], (0,0))
                self.screen.blit(self.images['ground'], (0, self.screen.get_height() - 100))
                utils.rendername(self, self.screen, f'{self.player_names[self.winner_index]} won!', self.images['nametile'], (720, 405), 'center')

                if hoverbuttonlist[1] and not self.hovering:
                    self.hovering = True
                    self.hoversound.play()

                if not hoverbuttonlist[1]:
                    self.hovering = False

                if (pygame.mouse.get_pressed()[0] and hoverbuttonlist[0] == 'mainmenu'):
                    self.mainmenu = True
                    self.someonewon = False
                    self.birds = [[], []]
                    self.player1_active = True
                    self.towers = [TowerModule.Tower(self, (20, 210), 'data/tower1.txt'), TowerModule.Tower(self, (1220, 210), 'data/tower2.txt')]
                    self.winner_index = -1
                    self.mode = None
                    self.player_names = ['', '']
                    self.name_entry_active = [False, False]
                    self.names_are_empty = [True, True, False] # 3rd boolean value indicates continue once pressed or not
                    self.leaderboardfile = open('data/leaderboard.txt', 'a')
                    self.number_of_birds = [0, 0]

                pygame.display.update()
                self.clock.tick(60)


            if (self.mode == 1):
                for i in range(2):
                    for block in self.towers[i].towerlist[1-i]:
                        block.health = 0


            while self.gamerunning:
                for event in pygame.event.get():
                    # Quit Game
                    if event.type == pygame.QUIT:
                        utils.QuitGame()
                    # Check mouse pressed in sling 1 area when player 1 active
                    if (pygame.mouse.get_pressed()[0] and self.x_mouse > 230 and
                        self.x_mouse < 430 and self.y_mouse > 430 and self.y_mouse < 630 and self.player1_active):
                        opp2birdinair = False
                        for bird in self.birds[1]:
                            if bird.health > 0:
                                opp2birdinair = True
                                break
                        if not opp2birdinair:
                            if not self.mouse_pressed:
                                self.sfx['slingshot'].play()
                            self.mouse_pressed = True
                    # Check mouse pressed in sling 2 area when player 2 active
                    if (pygame.mouse.get_pressed()[0] and self.x_mouse > 1060 and
                        self.x_mouse < 1260 and self.y_mouse > 430 and self.y_mouse < 630 and not self.player1_active):
                        opp1birdinair = False
                        for bird in self.birds[0]:
                            if bird.health > 0:
                                opp1birdinair = True
                                break
                        if not opp1birdinair:
                            if not self.mouse_pressed:
                                self.sfx['slingshot'].play()
                            self.mouse_pressed = True
                    # Release new bird for current player
                    if (event.type == pygame.MOUSEBUTTONUP and event.button == 1 and self.mouse_pressed):
                        player_index = 0 if self.player1_active else 1
                        self.mouse_pressed = False
                        self.t1[player_index] = time.time() * 1000

                        xo = 310 if player_index == 0 else 1070
                        yo = 510

                        if self.mouse_distance[player_index] > self.rope_length:
                            self.mouse_distance[player_index] = self.rope_length

                        bird = BirdModule.Bird(self, self.current_bird[player_index], (xo, yo), (50, 50))
                        bird.velocity[0] = -self.mouse_distance[player_index] * math.cos(self.angle[player_index]) * 0.37
                        bird.velocity[1] = -self.mouse_distance[player_index] * math.sin(self.angle[player_index]) * 0.37
                        self.birds[player_index].append(bird)
                        self.sfx[self.current_bird[player_index] + 'launch'].play()
                        utils.NextBirdGenerator(self)
                        self.number_of_birds[player_index] += 1
                        self.player1_active = not self.player1_active
                    if (event.type == pygame.MOUSEBUTTONDOWN and event.button == 1):
                        for bird in self.birds[0]:
                            if not bird.power_activated and bird.health > 0:
                                bird.activate_power(0, self)
                        for bird in self.birds[1]:
                            if not bird.power_activated and bird.health > 0:
                                bird.activate_power(0, self)

                self.x_mouse, self.y_mouse = pygame.mouse.get_pos()
                hoverbuttonlist = utils.hoverbutton(self.x_mouse, self.y_mouse, 'game')

                self.windeffect = 100*math.sin(pygame.time.get_ticks()/1000) if self.wind else 0

                self.screen.blit(self.game_bg[hoverbuttonlist[0]][self.backgroundmode], (0,0))
                self.screen.blit(self.images['cloudbig'], (167 + self.windeffect, 158))
                self.screen.blit(self.images['cloudbig'], (1379 + self.windeffect, 360))
                self.screen.blit(self.images['cloudsmall'], (65 + self.windeffect, 640))
                self.screen.blit(self.images['cloudsmall'], (1109 + self.windeffect, 562))
                self.screen.blit(self.images['ground'], (0, self.screen.get_height() - 100))
                self.screen.blit(self.images['sling1'], (302, 510))
                self.screen.blit(self.images['sling2'], (1070, 510))

                if pygame.time.get_ticks() - self.time_for_delay < 2000:
                    if self.player1_active:
                        utils.rendername(self, self.screen, self.player_names[self.winner_index], self.images['nametile'], (720, 405), 'center')
                    else:
                        utils.rendername(self, self.screen, self.player_names[self.winner_index], self.images['nametile'], (720, 405), 'center')
                
                # Render player names on screen
                utils.rendername(self, self.screen, self.player_names[0], self.images['nametile'], (20, 153), 'left')
                utils.rendername(self, self.screen, self.player_names[1], self.images['nametile'], (1420, 153), 'right')

                # Draw not flying birds for player 1
                if self.mouse_pressed and self.player1_active:
                    utils.sling_action(self, self.player1_active)

                    # 🎯 Trajectory Prediction Dots with Fading Alpha
                    start_pos = (310, 510) if self.player1_active else (1070, 510)
                    player_index = 0 if self.player1_active else 1
                    angle = self.angle[player_index]
                    distance = self.mouse_distance[player_index]
                    rope_limit = min(distance, self.rope_length)

                    v0 = rope_limit * 0.37
                    v0x = -v0 * math.cos(angle)
                    v0y = -v0 * math.sin(angle)
                    g = 0.3

                    num_dots = 40
                    for i in range(1, num_dots + 1):
                        t = i * 2  # controls spacing of dots
                        x = start_pos[0] + v0x * t + 25
                        y = start_pos[1] + v0y * t + 0.5 * g * (t ** 2) + 25

                        alpha = max(255 - i * 6, 0)  # gradually decreasing alpha
                        dot_surface = pygame.Surface((16, 16), pygame.SRCALPHA)
                        if self.trajdots:
                            pygame.draw.circle(dot_surface, (255, 255, 255, alpha), (8, 8), 8)
                        self.screen.blit(dot_surface, (x - 8, y - 8))
                else:
                    if time.time()*1000 - self.t1[0] > 300:
                        self.screen.blit(self.images[self.current_bird[0]], (310, 510))
                    else:
                        pygame.draw.line(self.screen, (0, 0, 0), (self.sling_x1[0], self.sling_y1[0]-8),
                                        (self.sling_x2[0], self.sling_y2[0]-7), 5)
                        
                # Draw not flying birds for player 2
                if self.mouse_pressed and not self.player1_active:
                    utils.sling_action(self, self.player1_active)

                    # 🎯 Trajectory Prediction Dots with Fading Alpha
                    start_pos = (310, 510) if self.player1_active else (1070, 510)
                    player_index = 0 if self.player1_active else 1
                    angle = self.angle[player_index]
                    distance = self.mouse_distance[player_index]
                    rope_limit = min(distance, self.rope_length)

                    v0 = rope_limit * 0.37
                    v0x = -v0 * math.cos(angle)
                    v0y = -v0 * math.sin(angle)
                    g = 0.3

                    num_dots = 40
                    for i in range(1, num_dots + 1):
                        t = i * 2  # controls spacing of dots
                        x = start_pos[0] + v0x * t + 25
                        y = start_pos[1] + v0y * t + 0.5 * g * (t ** 2) + 25

                        alpha = max(255 - i * 6, 0)  # gradually decreasing alpha
                        dot_surface = pygame.Surface((16, 16), pygame.SRCALPHA)
                        if self.trajdots:
                            pygame.draw.circle(dot_surface, (255, 255, 255, alpha), (8, 8), 8)
                        self.screen.blit(dot_surface, (x - 8, y - 8))
                else:
                    if time.time()*1000 - self.t1[1] > 300:
                        self.screen.blit(pygame.transform.flip(self.images[self.current_bird[1]], True, False), (1070, 510))
                    else:
                        pygame.draw.line(self.screen, (0, 0, 0), (self.sling_x1[1], self.sling_y1[1]-8),
                                        (self.sling_x2[1], self.sling_y2[1]-7), 5)
                        
                for bird in self.birds[0]:
                    if bird.collided and time.time() - bird.collidingtime > 3:
                        self.birds[0].pop(self.birds[0].index(bird))
                        continue
                    if not utils.between(bird.pos[0], -bird.size[0], self.screen.get_width()) and bird.health > 0:
                        bird.health -= 1
                        bird.collided = True
                        bird.collidingtime = pygame.time.get_ticks()
                    if self.groundrect.colliderect(pygame.Rect(*bird.pos, *bird.size)):
                        bird.health -= 1
                        if (not bird.collided):
                            bird.collided = True
                            bird.collidingtime = time.time()
                        if abs(bird.velocity[1]) < 2:
                            bird.velocity[1] = 0
                            bird.onground = True
                            bird.onwhat = 'ground'
                        else:
                            bird.velocity[1] = -bird.velocity[1]*0.5
                        bird.velocity[0] = bird.velocity[0]*0.6

                        bird.pos[1] = self.groundrect.top - bird.size[1]
                        if abs(bird.velocity[0]) < 0.1:
                            bird.velocity[0] = 0

                    for tower in self.towers:
                        tower.check_collision(bird)

                    if bird.onground and bird.pos[1] < 660:
                        bird.onground = False
                        for tower_obj in self.towers:
                            for block in tower_obj.towerlist[0] + tower_obj.towerlist[1]:
                                if block.rect.colliderect(bird.justbelowrect):
                                    bird.onground = True
                                    bird.pos[1] = block.rect.top - bird.size[1]
                                    bird.rect.y = int(bird.pos[1])
                                    break
                            if bird.onground:
                                break

                    if bird.onground:
                        bird.velocity[1] = 0

                    bird.update()
                    bird.render(self.screen, False)

                for bird in self.birds[1]:
                    if bird.collided and time.time() - bird.collidingtime > 3:
                        self.birds[1].pop(self.birds[1].index(bird))
                        continue
                    if not utils.between(bird.pos[0], -bird.size[0], self.screen.get_width()) and bird.health > 0:
                        bird.health -= 1
                        bird.collided = True
                        bird.collidingtime = pygame.time.get_ticks()
                    if self.groundrect.colliderect(pygame.Rect(*bird.pos, *bird.size)):
                        bird.health -= 1
                        if (not bird.collided):
                            bird.collided = True
                            bird.collidingtime = time.time()
                        if abs(bird.velocity[1]) < 2:
                            bird.velocity[1] = 0
                            bird.onground = True
                        else:
                            bird.velocity[1] = -bird.velocity[1]*0.5            
                        bird.velocity[0] = bird.velocity[0]*0.8

                        bird.pos[1] = self.groundrect.top - bird.size[1]

                        if abs(bird.velocity[0]) < 0.5:
                            bird.velocity[0] = 0

                    for tower in self.towers:
                        tower.check_collision(bird)

                    if bird.onground and bird.pos[1] < 660:
                        bird.onground = False
                        for tower_obj in self.towers:
                            for block in tower_obj.towerlist[0] + tower_obj.towerlist[1]:
                                if block.rect.colliderect(bird.justbelowrect):
                                    bird.onground = True
                                    bird.pos[1] = block.rect.top - bird.size[1]
                                    bird.rect.y = int(bird.pos[1])
                                    break
                            if bird.onground:
                                break
                            
                    bird.update()
                    bird.render(self.screen, True)

                utils.printWaitingList(self)

                for i in range(2):
                    self.towers[i].render(self.screen)
                    if (self.towers[i].checkifdestroyed()):
                        self.winner_index = 1 - i
                        self.gamerunning = False
                        self.someonewon = True
                        self.leaderboardfile.write(f'{self.mode}: {self.player_names[self.winner_index]}: {self.number_of_birds[self.winner_index]}\n')
                        self.leaderboardfile.close()
                        break

                if not pygame.mixer.music.get_busy():
                        pygame.mixer.music.load('data/audio/theme.mp3')
                        pygame.mixer.music.set_volume(0.5 if self.bgm else 0)
                        pygame.mixer.music.play(-1)

                if hoverbuttonlist[1] and not self.hovering:
                    self.hovering = True
                    self.hoversound.play()

                if not hoverbuttonlist[1]:
                    self.hovering = False

                if (pygame.mouse.get_pressed()[0] and hoverbuttonlist[0] == 'mainmenu'):
                    self.mainmenu = True
                    self.gamerunning = False
                    self.birds = [[], []]
                    self.player1_active = True
                    self.towers = [TowerModule.Tower(self, (20, 210), 'data/tower1.txt'), TowerModule.Tower(self, (1220, 210), 'data/tower2.txt')]
                    self.winner_index = -1
                    self.mode = None
                    self.player_names = ['', '']
                    self.name_entry_active = [False, False]
                    self.names_are_empty = [True, True, False] # 3rd boolean value indicates continue once pressed or not
                    self.leaderboardfile = open('data/leaderboard.txt', 'a')
                    self.number_of_birds = [0, 0]

                pygame.display.update()
                self.clock.tick(60)

Game().run()
