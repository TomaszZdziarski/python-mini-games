import pygame
import math
import modules
import random
import sys
import time

# ============================================================
# SETUP — runs once, before the game loop starts
# ============================================================

pygame.init()  # initializes all pygame modules (video, fonts, etc.) — must run first

WIDTH, HEIGHT = 1000, 700
screen = pygame.display.set_mode((WIDTH, HEIGHT))  # creates the window, returns a Surface we can draw on
pygame.display.set_caption("Mastermind")           # sets the window title bar text



# --- Layout constants ---
# These never change frame to frame, so they're defined once here,
# not recomputed 60 times a second inside the loop.

peg_radius   = 20   # radius of each peg circle, in pixels
peg_spacing  = 60   # horizontal distance between one peg's center and the next
start_x      = 60   # x-coordinate of the first peg in each board row
start_y      = 60   # y-coordinate of the first board row
row_spacing  = 50   # vertical distance between one board row and the next
palette_x = WIDTH - 580  # 100 px marginesu od prawej krawędzi  # x-coordinate of the first palette swatch
palette_y    = 60   # y-coordinate of the palette row


# CZARNE/BIAŁE PINY

pin_black_color = (20, 20, 20)     # niemal czarny
pin_white_color = (230, 230, 230)  # niemal biały
pin_small_radius = 6               # mniejszy promień niż peg_radius (20)


# FONTY

pygame.font.init()  # inicjalizacja modułu fontów (podobnie jak pygame.init())
font = pygame.font.SysFont(None, 28)  # None = domyślny font systemowy, 28 = rozmiar w pikselach

# --- Game state ---
# These DO change during play, which is why they live outside the loop
# (so they persist across frames) but get read/written inside it.

current_guess = []   # colors clicked so far for the row currently being played
current_round = 0    # which board row is currently in progress
guess_ready = False
completed_guesses = []
pin_score = []
code = []
game_won = False
game_lost = False
line_height = 30
win_time = 0
loose_time = 0
passed = 0


for i in range(4):
    color = random.choice(list(modules.COLOR_MAP.keys()))
    code.append(color)
print(code)

instructions = [
    "                                 Witaj w Mastermind! ",
    "                                                     ",
    "  Zgadnij tajny kod 4 kolorow (kolor może się powtarzać).",
    "  Czarna pinezka = trafiony kolor na właściwym miejscu.",
    "  Biała pinezka = trafiony kolor, złe miejsce.",
    "                                                     ",
    "                                               Autor: Tomasz Zdziarski",
]



# ============================================================
# GAME LOOP — repeats every frame until the window is closed
# ============================================================


running = True
while running:


    # --------------------------------------------------------
    # 1. EVENT HANDLING — react to things that just happened
    #    (a click, a keypress, the window's X button)
    # --------------------------------------------------------


    for event in pygame.event.get():

        # QUIT EVENT
        if event.type == pygame.QUIT:
            running = False  # loop exits after this iteration

        # QUIT EVENT
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_n:
                running = False  # loop exits after this iteration



        # PLAY AGAIN EVENT
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_y:
                current_guess,current_round,completed_guesses,pin_score,game_won,game_lost,guess_ready,code = modules.reset_game()
                print('new code=',code)


        # --- Click detection: was a palette swatch clicked? ---
        if event.type == pygame.MOUSEBUTTONDOWN:
            x1, y1 = event.pos  # mouse position at time of click

            for i, color in enumerate(modules.COLOR_MAP):
                y = palette_y + (i * peg_spacing)
                distance = math.sqrt((y - y1) ** 2 + (palette_x - x1) ** 2)

                if distance < peg_radius:

                    # --- State change: record the guessed color ---

                    if len(current_guess) < 4 and not game_won and not game_lost:
                        current_guess.append(color)
                        print(f"color {color}")

                        # --- State change: advance to next round once guess is full ---
                        if len(current_guess) == 4:

                            current_round += 1

                            my_copy = current_guess.copy()
                            completed_guesses.append(my_copy)

                            score = modules.check_guess(code,my_copy)
                            b,w = score

                            if b == 4 and w == 0:

                                # OGŁOSZENIE ZWYCIĘSTWA
                                game_won = True
                                win_time = pygame.time.get_ticks()

                            if current_round > 9 and not game_won:

                                # OGŁOSZENIE PORAŻKI
                                game_lost = True
                                loose_time = pygame.time.get_ticks()


                            pin_score.append(score)



                            guess_ready = True
                            current_guess = []


    # --------------------------------------------------------
    # 2. DRAWING — redraws EVERYTHING, every frame, from scratch.
    #    Nothing here reacts to events directly; it just paints
    #    the screen based on current state.
    # --------------------------------------------------------

    # 1 --- Background: erases whatever was drawn last frame ---

    screen.fill((90, 90, 100))  # dark blue-gray, RGB

    if game_won:

        text_surface = font.render('BRAWO! ODGADŁEŚ KOD! CHCESZ ZAGRAĆ JESZCZE RAZ?  Y / N ? ', True, (255,255,255))
        screen.blit(text_surface, (200, 600))


        current_time = pygame.time.get_ticks()
        passed = current_time - win_time
        all_seconds = passed // 1000

        remaining_seconds = 10-all_seconds

        text_surface = font.render(f'PROGRAM ZAMKNIE SIĘ AUTOMATYCZNIE ZA: {remaining_seconds} SEKUND', True, (255,255,255))
        screen.blit(text_surface, (200, 650))

        if all_seconds == 10:
            running = False



    if game_lost:

        text_surface = font.render('GAME OVER!!! CHCESZ ZAGRAĆ JESZCZE RAZ?  Y / N ? ', True, (255,255,255))
        screen.blit(text_surface, (200, 600))


        current_time = pygame.time.get_ticks()

        passed = current_time - loose_time
        all_seconds = passed // 1000

        remaining_seconds = 10-all_seconds

        text_surface = font.render(f'PROGRAM ZAMKNIE SIĘ AUTOMATYCZNIE ZA: {remaining_seconds} SEKUND', True, (255,255,255))
        screen.blit(text_surface, (200, 650))

        if all_seconds == 10:
            running = False



    # tytuł i instrukcje

    for i, line in enumerate(instructions):
        line_surface = font.render(line, True, (255, 255, 255))
        screen.blit(line_surface, (450, 150 + i * line_height))


    # 2 --- Empty 10x4 board (hollow pegs) ---

    for row in range(10):                    # one iteration per round
        y = start_y + row * row_spacing

        # numer rundy
        text_surface = font.render(str(row + 1), True, (255,255,255))
        screen.blit(text_surface, (peg_radius-10, y-10))  # "wklejenie" tej mini-grafiki na ekran w danym miejscu

        for col in range(4):                  # one iteration per peg in the row
            x = start_x + col * peg_spacing
            pygame.draw.circle(
                screen,
                (200, 200, 200),
                (x, y),
                peg_radius,
                width=2  # outline only — hollow ring, not filled
            )

    # 3 --- Color palette (filled swatches) ---

    for i, color in enumerate(modules.COLOR_MAP):
        y = palette_y + (i * peg_spacing)
        pygame.draw.circle(screen, modules.COLOR_MAP[color], (palette_x, y), peg_radius)

    # 4 --- Completed guesses to show ---
    #if guess_ready:


    for i, colors in enumerate(completed_guesses): # który wiersz

        y = start_y + i * row_spacing # do przesuniecia góra/dół używasz iteratora i z enumerated list of lists (która lista)
        for j,color in enumerate(colors): # który kolor/która pinezka w wierszu
            x = start_x + (j * peg_spacing) # więc do przesunięcia o x w prawo/lewo używasz numeracji z j

            pygame.draw.circle(screen, modules.COLOR_MAP[color], (x,y), peg_radius)

        black,white = pin_score[i] #
        score_x = start_x + 4 * peg_spacing + 20  # start klastra z białymi i czarnymi, kawałek za ostatnią dużą pinezką


        for k in range(black):
            px = score_x + k * (pin_small_radius * 2 + 4)
            pygame.draw.circle(screen, pin_black_color, (px,y), pin_small_radius)

        for k in range(white):
            px = score_x + (black + k) * (pin_small_radius * 2 + 4)
            pygame.draw.circle(screen, pin_white_color, (px,y), pin_small_radius)

    if current_guess:
        for i, color in enumerate(current_guess):
            y = start_y + current_round * row_spacing
            x = start_x + (i * peg_spacing)
            pygame.draw.circle(screen, modules.COLOR_MAP[color], (x, y), peg_radius)




    # --------------------------------------------------------
    # 3. FLIP — pushes everything drawn this frame to the actual display
    # --------------------------------------------------------
    pygame.display.flip()


pygame.quit()  # cleans up pygame resources once the loop has ended
sys.exit()