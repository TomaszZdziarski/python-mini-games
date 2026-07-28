import random


"""# A) MY APPROACH

things = ["scissors", "lizard","rock", "spock","paper"]
beats = {
    "rock": ["scissors", "lizard"],
    "paper": ["rock", "spock"],
    "scissors": ["paper", "lizard"],
    "lizard": ["spock", "paper"],
    "spock": ["rock", "scissors"],
}

def decide(a, b):
    if a == b:
        return "tie"
    return "player 1" if b in beats[a] else "player 2"


player1score = 0
player2score = 0
ties = 0

for toss in range(1,101):

    a = random.choice(things)
    b = random.choice(things)

    print('Random a value: ',a)
    print('Random b value: ',b)
    result = decide(a,b)
    if result == "player 1":
        player1score +=1
    elif result == "player 2":
        player2score +=1
    else:
        ties +=1
    print(result)
    print('Player 1: ',player1score)
    print('Player 2: ',player2score)
    print('Ties: ',ties)
"""

# B) CLAUDE CODE
"""

things = ["scissors", "lizard", "rock", "spock", "paper"]
beats = {
    "rock": ["scissors", "lizard"],
    "paper": ["rock", "spock"],
    "scissors": ["paper", "lizard"],
    "lizard": ["spock", "paper"],
    "spock": ["rock", "scissors"],
}

def decide(a, b):
    if a == b:
        return "tie"
    return "player 1" if b in beats[a] else "player 2"

scores = {"player 1": 0, "player 2": 0, "tie": 0}

for toss in range(100):
    a = random.choice(things)
    b = random.choice(things)
    result = decide(a, b)
    scores[result] += 1

print(f"Player 1: {scores['player 1']}")
print(f"Player 2: {scores['player 2']}")
print(f"Ties: {scores['tie']}")"""

# C) INPUT VERSION WITH WHILE LOOP EXITING WHEN NEEDED - MY STORY
"""
beats = {
    "rock": ["scissors", "lizard"],
    "paper": ["rock", "spock"],
    "scissors": ["paper", "lizard"],
    "lizard": ["spock", "paper"],
    "spock": ["rock", "scissors"],
}

def decide(player_input, your_input):
    if player_input == your_input:
        return "tie"
    return "player" if your_input in beats[player_input] else "you"

scores = {"player": 0, "you": 0, "tie": 0}




while True:

    player_input = input("What player choose? scissors, lizard, rock, spock, or paper: ").lower()
    your_input = input("Choose your item: scissors, lizard, rock, spock, or paper: ").lower()


    if player_input in beats.keys() and your_input in beats.keys():
        result = decide(player_input,your_input)

        scores[result] += 1

        print("Player: ",scores['player'])
        print("You: ",scores['you'])
        print("Tie: ",scores['tie'])
        print("#################################")

        play_again = input("Do you want to play again? y or n ").lower()

        if play_again == "y":
            continue
        else:
            break

        if scores[result] == 10:
            break

    else:
        print("Your item is not in the game")"""


# C) INPUT VERSION WITH WHILE LOOP EXITING WHEN NEEDED - CLAUDE'S STORY


beats = {
    "rock": ["scissors", "lizard"],
    "paper": ["rock", "spock"],
    "scissors": ["paper", "lizard"],
    "lizard": ["spock", "paper"],
    "spock": ["rock", "scissors"],
}

def decide(player_input, your_input):
    if player_input == your_input:
        return "tie"
    return "player" if your_input in beats[player_input] else "you"

def get_choice(prompt): # spryciarz

    while True:
        choice = input(prompt).lower()
        if choice in beats:
            return choice
        print("Item is not in the game!!!")



match_wins = {"Team Blue": 0, "Team Red": 0, "DRAWS": 0}
team_names = {"player": "Team Blue", "you": "Team Red"}

while True:
    scores = {"player": 0, "you": 0, "tie": 0}
    games=10

    while games !=0:

        player_input = get_choice("What player choose? scissors, lizard, rock, spock, or paper: ")
        your_input = get_choice("Choose your item: scissors, lizard, rock, spock, or paper: ")

        result = decide(player_input,your_input)
        scores[result] +=1

        print(f"Player score:{scores['player']}, Your score: {scores['you']},ties: {scores['tie']}")
        print("#" * 33)

        if scores["player"] == 5 or scores["you"] == 5:
            winner = max(("player", "you"), key=scores.get) # key to klucz do posortowania przedmiotow na liscie, tutaj uzywamy f.get zeslownika scores
            #inny przyklad - tutaj kluczem jest len.  words = ["hi", "banana", "ok", "elephant"]
                        # max(words, key=len) - podaj mi najdluzsze slowo z listy
                        # → "elephant"
                        # every word is considered, but they're COMPARED by their length, not alphabetically
            print(f"{winner} reached 5 and wins the match!")

            winner_team = team_names[winner]          # NEW — translate "player"/"you" into the team name
            match_wins[winner_team] += 1
            print(f"{winner_team} wins the game and has got {match_wins[winner_team]} won matches")

            break
        elif scores["tie"] == 5:
            print("5 ties total — it's a draw!")
            match_wins['DRAWS'] +=1
            break

        games -= 1

    else:
        print("It's undecided so the match ends up as DRAW! ")
        match_wins['DRAWS'] +=1


    # match is over here — show leaderboard, ask to play again
    print("\nFinal scoreboard:")
    print(f"Player: {scores['player']}  You: {scores['you']}  Tie: {scores['tie']}")

    if input("Play again? y or n: ").lower() != "y":
        break



print("Final TEAM LEADERBOARD")
print(f"Team Blue: {match_wins['Team Blue']}, Team Red: {match_wins['Team Red']}, DRAWS: {match_wins['DRAWS']}")