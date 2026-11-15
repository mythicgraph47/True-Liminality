import asyncio
import pygame
import effects

INTRO_TEXT = "Whilst trying to ascend to a higher dimension, you accidentally noclipped into The Liminality. Escape."
PROMPT_TEXT = "Press any key to start the game"
INTRO_SECONDS = 6
FADE_MS = 1000
RED = (200, 30, 30)
GRAY = (150, 150, 150)


def wrap_text(font, text, max_width):
    words = text.split(" ")
    lines = []
    current = ""
    for word in words:
        if current == "":
            test = word
        else:
            test = current + " " + word
        if font.size(test)[0] <= max_width:
            current = test
        else:
            lines.append(current)
            current = word
    if current != "":
        lines.append(current)
    return lines


async def play_intro(screen, clock):
    font = pygame.font.SysFont(None, 28, bold=True)
    small_font = pygame.font.SysFont(None, 22, bold=True)
    width = screen.get_width()
    height = screen.get_height()

    lines = wrap_text(font, INTRO_TEXT, width - 160)
    line_height = font.get_linesize() + 8
    block_height = len(lines) * line_height
    block = pygame.Surface((width, block_height), pygame.SRCALPHA)
    line_number = 0
    for line in lines:
        line_width = font.size(line)[0]
        effects.render_glitch_text(block, font, line, (width - line_width) // 2, line_number * line_height, RED)
        line_number = line_number + 1

    block_y = (height - block_height) // 2 - 30
    prompt_width = small_font.size(PROMPT_TEXT)[0]
    prompt_x = (width - prompt_width) // 2
    prompt_y = block_y + block_height + 50

    start = pygame.time.get_ticks()
    while True:
        elapsed = pygame.time.get_ticks() - start
        ready = elapsed >= INTRO_SECONDS * 1000

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return False
            if event.type == pygame.KEYDOWN and ready:
                return True

        alpha = min(255, elapsed * 255 // FADE_MS)
        block.set_alpha(alpha)

        screen.fill((0, 0, 0))
        screen.blit(block, (0, block_y))
        if ready:
            effects.render_glitch_text(screen, small_font, PROMPT_TEXT, prompt_x, prompt_y, GRAY)
        effects.draw_static(screen, 40)
        pygame.display.flip()
        clock.tick(60)
        await asyncio.sleep(0)
