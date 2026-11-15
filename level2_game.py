import asyncio
import pygame
import random
import effects as brew
import level2_rooms as rooms
import end
import math

class LiminalGame:
    def __init__(self):
        self.width = 980
        self.height = 720   
        self.screen = pygame.display.set_mode((self.width, self.height))
        pygame.display.set_caption("Liminal Traverse")
        self.clock = pygame.time.Clock()
        self.font = pygame.font.SysFont(None, 20, bold=True)
        self.big_font = pygame.font.SysFont(None, 40, bold=True)

        # Game State
        self.running = True
        self.room_list = rooms.get_rooms()
        self.current_room_idx = 0
        self.fragments_needed = 3
        self.fragments_collected = 0
        self.has_shard = False
        self.frame_counter = 0
        self.temp_value = 0

        # Player Setup
        self.player_rect = pygame.Rect(380, 500, 40, 40)
        self.player_speed = 5

        # Fragment Setup
        self.spawn_fragment()

    def spawn_fragment(self):
        # Spawns a red triangle at a random X position at the top
        new_x = random.randint(50, self.width - 50)
        while abs(new_x - self.player_rect.centerx) < 100:
            new_x = random.randint(50, self.width - 50)
        self.frag_x = new_x
        self.frag_y = -50
        self.frag_dx = random.choice([-1, 1]) * random.uniform(3.0, 6.0)
        self.frag_dy = random.uniform(2.0, 4)
        self.frag_rect = pygame.Rect(self.frag_x, self.frag_y, 30, 30)

    def handle_events(self):
        events = pygame.event.get()
        for event in events:
            if event.type == pygame.QUIT:
                self.running = False

    async def update(self):
        current_room = self.room_list[self.current_room_idx]
        room_walls = current_room["walls"]

        keys = pygame.key.get_pressed()
        go_left = False
        go_right = False
        go_up = False
        go_down = False
        if keys[pygame.K_LEFT] == True or keys[pygame.K_a] == True:
            go_left = True
        if keys[pygame.K_RIGHT] == True or keys[pygame.K_d] == True:
            go_right = True
        if keys[pygame.K_UP] == True or keys[pygame.K_w] == True:
            go_up = True
        if keys[pygame.K_DOWN] == True or keys[pygame.K_s] == True:
            go_down = True
        dx = 0
        dy = 0
        if go_left == True:
            dx = dx - self.player_speed
        if go_right == True:
            dx = dx + self.player_speed
        if go_up == True:
            dy = dy - self.player_speed
        if go_down == True:
            dy = dy + self.player_speed

        self.player_rect.x = self.player_rect.x + dx
        wall_number = 0
        while wall_number < len(room_walls):
            wall = room_walls[wall_number]
            if self.player_rect.colliderect(wall) == True:
                if dx > 0:
                    self.player_rect.right = wall.left
                elif dx < 0:
                    self.player_rect.left = wall.right
            wall_number = wall_number + 1

        self.player_rect.y = self.player_rect.y + dy
        wall_number = 0
        while wall_number < len(room_walls):
            wall = room_walls[wall_number]
            if self.player_rect.colliderect(wall) == True:
                if dy > 0:
                    self.player_rect.bottom = wall.top
                elif dy < 0:
                    self.player_rect.top = wall.bottom
            wall_number = wall_number + 1

        if current_room["maze"] == False:
            # 3. Move Fragment
            self.frag_x = self.frag_x + self.frag_dx
            if self.frag_x < 20:
                self.frag_x = 20
                self.frag_dx = -self.frag_dx
            if self.frag_x > self.width - 50:
                self.frag_x = self.width - 50
                self.frag_dx = -self.frag_dx
            self.frag_y = self.frag_y + self.frag_dy
            self.frag_rect.y = self.frag_y
            self.frag_rect.x = self.frag_x

            # Reset fragment if it hits the floor
            if self.frag_y > self.height:
                self.spawn_fragment()

            # 4. Player catches Fragment
            if self.player_rect.colliderect(self.frag_rect) == True:
                self.fragments_collected = self.fragments_collected + 1
                self.spawn_fragment()

                # Check if we can move to the next room
                if self.fragments_collected >= self.fragments_needed:
                    self.fragments_collected = 0
                    self.current_room_idx = self.current_room_idx + 1

                    if self.current_room_idx >= len(self.room_list):
                        await end.play_ending(self.screen, self.clock, self.font, self.big_font)
                        self.running = False
                        return

                    next_room = self.room_list[self.current_room_idx]
                    self.player_rect.topleft = next_room["spawn"]
                    self.has_shard = False
                    self.spawn_fragment()
        else:
            if self.has_shard == False:
                if self.player_rect.colliderect(current_room["shard"]) == True:
                    self.has_shard = True
            if self.player_rect.colliderect(current_room["exit"]) == True:
                if self.has_shard == True:
                    await end.play_ending(self.screen, self.clock, self.font, self.big_font)
                    self.running = False
                    return
                else:
                    self.screen.fill((0, 0, 0))
                    end.draw_centered(self.screen, self.big_font, "YOU SUCK AT THIS GAME", 240, (180, 20, 20))
                    end.draw_centered(self.screen, self.font, "Find the shard first", 310)
                    pygame.display.flip()
                    await asyncio.sleep(2)
                    self.player_rect.topleft = current_room["spawn"]
    def draw(self):
        current_room = self.room_list[self.current_room_idx]
        
        # 1. Draw Background
        self.screen.fill(current_room["bg_color"])

        # 2. Draw Walls
        for wall in current_room["walls"]:
            pygame.draw.rect(self.screen, current_room["wall_color"], wall)

        # 3. Draw Fragment (Red Triangle)
        if current_room["maze"] == False:
            points = [
                (self.frag_x, self.frag_y + 30),
                (self.frag_x + 30, self.frag_y + 30),
                (self.frag_x + 15, self.frag_y)
            ]
            pygame.draw.polygon(self.screen, (150, 20, 20), points)
        else:
            exit_rect = current_room["exit"]
            glow = 150 + int(70 * math.sin(self.frame_counter * 0.1))
            pygame.draw.rect(self.screen, (15, 70, 35), exit_rect)
            pygame.draw.rect(self.screen, (40, glow, 70), (exit_rect.x + 7, exit_rect.y + 5, 36, 45))
            pygame.draw.circle(self.screen, (255, 230, 120), (exit_rect.x + 36, exit_rect.y + 30), 3)
            if self.has_shard == False:
                shard_rect = current_room["shard"]
                shard_points = [
                    (shard_rect.centerx, shard_rect.top),
                    (shard_rect.right, shard_rect.centery),
                    (shard_rect.centerx, shard_rect.bottom),
                    (shard_rect.left, shard_rect.centery)
                ]
                pygame.draw.polygon(self.screen, (0, 220, 200), shard_points)

        # 4. Draw Player (White Square)
        pygame.draw.rect(self.screen, (220, 220, 220), self.player_rect)

        # 5. Apply Liminal Effects (from brew.py)
        player_center_x = self.player_rect.centerx
        player_center_y = self.player_rect.centery
        brew.draw_vignette(self.screen, player_center_x, player_center_y, current_room["vision"])
        brew.draw_static(self.screen, intensity=8)

        # 6. Draw UI
        if current_room["maze"] == True:
            shard_number = 0
            if self.has_shard == True:
                shard_number = 1
            ui_text = "SHARD: " + str(shard_number) + "/1"
        else:
            ui_text = f"FRAGMENTS: {self.fragments_collected}/{self.fragments_needed}"
        brew.render_glitch_text(self.screen, self.font, ui_text, 20, 20)

        room_text = f"LOCATION: {current_room['name']}"
        brew.render_glitch_text(self.screen, self.font, room_text, 20, 50, (100, 100, 100))

        vibe_text = current_room["vibe"]
        vibe_surface = self.font.render(vibe_text, True, (50, 50, 50))
        vibe_x = self.width - vibe_surface.get_width() - 20
        vibe_y = self.height - 40
        self.screen.blit(vibe_surface, (vibe_x, vibe_y))

        pygame.display.flip()

    async def run(self):
        while self.running == True:
            self.handle_events()
            await self.update()
            if self.running == False:
                break
            self.draw()
            self.frame_counter = self.frame_counter + 1
            self.clock.tick(60)
            await asyncio.sleep(0)
