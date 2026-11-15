import pygame

WIDTH, HEIGHT = 980, 720
B = 30  
BRICK = 24  


def borders():
   

    return [
        pygame.Rect(0, 0, WIDTH, B),       
        pygame.Rect(0, 0, B, HEIGHT),          
        pygame.Rect(WIDTH, 0, B, HEIGHT),      
    ]


def brickRow(x, y, count):
   
    return pygame.Rect(x, y, count * BRICK, BRICK)


def get_room():
    rooms = []

   
    
    bricks1 = [
        brickRow(30, 520, 5),    #left brci
        brickRow(270, 470, 4),    #brick
        brickRow(510, 430, 4),    #brikc
        brickRow(710, 470, 4),    #bicii
        brickRow(836, 520, 6),    #last brick
        brickRow(836, 420, 3),    # stair up
        brickRow(920, 320, 2),    # stairs up
        # top floor parkour (right to left)
        brickRow(790, 220, 4),
        brickRow(660, 180, 3),
        brickRow(420, 220, 8),    #attackkkkkkkkkkkkkk
        brickRow(260, 170, 3),
        brickRow(140, 220, 3),
        brickRow(30, 170, 3),     # attackkkkkkkkkk againnnnnnn
    ]
    obstacles1 = [
        {   # bottom floor
            "rect": pygame.Rect(300, 400, 50, 20),
            "speed": 4,
            "min_x": 200,
            "max_x": 800,
        },
        {   # top floor
            "rect": pygame.Rect(430, 200, 40, 20),
            "speed": 2,
            "min_x": 420,
            "max_x": 612,
        },
    ]
    rooms.append({
        "name": "Da bounce!",
        "bg_color": (204, 255, 255),
        "color": (255, 255, 204),
        "walls": borders(),
        "bricks": bricks1,
        "obstacles": obstacles1,
        "fragment": pygame.Rect(45, 140, 45, 25),   
    })

    return rooms
