
import random

kolory = ('Pik', 'Kier', 'Trefl', 'Karo')
figury = ('2', '3', '4', '5', '6', '7', '8', '9', '10', 'Walet', 'Krolowa', 'Krol', 'As')
wartosci = {'2': 2, '3': 3, '4': 4, '5': 5, '6': 6, '7': 7, '8': 8,
          '9': 9, '10': 10, 'Walet': 10, 'Krolowa': 10, 'Krol': 10, 'As': 11}

gramy =True

class Karta:
    def __init__(self, kolor, figura):
        self.kolor = kolor
        self.figura = figura

    def __str__(self):
        return self.figura + " "+ self.kolor

class Talia:
    def __init__(self):
        self.talia = []
        for kolor in kolory:
            for figura in figury:
                self.talia.append(Karta(kolor, figura))

    def __str__(self):
        talia_komp = ''
        for karta in self.talia:
            talia_komp += '\n ' + karta.__str__()
        return 'Talia :' + talia_komp

    def tasuj(self):
        random.shuffle(self.talia)

    def dodaj_karte(self):
        dodana_karta = self.talia.pop()
        return dodana_karta

class Gracz:
    def __init__(self):
        self.karty = []
        self.wartosc = 0
        self.asy = 0

    def dobierz_karte(self, kart):
        self.karty.append(kart)
        self.wartosc += wartosci[kart.figura]
        if kart.figura == 'As':
            self.asy += 1

    def wylicz_dla_asa(self):
        while self.wartosc > 21 and self.asy:
            self.wartosc -= 11
            self.asy -= 1

class Zaklady:
    def __init__(self):
        self.calosc = 1000
        self.postawione = 0

    def wygrana(self):
        self.calosc += self.postawione

    def przegrana(self):
        self.calosc -= self.postawione


def przyjmij_zaklad(zaklady):
    while True:
        try:
            zaklady.postawione = int(input('\n Ile chcesz postawic w zakladzie?'))
        except ValueError:
            print('Musi byc postawiona liczba calkowita')
        else:
            if zaklady.postawione > zaklady.calosc:
                print("Hola, hola - nie mozesz postawic wiecej niz kasyno czyli ", zaklady.calosc)
            else:
                break

def uderz(talia, gracz):
    gracz.dobierz_karte(talia.dodaj_karte())
    gracz.wylicz_dla_asa()

def uderz_czekaj(talia, gracz):
    global gramy

    while True:
        zaczynamy = input("\n Teraz twoja kolej - dobierasz czy czekasz? wybierz odpowiednio 'D' lub 'C' ")

        if zaczynamy[0].upper() == 'D':
            uderz(talia, gracz)

        elif zaczynamy[0].upper() == 'C':
            print("Teraz czekasz a gra kasyno")
            gramy = False

        else:
            print("Jeszcze raz, wpisz D lub C")
            continue
        break

def pokaz_karty_gracza(ty, kasyno):
    print('--------------------------------------------')
    print("\nKasyno trzyma dwie karty: ")
    print("#1 <karta kasyna -  nie widzisz >")
    print('#2 ', kasyno.karty[1])
    print('--------------------------------------------')
    print("\nTwoje karty:", *ty.karty, sep=' \n ')
    print('--------------------------------------------')

def pokaz_wszystko(ty, kasyno):
    print("\nKarty kasyna:", *kasyno.karty, sep=' \n ')
    print("Wartosc kasyna =", kasyno.wartosc)
    print("\nTwoje karty:", *ty.karty, sep=' \n ')
    print("Twoja wartosc =", ty.wartosc)

def ty_przegrywasz(ty, kasyno, zaklady):
    print("Niestety przegrales (kasyno zawsze wygrywa)")
    zaklady.przegrana()

def ty_wygrywasz(ty, kasyno, zaklady):
    print("Wygrales :) ! ")
    zaklady.wygrana()

def kasyno_przegrywa(ty, kasyno, zaklady):
    print("Kasyno przegralo")
    zaklady.wygrana()

def kasyno_wygrywa(ty, kasyno, zaklady):
    print("Kasyno wygralo")
    zaklady.przegrana()

def remis(ty, kasyno):
    print("Remis twoj i kasyna")

while True:
    print('\n\
    ----------------------------------------------------------------------------\n\
    Chcesz zagrac w Oczko (21)?  \n\
    Zadaniem gracza jest uzyskać najblizej 21 punktów.  \n\
    Najbardziej ceniony uklad kart to blackjack (czyli As i 10 lub figura) \n\
    Asy maja wartosc 1 lub 11 jest to tzw. soft hand\n\
    Kasyno dobiera karty powyzej 17\n\
    Dobra rada - licz karty aby oszacowac karte kasyna \n\
    ----------------------------------------------------------------------------')

    talia = Talia()
    talia.tasuj()

    ty_gracz = Gracz()
    ty_gracz.dobierz_karte(talia.dodaj_karte())
    ty_gracz.dobierz_karte(talia.dodaj_karte())

    kasyno_gracz = Gracz()
    kasyno_gracz.dobierz_karte(talia.dodaj_karte())
    kasyno_gracz.dobierz_karte(talia.dodaj_karte())

    ty_zaklad = Zaklady()
    przyjmij_zaklad(ty_zaklad)
    pokaz_karty_gracza(ty_gracz,kasyno_gracz)

    while gramy:

        uderz_czekaj(talia, ty_gracz)
        pokaz_karty_gracza(ty_gracz, kasyno_gracz)

        if ty_gracz.wartosc > 21:
            ty_przegrywasz(ty_gracz, kasyno_gracz, ty_zaklad)
            break

    # if ty_gracz.wartosc == 21:
    #     print("\nBlackjack :) ! Wygrales ", ty_zaklad.calosc)
    #     print('\nKarty kasyna to ', kasyno_gracz.wartosc)

    if ty_gracz.wartosc < 21:

        while kasyno_gracz.wartosc < 17:
            uderz(talia, kasyno_gracz)

        pokaz_wszystko(ty_gracz, kasyno_gracz)

        if kasyno_gracz.wartosc > 21:
            kasyno_przegrywa(ty_gracz, kasyno_gracz, ty_zaklad)

        elif kasyno_gracz.wartosc > ty_gracz.wartosc:
            kasyno_wygrywa(ty_gracz, kasyno_gracz, ty_zaklad)

        elif kasyno_gracz.wartosc < ty_gracz.wartosc:
            ty_wygrywasz(ty_gracz, kasyno_gracz, ty_zaklad)

        else:
            remis(ty_gracz, kasyno_gracz)

        # print("\nPlayer current bet value is ", player_chips.total)

    print("\nTwoj stan konta w tym rozdaniu to ", ty_zaklad.calosc)

    nowa_gra = input("Chcesz zrobic kolejny zaklad? Wpisz 'T' dla tak lub cokolwiek aby zakonczyc ")
    try:
        if nowa_gra[0].upper() == 'T':
            gramy = True
            continue
        else:
            print("Ok dziekuje za gre, do zobaczenia")
            break
    except ValueError:
            print('Musi byc T lub cokolwiek')
