import pygame
import random

def draw_vignette(surface, player_x, player_y, radius=200):
    width = surface.get_width()
    height = surface.get_height()
    left_edge = player_x - radius
    right_edge = player_x + radius
    top_edge = player_y - radius
    bottom_edge = player_y + radius
    if left_edge < 0:
        left_edge = 0
    if top_edge < 0:
        top_edge = 0
    if right_edge > width:
        right_edge = width
    if bottom_edge > height:
        bottom_edge = height
    black = (0, 0, 0)

    if top_edge > 0:
        pygame.draw.rect(surface, black, (0, 0, width, top_edge))
    if bottom_edge < height:
        pygame.draw.rect(surface, black, (0, bottom_edge, width, height - bottom_edge))
    middle_height = bottom_edge - top_edge
    if middle_height > 0:
        if left_edge > 0:
            pygame.draw.rect(surface, black, (0, top_edge, left_edge, middle_height))
        if right_edge < width:
            pygame.draw.rect(surface, black, (right_edge, top_edge, width - right_edge, middle_height))

def draw_static(surface, intensity=5):
    width = surface.get_width()
    height = surface.get_height()  
    counter = 0
    while counter < intensity:
        x = random.randint(0, width)
        y = random.randint(0, height)
        gray = 120
        pygame.draw.rect(surface, (gray, gray, gray), (x, y, 2, 2))
        counter = counter + 1

def render_glitch_text(surface, font, text, x, y, color=(200, 200, 200)):
    red_color = (100, 0, 0)
    shadow = font.render(text, True, red_color)
    shadow_x = x + 2
    shadow_y = y
    surface.blit(shadow, (shadow_x, shadow_y))
    

    main_text = font.render(text, True, color)
    surface.blit(main_text, (x, y))
