import pygame
import sys
import math
import numpy as np

# Function to quit game
def QuitGame():
    pygame.quit()
    sys.exit()

# For loading images with proper scaling
def LoadScaledImage(path: str, scaling_factor: float = 1.0, scaling_dim: tuple = (0, 0), removebg: bool = True, bgcolorkey=(0,0,0)):
    BASE_PATH = 'data/images/'
    image = pygame.image.load(BASE_PATH + path)
    if scaling_dim != (0, 0):
        resized_image = pygame.transform.scale(image, scaling_dim)
    elif scaling_factor != 1:
        new_width = int(image.get_width() * scaling_factor)
        new_height = int(image.get_height() * scaling_factor)
        resized_image = pygame.transform.scale(image, (new_width, new_height))
    else:
        resized_image = image
    if removebg:
        resized_image.set_colorkey(bgcolorkey)
    return resized_image

def vector(p0, p1):
    """Return the vector of the points
    p0 = (xo,yo), p1 = (x1,y1)"""
    a = p1[0] - p0[0]
    b = p1[1] - p0[1]
    return (a, b)


def unit_vector(v):
    """Return the unit vector of the points
    v = (a,b)"""
    h = ((v[0]**2)+(v[1]**2))**0.5
    if h == 0:
        h = 0.000000000000001
    ua = v[0] / h
    ub = v[1] / h
    return (ua, ub)


def distance(xo, yo, x, y):
    """distance between points"""
    dx = x - xo
    dy = y - yo
    d = ((dx ** 2) + (dy ** 2)) ** 0.5
    return d

def sling_action(game, player1_active: bool):
    """Set up sling behavior"""
    # Fixing bird to the sling rope
    if player1_active: i = 0
    else: i = 1

    v = vector((game.sling_x1[i], game.sling_y1[i]), (game.x_mouse, game.y_mouse))
    uv = unit_vector(v)
    uv1 = uv[0]
    uv2 = uv[1]
    game.mouse_distance[i] = distance(game.sling_x1[i], game.sling_y1[i], game.x_mouse, game.y_mouse)
    pu = (uv1*game.rope_length+game.sling_x1[i], uv2*game.rope_length+game.sling_y1[i])
    bigger_rope = 70
    x_redbird = game.x_mouse - 25
    y_redbird = game.y_mouse - 25
    if game.mouse_distance[i] > game.rope_length:
        pux, puy = pu
        pux -= 25
        puy -= 25
        pul = pux, puy
        pu2 = (uv1*bigger_rope+game.sling_x1[i], uv2*bigger_rope+game.sling_y1[i])
        pygame.draw.line(game.screen, (0, 0, 0), (game.sling_x2[i], game.sling_y2[i]), pu2, 5)
        if player1_active:
            game.screen.blit(game.images[game.current_bird[i]], pul)
        else:
            game.screen.blit(pygame.transform.flip(game.images[game.current_bird[i]], True, False), pul)
        pygame.draw.line(game.screen, (0, 0, 0), (game.sling_x1[i], game.sling_y1[i]), pu2, 5)
    else:
        game.mouse_distance[i] += 10
        pu3 = (uv1*game.mouse_distance[i]+game.sling_x1[i], uv2*game.mouse_distance[i]+game.sling_y1[i])
        pygame.draw.line(game.screen, (0, 0, 0), (game.sling_x2[i], game.sling_y2[i]), pu3, 5)
        if player1_active:
            game.screen.blit(game.images[game.current_bird[i]], (x_redbird, y_redbird))
        else:
            game.screen.blit(pygame.transform.flip(game.images[game.current_bird[i]], True, False), (x_redbird, y_redbird))
        pygame.draw.line(game.screen, (0, 0, 0), (game.sling_x1[i], game.sling_y1[i]), pu3, 5)
    # Angle of impulse
    dy = game.y_mouse - (game.sling_y1[i] + game.sling_y2[i])/2
    dx = game.x_mouse - (game.sling_x1[i] + game.sling_x2[i])/2
    if dx == 0:
        game.angle[i] = math.pi/2 if dy > 0 else -math.pi/2
    else:
        if dx > 0:
            game.angle[i] = math.atan((float(dy))/dx)
        if dx < 0 and dy >= 0:
            game.angle[i] = math.atan((float(dy))/dx) + math.pi
        if dx < 0 and dy < 0:
            game.angle[i] = math.atan((float(dy))/dx) - math.pi

def InitialiseBirdsWaiting():
    initial = [[], []]
    for i in range(2):
        for j in range(4):
            initial[i].append(np.random.choice(['red', 'yellow', 'blue', 'bomb']))
    return initial

def NextBirdGenerator(game):
    if game.player1_active: i = 0
    else: i = 1
    game.current_bird[i] = game.birds_waiting[i][0]
    game.birds_waiting[i].pop(0)
    game.birds_waiting[i].append(np.random.choice(['red', 'yellow', 'blue', 'bomb']))

def printWaitingList(game):
    for j in range(4):
        game.screen.blit(game.images[game.birds_waiting[0][j]], (400 + 70*j, 660))
    for j in range(4):
        game.screen.blit(pygame.transform.flip(game.images[game.birds_waiting[1][j]], True, False), (990 - 70*j, 660))

def between(x, lower, upper, inclusive=True):
    return lower <= x <= upper if inclusive else lower < x < upper

def hoverbutton(xmouse, ymouse, screentype):
    if screentype == 'mainmenu':
        if (between(xmouse, 320, 420) and between(ymouse, 498, 598)):
            return ['play', True, 314, 'red']
        elif (between(xmouse, 520, 620) and between(ymouse, 498, 598)):
            return ['leaderboard', True, 514, 'blue']
        elif (between(xmouse, 720, 820) and between(ymouse, 498, 598)):
            return ['settings', True, 714, 'yellow']
        elif (between(xmouse, 920, 1020) and between(ymouse, 498, 598)):
            return ['quit', True, 914, 'bomb']
        else:
            return ['bg', False]
    if screentype == 'modeselect':
        if (between(xmouse, 50, 110) and between(ymouse, 50, 110)):
            return ['mainmenu', True]
        elif (between(xmouse, 395, 1045) and between(ymouse, 250, 350)):
            return ['one', True]
        elif (between(xmouse, 395, 1045) and between(ymouse, 450, 550)):
            return ['two', True]
        else:
            return ['bg', False]
    if screentype == 'entername':
        if (between(xmouse, 50, 110) and between(ymouse, 50, 110)):
            return ['mainmenu', True]
        if (between(xmouse, 685, 755) and between(ymouse, 519, 589)):
            return ['continue', True]
        if (between(xmouse, 475, 1015) and between(ymouse, 245, 290)):
            return ['1', False]
        if (between(xmouse, 475, 1015) and between(ymouse, 415, 460)):
            return ['2', False]
        else:
            return ['none', False]
    if screentype == 'leaderboardselect':
        if (between(xmouse, 50, 110) and between(ymouse, 50, 110)):
            return ['back', True]
        elif (between(xmouse, 466, 966) and between(ymouse, 310, 410)):
            return ['one', True]
        elif (between(xmouse, 466, 966) and between(ymouse, 472, 572)):
            return ['two', True]
        else:
            return ['bg', False]
    if screentype == 'leaderboard':
        if (between(xmouse, 50, 110) and between(ymouse, 50, 110)):
            return ['back', True]
        else:
            return ['bg', False]
    if screentype == 'settings':
        if (between(xmouse, 50, 110) and between(ymouse, 50, 110)):
            return ['back', True]
        elif (between(xmouse, 975, 1015) and between(ymouse, 300, 340)):
            return ['bgm', False]
        elif (between(xmouse, 775, 815) and between(ymouse, 370, 410)):
            return ['day', False]
        elif (between(xmouse, 975, 1015) and between(ymouse, 370, 410)):
            return ['night', False]
        elif (between(xmouse, 975, 1015) and between(ymouse, 440, 480)):
            return ['wind', False]
        elif (between(xmouse, 975, 1015) and between(ymouse, 510, 550)):
            return ['dots', False]
        else:
            return ['bg', False]
    if screentype == 'game':
        if (between(xmouse, 50, 110) and between(ymouse, 50, 110)):
            return ['mainmenu', True]
        else:
            return ['bg', False]
        

def rendername(game, screen, name, tile_image, start_pos, align):
    padding = 2
    name = name.upper()
    tile_width, tile_height = tile_image.get_size()
    total_width = ((len(name) + 2) * tile_width)
    borderrect = pygame.Rect(0, 0, total_width + 14, tile_height + 14)

    if align == "right":
        x = start_pos[0] - total_width - 7
    elif align == "center":
        x = start_pos[0] - total_width / 2
    else:
        x = start_pos[0] + 7

    y = start_pos[1]

    borderrect.topleft = (x - 7, y - 7)
    pygame.draw.rect(screen, (240, 188, 60), borderrect)

    screen.blit(tile_image, (x, y))
    x += tile_width

    for letter in name:
        # Draw the tile
        screen.blit(tile_image, (x, y))

        # Render the letter
        char_surf = game.gamefont.render(letter, True, (255, 255, 255))
        char_rect = char_surf.get_rect(center=(x + tile_width/2, y + tile_height/2))
        screen.blit(char_surf, char_rect)

        x += tile_width
    
    screen.blit(tile_image, (x, y))

def get_top_players(filename, gamemode):
    mode1_scores = {}
    mode2_scores = {}

    file = open(filename, 'r')
    for line in file:
        line = line.strip()
        if not line:
            continue

        # First colon → mode, rest
        first_colon_index = line.find(":")

        mode_str = line[:first_colon_index].strip()
        rest = line[first_colon_index + 2:].strip()

        # Last colon → player name, birds used
        last_colon_index = rest.rfind(":")

        name = rest[:last_colon_index].strip()
        birds_str = rest[last_colon_index + 2:].strip()

        mode = int(mode_str)
        birds = int(birds_str)

        # Add to respective mode dict
        if mode == 1:
            if name not in mode1_scores or birds < mode1_scores[name]:
                mode1_scores[name] = birds
        elif mode == 2:
            if name not in mode2_scores or birds < mode2_scores[name]:
                mode2_scores[name] = birds

    # Get top 3 sorted by birds used
    mode1_top = sorted(mode1_scores.items(), key=lambda x: x[1])[:3]
    mode2_top = sorted(mode2_scores.items(), key=lambda x: x[1])[:3]

    if gamemode == 1:
        return mode1_top
    else:
        return mode2_top
