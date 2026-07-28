"""
BEZ GLOBAL:
Gdy Python widzi counter = 5 wewnątrz funkcji, bez global, z góry zakłada: "skoro w tej funkcji przypisujesz
wartość do counter, to counter jest zmienną lokalną dla tej funkcji" - i to dotyczy całego ciała funkcji,
nawet linijek, które są przed tym przypisaniem (stąd czasem UnboundLocalError, jeśli spróbujesz odczytać counter
przed przypisaniem w tej samej funkcji).
Ta lokalna counter = 5 istnieje tylko przez czas trwania wywołania funkcji - to zupełnie inny "byt" niż
modułowa counter = 0, mimo identycznej nazwy. Gdy funkcja się kończy, lokalna counter znika bez śladu, a
modułowa counter = 0 nigdy nie została tknięta.

Z GLOBAL:

Moment 1 - Python czyta definicję funkcji

Zanim funkcja w ogóle zostanie wywołana, Python skanuje jej ciało i widzi linijkę global counter.
To jest deklaracja, nie akcja - Python zapisuje sobie: "OK, wewnątrz tej funkcji, nazwa counter nie ma być
traktowana jak zmienna lokalna. Ilekroć zobaczę counter w tej funkcji - do odczytu czy do przypisania - mam
patrzeć na poziom modułu, nie tworzyć nic nowego lokalnie."

Moment 2 - funkcja zostaje wywołana, Python dochodzi do counter += 1 (albo counter = 5)

Bez global, Python by pomyślał: "przypisanie do counter → stwórz nową, lokalną szufladkę o tej nazwie, żyjącą tylko
 na czas trwania tej funkcji."

Z global, Python myśli inaczej: "mam już zadeklarowane, że counter to nie lokalna sprawa. Idę więc do
przestrzeni nazw modułu (czyli tego samego pliku .py, na poziomie 'poza wszystkimi funkcjami').
Sprawdzam: czy tam już istnieje counter?"

Moment 3a - jeśli zmienna modułowa już istnieje

Python znajduje ją i modyfikuje dokładnie tę samą szufladkę w pamięci, którą widzi reszta programu
(każda inna funkcja, główny kod pliku). Zmiana jest więc "widoczna na zewnątrz" - to dlatego licznik faktycznie
rośnie.

Moment 3b - jeśli zmienna modułowa jeszcze nie istnieje

Python po prostu tworzy ją tam, na poziomie modułu - w tym momencie, z tą wartością. Od teraz istnieje w module,
dostępna też spoza funkcji (o ile ktoś ją odczyta po wywołaniu tej funkcji).
Kluczowa rzecz, którą trzeba zapamiętać z Twojego przypadku: "poziom modułu" to zawsze poziom modułu,
w którym funkcja jest fizycznie zdefiniowana (zapisana w pliku) - nigdy poziom modułu, z którego funkcja
została wywołana. To dwie różne rzeczy, i to jest właśnie to, co Cię wcześniej myliło.

"""


counter = 0  # zmienna na poziomie modułu ("globalna")

def bez_global():
    counter = 5   # BEZ global → Python tworzy NOWĄ, lokalną zmienną counter,
    # niezależną od tej z góry pliku
    print('BEZ GLOBAL WE FUNKCJI',counter) # 5 (ta lokalna)

def z_global():
    global counter # Z global → Python mówi: NIE twórz nowej lokalnej,
    # użyj TEJ z poziomu modułu
    counter = 5
    print('Z GLOBAL WE FUNKCJI',counter)  # 5



bez_global()
print('BEZ GLOBAL',counter)  # 0 - ta z góry pliku nietknięta!

z_global()
print('Z GLOBAL',counter)  # 5 - ta z góry pliku faktycznie zmieniona