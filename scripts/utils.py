import pygame
import sys
import math
import numpy as np

# Function to quit game
def QuitGame():
    pygame.quit()
    sys.exit()

# For loading images with proper scaling
def LoadScaledImage(path: str, scaling_factor: float = 1.0, scaling_dim: tuple = (0, 0), removebg: bool = True):
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
        resized_image.set_colorkey((0,0,0))
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
    bigger_rope = 102
    x_redbird = game.x_mouse - 20
    y_redbird = game.y_mouse - 20
    if game.mouse_distance[i] > game.rope_length:
        pux, puy = pu
        pux -= 20
        puy -= 20
        pul = pux, puy
        pu2 = (uv1*bigger_rope+game.sling_x1[i], uv2*bigger_rope+game.sling_y1[i])
        pygame.draw.line(game.screen, (0, 0, 0), (game.sling_x2[i], game.sling_y2[i]), pu2, 5)
        game.screen.blit(game.images[game.current_bird[i]], pul)
        pygame.draw.line(game.screen, (0, 0, 0), (game.sling_x1[i], game.sling_y1[i]), pu2, 5)
    else:
        game.mouse_distance[i] += 10
        pu3 = (uv1*game.mouse_distance[i]+game.sling_x1[i], uv2*game.mouse_distance[i]+game.sling_y1[i])
        pygame.draw.line(game.screen, (0, 0, 0), (game.sling_x2[i], game.sling_y2[i]), pu3, 5)
        game.screen.blit(game.images[game.current_bird[i]], (x_redbird, y_redbird))
        pygame.draw.line(game.screen, (0, 0, 0), (game.sling_x1[i], game.sling_y1[i]), pu3, 5)
    # Angle of impulse
    dy = game.y_mouse - game.sling_y1[i]
    dx = game.x_mouse - game.sling_x1[i]
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
        game.screen.blit(game.images[game.birds_waiting[1][j]], (990 - 70*j, 660))

def between(x, lower, upper, inclusive=True):
    return lower <= x <= upper if inclusive else lower < x < upper

def hoverbutton(xmouse, ymouse):
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
