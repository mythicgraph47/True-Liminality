import asyncio
import pygame
from intro import play_intro
from level1_game import LiminalTraverse
from level2_game import LiminalGame

async def main():
    pygame.init()
    screen = pygame.display.set_mode((980, 720))
    pygame.display.set_caption("Liminal Traverse")
    clock = pygame.time.Clock()
    
    if await play_intro(screen, clock):
        level1 = LiminalTraverse()
        await level1.run()
        if level1.completed:
            level2 = LiminalGame()
            await level2.run()

asyncio.run(main())
