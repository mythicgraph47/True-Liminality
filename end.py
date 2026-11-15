import asyncio
import pygame
import effects as brew
ENDING_LINES = [
    "The last fragment settles into your hands.",
    "The hallway. The pool. The void.",
    "None of them were ever real places.",
    "They were only the spaces in between.",
    "You were never lost.",
    "You were just waiting to wake up.",
]

SECONDS_PER_LINE = 3

CREDITS_LINES = [
    "LIMINAL TRAVERSE",
    "",
    "DIRECTED BY",
    "MYTHICGRAPH AND UNCIFYING",
    "",
    "STARRING",
    "SIR NAEEM BILAL",
    "",
    "LOCATIONS",
    "THE CAVERNS",
    "THE HALLWAY",
    "THE POOL",
    "THE VOID",
    "",
    "SPECIAL THANKS",
    "THE SHARDS",
    "",
    "THANK YOU FOR PLAYING",
]

def draw_centered(screen, font, text, y, color=(200, 200, 200)):
    text_width = font.size(text)[0]
    half_screen = screen.get_width() // 2
    half_text = text_width // 2
    x = half_screen - half_text
    brew.render_glitch_text(screen, font, text, x, y, color)

async def play_ending(screen, clock, font, big_font):
    line_index = 0
    line_start = pygame.time.get_ticks()
    finished = False
    credits_y = screen.get_height()
    credits_done = False
    keep_going = True

    while keep_going == True:
        all_events = pygame.event.get()
        for event in all_events:
            if event.type == pygame.QUIT:
                return
            if event.type == pygame.KEYDOWN and finished == True and credits_done == True:
                return

        now = pygame.time.get_ticks()
        time_passed = now - line_start
        if finished == False and time_passed > SECONDS_PER_LINE * 1000:
            line_index = line_index + 1
            line_start = now
            if line_index >= len(ENDING_LINES):
                finished = True

        screen.fill((0, 0, 0))

        if finished == False:
            draw_centered(screen, font, ENDING_LINES[line_index], 280)
        elif credits_done == False:
            credit_number = 0
            for credit_line in CREDITS_LINES:
                line_y = credits_y + credit_number * 40
                if credit_line != "" and line_y > -40 and line_y < screen.get_height():
                    draw_centered(screen, font, credit_line, line_y)
                credit_number = credit_number + 1
            credits_y = credits_y - 2
            last_line_y = credits_y + len(CREDITS_LINES) * 40
            if last_line_y < 0:
                credits_done = True
        else:
            draw_centered(screen, big_font, "THE END", 250)
            draw_centered(screen, font, "Press any key to exit", 330, (100, 100, 100))

        brew.draw_static(screen, intensity=8)
        pygame.display.flip()
        clock.tick(60)
        await asyncio.sleep(0)
