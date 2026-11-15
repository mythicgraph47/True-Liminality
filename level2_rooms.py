import pygame

def get_rooms():
    rooms = []
    
    # ROOM 1: The Yellow Hallway
    walls1 = [
        pygame.Rect(0, 0, 980, 20),
        pygame.Rect(0, 700, 980, 20),
        pygame.Rect(0, 0, 20, 720),
        pygame.Rect(960, 0, 20, 720),
        pygame.Rect(300, 300, 200, 20) 
    ]
    rooms.append({
        "name": "The Hallway",
        "bg_color": (25, 22, 10),
        "wall_color": (40, 35, 15),
        "vibe": "......",
        "vision": 200,
        "spawn": (380, 500),
        "maze": False,
        "shard": None,
        "exit": None,
        "walls": walls1
    })

    # ROOM 2: The Pool
    walls2 = [
        pygame.Rect(0, 0, 980, 20),
        pygame.Rect(0, 700, 980, 20),
        pygame.Rect(0, 0, 20, 720),
        pygame.Rect(960, 0, 20, 720),
        pygame.Rect(150, 200, 150, 20),
        pygame.Rect(500, 400, 150, 20),
        pygame.Rect(350, 300, 20, 150),
        pygame.Rect(620, 150, 150, 20)
    ]
    rooms.append({
        "name": "The Pool",
        "bg_color": (10, 20, 30),
        "wall_color": (15, 40, 50),
        "vibe": "......",
        "vision": 150,
        "spawn": (380, 500),
        "maze": False,
        "shard": None,
        "exit": None,
        "walls": walls2
    })

    # ROOM 3: The Void
    maze_map = [
        "################",
        "#.#...........##",
        "#.###.#####.####",
        "#...#....S#...##",
        "###.#.#######.##",
        "#E#.#.#...#...##",
        "#.#.###.#.#.#.##",
        "#.#.....#...#.##",
        "#.###########.##",
        "#.............##",
        "################",
        "################"
    ]
    walls3 = []
    shard3 = None
    exit3 = None
    row_number = 0
    for row in maze_map:
        col_number = 0
        for char in row:
            if char == "#":
                walls3.append(pygame.Rect(col_number * 50, row_number * 50, 50, 50))
            if char == "S":
                shard3 = pygame.Rect(col_number * 50 + 15, row_number * 50 + 15, 20, 20)
            if char == "E":
                exit3 = pygame.Rect(col_number * 50, row_number * 50, 50, 50)
            col_number = col_number + 1
        row_number = row_number + 1
    rooms.append({
        "name": "The Void",
        "bg_color": (22, 22, 28),
        "wall_color": (85, 85, 105),
        "vibe": "......",
        "vision": 60,
        "spawn": (55, 55),
        "maze": True,
        "shard": shard3,
        "exit": exit3,
        "walls": walls3
    })

    return rooms
