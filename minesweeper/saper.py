"""
dla czytelności warto trzymać jakiś porządek. Sensowny układ dla twojego pliku:

importy
stałe — liczba_wierszy, liczba_kolumn, liczba_min, directions
stan globalny — board, pierwsze_klikniecie
funkcje pomocnicze — policz_sasiadow(), odkryj()
funkcje wysokopoziomowe — klik()
na końcu blok uruchomieniowy / pętla gry
"""

import random
random.seed(7)

directions = [
    (-1, -1), (-1, 0), (-1, 1),
    (0, -1),           (0, 1),
    (1, -1),  (1, 0),  (1, 1)
]





"""board = [
    [ {"mine": False, "revealed": False, "flagged": False, "neighbors": 0},   # board[0][0]
      {"mine": False, "revealed": False, "flagged": False, "neighbors": 0},   # board[0][1]
      {"mine": False, "revealed": False, "flagged": False, "neighbors": 0} ], # board[0][2]

    [ {"mine": False, "revealed": False, "flagged": False, "neighbors": 0},   # board[1][0]
      {"mine": False, "revealed": False, "flagged": False, "neighbors": 0},   # board[1][1]
      {"mine": False, "revealed": False, "flagged": False, "neighbors": 0} ], # board[1][2]
    # ... itd.
]"""


liczba_wierszy = 9
liczba_kolumn = 9
liczba_min = 10

CZYSTE = 0
FLAGA = 1
PYTAJNIK = 2


# 1) PLANSZA

board = [[{"mine": False, "revealed": False, "flagged": 0, "neighbors": 0}
          for col in range(liczba_kolumn)] for row in range(liczba_wierszy)]



# OZNACZANIE PÓL SĄSIEDNICH Z MINĄ, POTRZEBNE DO KLIK

def policz_sasiadow():

    for row in range(liczba_wierszy):
        for col in range(liczba_kolumn):
            for dr, dc in directions:

                neighbour_row = row + dr
                neighbour_col = col + dc

                # WARUNEK BYCIA W ŚRODKU PLANSZY A NIE POZA
                # dopiero tutaj bezpiecznie odwołujemy się do board[neighbour_row][neighbour_col]
                # tu jesteśmy pewni, że sąsiad mieści się w planszy

                if 0 <= neighbour_row < liczba_wierszy and 0 <= neighbour_col < liczba_kolumn:

                    if board[neighbour_row][neighbour_col]['mine'] : # nie musimy kończyć == True bo w pythonie jesli true to istnieje i if jest spełnione
                        board[row][col]['neighbors'] += 1



# FUNCKJA ODKRYWAJĄCA POLA, , POTRZEBNE DO KLIK

def odkryj(row, col):

        if board[row][col]['flagged'] == FLAGA:
            return

        # STRAŻNIK
        if board[row][col]['revealed']:
            return # !!! = NIE WYKONUJ RESZTY CIAŁA FUNKCJI,I właśnie to zatrzymuje odbijanie się A↔B.
            # Kiedy B woła z powrotem A, wywołanie dla A natychmiast się kończy — nie ustawia ponownie revealed,
            # nie idzie do sąsiadów, po prostu znika. Bez tego łańcuch wywołań nigdy by się nie skończył i
            # dostałbyś RecursionError.

        # OZNACZENIE KOMÓRKI JAKO ODSŁONIĘTA
        board[row][col]['revealed'] = True

        # SPRAWDZENIE SĄSIADÓW CZY ONI MAJĄ SĄSIADÓW - REKURENCJA
        if board[row][col]['neighbors'] == 0:
            for dr, dc in directions:

                neighbour_row = row + dr
                neighbour_col = col + dc

                # WARUNEK BYCIA W PLANSZY
                if 0 <= neighbour_row < liczba_wierszy and 0 <= neighbour_col < liczba_kolumn:
                    # WYWOŁANIE F REKURENCYJNEJ DLA SĄSIADÓW = POLA BEZ SĄSIADÓW BĘDĄ ODSŁANIANE JAKO FALA
                    odkryj(neighbour_row,neighbour_col)

# SPRAWDZENIE WYGRANEJ, POTRZEBNE DO KLIK
def czy_wygrana():

    for row in range(liczba_wierszy):
        for col in range(liczba_kolumn):

            # jesli w np.: 5 ruchu gra napotka taki warunek, nie odsloniete pole i pole zawiera mine
            # to zwraca od razu False,czyli nie ma jeszcze wygranej,pozostałe 75 pol nie bedzie dalej sprawdzane,dzieki return
            # Ponizszy warunek to kontrprzykład do pola z mina i pola odkrytego

            if not board[row][col]['revealed'] and not board[row][col]['mine']:
                return False
    # po przejsciu przez wszystkie pola, jesli wewnetrzny return nie przerwie, zwracamy True
    return True

# 2) OBSŁUGA KIKNIECIA/PIERWSZE KLIKNIECIE/ ROZSTAWIENIE MIN

pierwsze_klikniecie = True
gra_skonczona = False

def klik(row,col):
                   # global pierwsze_klikniecie na początku funkcji — mówi Pythonowi, żeby nie tworzył
                   # nazwy lokalnej, tylko sięgał i pisał do tej z zewnątrz(poza,nad funkcją).
                   # global wpływa na zapis. Mówi: „przypisania do tej nazwy w tej funkcji mają trafiać do
                   # zmiennej modułowej, a nie tworzyć nową lokalną".
                   # Bez global linijka pierwsze_klikniecie = False stworzyłaby świeżą zmienną lokalną,
                   # która ginie z końcem funkcji. Zewnętrzna flaga zostałaby na True — i miny rozstawiałyby się
                   # przy każdym kliknięciu od nowa. To był drugi, cichszy skutek, obok UnboundLocalError.

    global pierwsze_klikniecie,gra_skonczona

    if gra_skonczona:
       return
    if board[row][col]['flagged'] == FLAGA:
        return

    if pierwsze_klikniecie:

        wszystkie_pola = [(r, c) for r in range(liczba_wierszy) for c in range(liczba_kolumn)]
        wszystkie_pola.remove((row,col))
        pozycje_min = random.sample(wszystkie_pola,liczba_min)
        print('pozycje min: ', pozycje_min)

        # WSTAWIENIE LOSOWYCH MIN DO PLANSZY:

        for mr,mc in pozycje_min:
            board[mr][mc]['mine'] = True

        # 3) POLICZ SĄSIADÓW

        policz_sasiadow()

        pierwsze_klikniecie = False

    # PRZYKŁAD GUARD CLAUSE = KLAUZULI STRAŻNIKA
    # jeśli jakiś warunek to zrób coś, ale nie stosujemy else tylko w razie nie spelnienia warunku wykonaj
    # linijke ponizej



    if board[row][col]['mine']:

        print('you lost')
        board[row][col]['revealed'] = True
        gra_skonczona = True
        return



    odkryj(row,col)

    if czy_wygrana():
        print('WYGRAŁEŚ!')
        gra_skonczona = True




def flaga(row, col):

    if gra_skonczona:
        return

    if board[row][col]['revealed']:
        return
    # WARUNEK FLAGOWANIA DLA flagged = False/True: board[row][col]['flagged'] = not board[row][col]['flagged']
    # ZAWIJANIE WYNIKÓW 0,1,2 => 1,2,0
    # 1 % 3 = 1 (jedynka nie mieści się w trójce, więc cała zostaje resztą)
    # 2 % 3 = 2
    # 3 % 3 = 0 (trójka mieści się raz, reszty brak)

    board[row][col]['flagged'] = (board[row][col]['flagged'] + 1) % 3




# PRZYKŁADOWE OFLAGOWANIE POLA
flaga(3, 3)

# PRZYKLADOWE WYWOLANIE KLIKNIECIA
klik(4, 4)



# DEBUGG PRINT: POZYCJE MIN I OBLICZONE POLA SĄSIEDNIE

for row in range(liczba_wierszy):
    wiersz_do_wydruku = []
    for col in range(liczba_kolumn):

        if board[row][col]['flagged'] == FLAGA:
            wiersz_do_wydruku.append("F")

        elif board[row][col]['flagged'] == PYTAJNIK:
            wiersz_do_wydruku.append("?")

        # nieodkryte
        elif not board[row][col]['revealed']:
            wiersz_do_wydruku.append("#")
        elif board[row][col]['mine']:
            wiersz_do_wydruku.append("X")
        elif board[row][col]['neighbors'] == 0:
            wiersz_do_wydruku.append(".")
        else:
            wiersz_do_wydruku.append(str(board[row][col]["neighbors"]))
    print(" ".join(wiersz_do_wydruku))

print('#' * 40)

for row in range(liczba_wierszy):
    wiersz_do_wydruku = []
    for col in range(liczba_kolumn):
        if board[row][col]["mine"]:
            wiersz_do_wydruku.append("X")

        else:
            wiersz_do_wydruku.append(str(board[row][col]["neighbors"]))
    print(" ".join(wiersz_do_wydruku))






