import random

# --- Color palette: name -> RGB tuple ---
COLOR_MAP = {
    "red":    (220, 40, 40),
    "blue":   (40, 90, 220),
    "green":  (40, 160, 60),
    "yellow": (230, 200, 30),
    "brown":  (120, 70, 30),
    "orange": (230, 130, 30),
}

def check_guess(code,guess):

    code_copy = code.copy()
    guess_copy = guess.copy()

    black_pins = 0
    white_pins = 0

    for g in range(len(guess_copy)):
        if guess_copy[g] == code_copy[g]:
            black_pins +=1
            code_copy[g] = "black"
            guess_copy[g] = "burnt"

    for g in range(len(guess_copy)):
        if guess_copy[g] != code_copy[g] and guess_copy[g] != 'burnt' and guess_copy[g] in code_copy:
            white_pins +=1
            code_copy[code_copy.index(guess_copy[g])] = "white"


    return black_pins, white_pins

def reset_game():

    current_guess = []
    current_round = 0
    completed_guesses = []
    pin_score = []
    game_won = False
    game_lost = False
    guess_ready = False
    code = []
    for i in range(4):
        color = random.choice(list(COLOR_MAP.keys()))
        code.append(color)

    return [[],0,[],[],False,False,False,code]







