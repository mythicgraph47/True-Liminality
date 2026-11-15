
import asyncio
import pygame
import math
from level1_rooms import get_room, BRICK
from effects import draw_vignette, draw_static, render_glitch_text


class LiminalTraverse:

    def __init__(self):

        pygame.init()

        self.WIDTH, self.HEIGHT = 980, 720

        self.screen = pygame.display.set_mode((self.WIDTH, self.HEIGHT))
        self.clock = pygame.time.Clock()

        #title and icon
        pygame.display.set_caption("Liminal Traverse")
        try:
            self.icon = pygame.image.load("icon.png")
            self.icon = pygame.transform.scale(self.icon, (60, 60))
            pygame.display.set_icon(self.icon)

        except:
            pass

        self.background = pygame.image.load("background2.png")
        self.background = pygame.transform.scale(self.background, (self.WIDTH, self.HEIGHT))

        #fragment (a green triangle flipped down, made from a small pixel grid)
        self.fragment_px = 5
        self.fragmentPattern = [
            "#########",
            ".#######.",
            "..#####..",
            "...###...",
            "....#....",
        ]

        self.fragmentIMG = pygame.Surface((len(self.fragmentPattern[0]) * self.fragment_px, len(self.fragmentPattern) * self.fragment_px), pygame.SRCALPHA)

        for row in range(len(self.fragmentPattern)):
            for col in range(len(self.fragmentPattern[row])):
                if self.fragmentPattern[row][col] == "#":
                    pygame.draw.rect(self.fragmentIMG, (60, 220, 100), (col * self.fragment_px, row * self.fragment_px, self.fragment_px, self.fragment_px))

        #brick image
        self.brick_size = BRICK
        self.brickIMG = pygame.image.load("bricks.png")
        self.brickIMG = pygame.transform.scale(self.brickIMG, (self.brick_size, self.brick_size))

        #slime floor (square blocks, NOT stretched, the player bounces on it)
        self.tile_S = 30
        self.platform_H = 30
        self.bounce_power = -18
        try:
            self.slimeIMG = pygame.image.load("slime.png").convert_alpha()
            self.slimeIMG = self.slimeIMG.subsurface(self.slimeIMG.get_bounding_rect())   #cut the empty transparent part
            self.slimeIMG = pygame.transform.scale(self.slimeIMG, (self.tile_S, self.tile_S))
        except:
            #if slime.png is not in the folder, use a green block
            self.slimeIMG = pygame.Surface((self.tile_S, self.tile_S))
            self.slimeIMG.fill((90, 220, 90))
            pygame.draw.rect(self.slimeIMG, (170, 255, 170), (4, 4, 10, 6))

        #player
        self.playerX = 0
        self.playerY = 0
        self.playerX_change = 0
        self.playerY_change = 0
        self.onGround = False

        self.player_W = 60
        self.player_H = 60
        self.playerIMG = pygame.image.load("playerw.png")
        self.playerIMG = pygame.transform.scale(self.playerIMG, (self.player_W, self.player_H))

        self.speed = 3
        self.gravity = 0.6
        self.jump_power = -13

        self.vignette_radius = 200
        self.static_amount = 40

        #room
        self.rooms = get_room()
        self.roomNumber = 0
        self.current_rooms = self.rooms[self.roomNumber]
        self.walls = self.current_rooms["walls"]
        self.bricks = self.current_rooms["bricks"]
        self.obstacles = self.current_rooms["obstacles"]
        self.fragment = self.current_rooms["fragment"]

        #platform png
        self.platformRECT = pygame.Rect(0, self.HEIGHT - self.platform_H, self.WIDTH, self.platform_H)

        self.playerReset()

        self.running = True
        self.completed = False

    def playerReset(self):

        startBrick = self.bricks[0]
        self.playerX = startBrick.centerx - (self.player_W // 2)
        self.playerY = startBrick.top - self.player_H

        self.playerX_change = 0
        self.playerY_change = 0

    #load a room
    def loadRoom(self, number):

        self.current_rooms = self.rooms[number]
        self.walls = self.current_rooms["walls"]
        self.bricks = self.current_rooms["bricks"]
        self.obstacles = self.current_rooms["obstacles"]
        self.fragment = self.current_rooms["fragment"]
        self.playerReset()

    def drawScene(self):

        self.screen.fill((255, 255, 255))
        self.screen.blit(self.background, (0, 0))

        for brick in self.bricks:
            for blockX in range(brick.left, brick.right, self.brick_size):
                for blockY in range(brick.top, brick.bottom, self.brick_size):
                    self.screen.blit(self.brickIMG, (blockX, blockY))

        #obstacle (red triangle)
        for obstacle in self.obstacles:
            r = obstacle["rect"]
            pygame.draw.polygon(self.screen, (255, 0, 0), [(r.left, r.bottom), (r.right, r.bottom), (r.centerx, r.top)])

        #slime floor
        slimeX = 0
        while slimeX < self.WIDTH:
            self.screen.blit(self.slimeIMG, (slimeX, self.platformRECT.y))
            slimeX += self.tile_S

        #fragment (floats up and down a little)
        fr = int(3 * math.sin(pygame.time.get_ticks() / 200))
        self.screen.blit(self.fragmentIMG, (self.fragment.x, self.fragment.y + fr))

        #playerdraw
        self.screen.blit(self.playerIMG, (self.playerX, self.playerY))

        #effect
        draw_vignette(self.screen, int(self.playerX + self.player_W // 2), int(self.playerY + self.player_H // 2), self.vignette_radius)
        draw_static(self.screen, self.static_amount)

    #die
    async def deathScreen(self):

        font = pygame.font.SysFont(None, 44, bold=True)
        textW, textH = font.size("You died!")
        textW += 2
        text = pygame.Surface((textW, textH), pygame.SRCALPHA)
        render_glitch_text(text, font, "You died!", 0, 0)

        dark = pygame.Surface((self.WIDTH, self.HEIGHT))
        dark.fill((0, 0, 0))
        dark.set_alpha(90)

        maxAlpha = 170
        frames = 90
        for frame in range(frames):
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False
                    return

            if frame < 20:
                alpha = frame * maxAlpha // 20
            elif frame > 60:
                alpha = (frames - frame) * maxAlpha // 30
            else:
                alpha = maxAlpha
            text.set_alpha(alpha)

            self.drawScene()
            self.screen.blit(dark, (0, 0))
            self.screen.blit(text, ((self.WIDTH - textW) // 2, (self.HEIGHT - textH) // 2))
            pygame.display.update()
            self.clock.tick(60)
            await asyncio.sleep(0)

    #player dies
    async def playerDie(self):

        print("You died! Respawning...")
        await self.deathScreen()
        self.playerReset()

    async def nextLevelScreen(self):

        font = pygame.font.SysFont(None, 44, bold=True)
        line1W, line1H = font.size("Next Level:")
        line2W, line2H = font.size("The Liminal Landscape")

        textW = max(line1W, line2W) + 2
        textH = line1H + line2H + 10
        text = pygame.Surface((textW, textH))
        render_glitch_text(text, font, "Next Level:", (textW - line1W) // 2, 0)
        render_glitch_text(text, font, "The Liminal Landscape", (textW - line2W) // 2, line1H + 10)

        small = pygame.transform.smoothscale(text, (int(textW * 0.6), int(textH * 0.6)))
        text = pygame.transform.smoothscale(small, (textW, textH))

        frames = 180
        for frame in range(frames):
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False
                    return

            if frame < 60:
                alpha = frame * 255 // 60
            elif frame > 120:
                alpha = (frames - frame) * 255 // 60
            else:
                alpha = 255
            text.set_alpha(alpha)

            self.screen.fill((0, 0, 0))
            self.screen.blit(text, ((self.WIDTH - textW) // 2, (self.HEIGHT - textH) // 2))
            draw_static(self.screen, self.static_amount)
            pygame.display.update()
            self.clock.tick(60)
            await asyncio.sleep(0)

    #game loop
    async def run(self):

        while self.running:

            self.clock.tick(60)
            await asyncio.sleep(0)

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False

            keys = pygame.key.get_pressed()

            self.playerX_change = 0
            if keys[pygame.K_LEFT] or keys[pygame.K_a]:
                self.playerX_change -= self.speed
            if keys[pygame.K_RIGHT] or keys[pygame.K_d]:
                self.playerX_change += self.speed

            if keys[pygame.K_UP] or keys[pygame.K_w] or keys[pygame.K_SPACE]:
                if self.onGround:
                    print("Jump")
                    self.playerY_change = self.jump_power

            #obstacle move
            for obstacle in self.obstacles:
                rect = obstacle["rect"]
                rect.x += obstacle["speed"]
                if rect.right >= obstacle["max_x"] or rect.left <= obstacle["min_x"]:
                    obstacle["speed"] *= -1

            self.playerX += self.playerX_change
            playerRECT = pygame.Rect(int(self.playerX), int(self.playerY), self.player_W, self.player_H)

            for wall in self.walls + self.bricks:
                if playerRECT.colliderect(wall):
                    if self.playerX_change > 0:
                        self.playerX = wall.left - self.player_W
                    if self.playerX_change < 0:
                        self.playerX = wall.right
                    playerRECT.x = int(self.playerX)

            self.playerY_change += self.gravity
            self.playerY += self.playerY_change
            playerRECT.y = int(self.playerY)
            self.onGround = False

            for wall in self.walls + self.bricks:
                if playerRECT.colliderect(wall):
                    if self.playerY_change > 0:
                        self.playerY = wall.top - self.player_H
                        self.playerY_change = 0
                        self.onGround = True
                    elif self.playerY_change < 0:
                        self.playerY = wall.bottom
                        self.playerY_change = 0
                    playerRECT.y = int(self.playerY)

            #slime floor = bounce up
            if playerRECT.colliderect(self.platformRECT):
                print("Bounce!")
                self.playerY = self.platformRECT.top - self.player_H
                self.playerY_change = self.bounce_power
                playerRECT.y = int(self.playerY)

            #death red triangle
            for obstacle in self.obstacles:
                if playerRECT.colliderect(obstacle["rect"]):
                    await self.playerDie()
                    break

            #collect the green 4 fragment = next level
            if playerRECT.colliderect(self.fragment):
                print("Fragment collected!")
                self.roomNumber += 1
                if self.roomNumber >= len(self.rooms):
                    await self.nextLevelScreen()
                    if self.running:
                        self.completed = True
                    self.running = False
                    break
                self.loadRoom(self.roomNumber)

            self.drawScene()

            pygame.display.update()
