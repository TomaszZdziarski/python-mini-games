import pygame, sys
from game_of_life import GameOfLife, PATTERNS

CELL  = 12
COLS, ROWS = 80, 60
FPS   = 10

pygame.init()

PANEL_WIDTH = 200
screen = pygame.display.set_mode((COLS * CELL + PANEL_WIDTH, ROWS * CELL))
GRID_WIDTH = COLS * CELL

font = pygame.font.SysFont("Arial", 16)
pygame.display.set_caption("Game of Life")
clock  = pygame.time.Clock()

game   = GameOfLife(ROWS, COLS)

game.randomise()

paused = False
painting = False
last_painted = None
selected_pattern = None

buttons = {
    "Pause":     pygame.Rect(GRID_WIDTH + 10, 10,  180, 35),
    "Clear":     pygame.Rect(GRID_WIDTH + 10, 55,  180, 35),
    "Randomise": pygame.Rect(GRID_WIDTH + 10, 100, 180, 35),
}

pattern_buttons = {}
y = 180
for name in PATTERNS:
    pattern_buttons[name] = pygame.Rect(GRID_WIDTH + 10, y, 180, 35)
    y += 45


def draw_panel(surface, font, paused, selected_pattern, buttons, pattern_buttons):
    pygame.draw.rect(surface, (40, 40, 40), (GRID_WIDTH, 0, PANEL_WIDTH, ROWS * CELL))

    for label, rect in buttons.items():
        color = (70, 70, 70)
        if label == "Pause" and paused:
            color = (180, 100, 0)
        pygame.draw.rect(surface, color, rect, border_radius=6)
        text = font.render(label, True, (220, 220, 220))
        surface.blit(text, (rect.x + 10, rect.y + 10))

    label = font.render("-- Patterns --", True, (150, 150, 150))
    surface.blit(label, (GRID_WIDTH + 10, 155))

    for name, rect in pattern_buttons.items():
        color = (0, 120, 60) if name == selected_pattern else (70, 70, 70)
        pygame.draw.rect(surface, color, rect, border_radius=6)
        text = font.render(name, True, (220, 220, 220))
        surface.blit(text, (rect.x + 10, rect.y + 10))

    instructions = [
        "-- Controls --",
        "SPACE: pause/resume",
        "R: randomise",
        "",
        "-- How to place --",
        "1. Select a pattern",
        "2. Click on the grid",
        "3. Hold to paint",
    ]

    y_text = ROWS * CELL - (len(instructions) * 20) - 10
    for line in instructions:
        text = font.render(line, True, (150, 150, 150))
        surface.blit(text, (GRID_WIDTH + 10, y_text))
        y_text += 20


while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit(); sys.exit()

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE: paused = not paused
            if event.key == pygame.K_r:     game.randomise()

        if event.type == pygame.MOUSEBUTTONDOWN:
            mx, my = event.pos

            if mx >= GRID_WIDTH: # WE ARE OUTSIDE GRID SO IT'S SIDE PANEL
                if buttons["Pause"].collidepoint(mx, my):
                    paused = not paused
                elif buttons["Clear"].collidepoint(mx, my):
                    game.grid = game.empty_grid()
                elif buttons["Randomise"].collidepoint(mx, my):
                    game.randomise()
                else:
                    for name, rect in pattern_buttons.items():
                        if rect.collidepoint(mx, my):
                            selected_pattern = name
                            break
            else: # WE ARE INSIDE GRID SO PAINT
                painting = True
                if selected_pattern:
                    col = mx // CELL
                    row = my // CELL
                    game.place_pattern(PATTERNS[selected_pattern], row, col)
                    last_painted = (row, col)

        if event.type == pygame.MOUSEBUTTONUP:
            if event.button == 1:
                painting = False
                last_painted = None

    if painting and selected_pattern:
        mx, my = pygame.mouse.get_pos()
        if mx < GRID_WIDTH:
            col = mx // CELL
            row = my // CELL
            if (row, col) != last_painted:
                game.place_pattern(PATTERNS[selected_pattern], row, col)
                last_painted = (row, col)

    if not paused:
        game.step()

    screen.fill((20, 20, 20))

    for row in range(ROWS):
        for col in range(COLS):
            if game.grid[row][col]:
                pygame.draw.rect(screen, (0, 200, 100),
                                 (col * CELL, row * CELL, CELL - 1, CELL - 1))

    draw_panel(screen, font, paused, selected_pattern, buttons, pattern_buttons)
    pygame.display.flip()
    clock.tick(FPS)