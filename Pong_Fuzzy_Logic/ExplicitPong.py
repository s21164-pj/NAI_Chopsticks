# Program potrzebuje następujących bibliotek:
# pygame, numpy, matplotlib, keras

# import gry Pong
from PongGame import PongGame
from PongGenome import PongGenome

import matplotlib.pyplot as plt

# Maksymalna liczba klatek
MAX_EVALUATE_FRAMES = 250
# Maksymalna liczba powtórzeń
MAXEPOCHS = 3


def GetFuzzyValues(BallX, BallY, PlayerY, BDirection):
    """ Metoda zwraca "z-fuzz-owane ;D" przybliżone wartości dla:
    - dystans
    - wysokość
    - kierunek wznoszenia (~Kąt toru lotu)

    Nie są one idealne - wymagają dopracowania
    ToDo - Poprawić otrzymywane wartości """

    DString = 'Null'  # Dystans
    HString = 'Same'  # Wysokość
    DirString = 'Null'  # Kierunek wznoszenia

    """
    Wyliczanie dystansu piłki:
    Far  - Daleko
    Med  ~ W połowie
    Near - Bardzo blisko 
    """

    if (BallX >= 175):
        DString = 'Far'
    if ((BallX < 175) and (BallX >= 50)):
        DString = 'Med'
    if (BallX < 50):
        DString = 'Near'

    """
       Wyliczanie wysokości piłki:
       Aboce - Ponad
       Same  - Ten sam poziom
       Below - Poniżej
    """
    DeltaY = (PlayerY + 30) - (BallY + 5)

    if (DeltaY >= 10):
        HString = 'Below'
    if (DeltaY < -10):
        HString = 'Above'

    """
    Wyliczanie wznoszenia/opadania piłki:
       Rising  - Wznosi się piłka
       Falling - Opada piłka 
    """
    if (BDirection < 0):
        DirString = 'Left'
    else:
        DirString = 'Right'

    return DString, HString, DirString

    """
       Główna metoda Fuzzy Logic
    """


def EvaluateGenome(TheGenome):
    FrameTime = 0

    GameHistory = []

    #  Stwórz instancje gry Pong
    TheGame = PongGame()
    #  Inicjalizacja gry
    TheGame.InitialDisplay()

    #  Inicjalizacja kolejnych akcji:
    #  0:pozostań
    #  1:w górę
    #  2:w dół
    AppliedAction = 'S'
    PMissed = False
    GameQuit = False

    #  Główna pętla całej gry
    while ((FrameTime < MAX_EVALUATE_FRAMES) and (not PMissed) and (not GameQuit)):

        # Aktualny stan gry
        [PlayerYPos, BallXPos, BallYPos, BallXDirection, BallYDirection] = TheGame.ReturnCurrentState()
        DValue, HValue, DirValue = GetFuzzyValues(BallXPos, BallYPos, PlayerYPos, BallXDirection)
        AppliedAction = 'S'

        #  Przesuń w górę, swoją "paletką", jeśli piłka jest wyżej, niż "paletka" przeciwnika
        if (PlayerYPos + 30 > BallYPos + 5):
            BestAction = 'U'
        #  Przesuń w dół, swoją "paletką", jeśli piłka jest niżej, niż "paletka" przeciwnika
        if (PlayerYPos + 30 < BallYPos + 5):
            BestAction = 'D'

        #  Użyj FuzzyLogic, aby wybrać odpowiednią akcję
        AppliedAction = TheGenome.RtnAction(HValue, DValue, DirValue)

        if (not (BestAction == AppliedAction)):
            print("Optimum Action: ", BestAction, "  Identified Action: ", AppliedAction, "  Player-Ball: ",
                  (PlayerYPos + 30 - BallYPos + 5))

        #  Zastosuj najbardziej odpowiednią akcję w grze
        FrameCount, PMissed, GameQuit = TheGame.PlayNextMove(AppliedAction)

        #  Przejdź do kolejnej klatki
        FrameTime = FrameTime + 1

    TheGenome.SetScore(FrameTime)

    return GameQuit


def TrainPopulation():
    print()
    print("Tworzenie gracza... ")

    EpochCount = 0
    HighestScore = 0
    TrainQuit = False

    GameHistory = []

    #  Zainicjalizuj i usuń cache genomu Pong-a
    TheGenome = PongGenome()
    TheGenome.Clear()
    #
    #
    print()
    print("Ustawianie ustawień gracza : ")

    # Jeśli piłka powyżej, postaw pong-a w dół
    TheGenome.SetValue('Above', 'Far', 'Left', 'D')
    TheGenome.SetValue('Above', 'Med', 'Left', 'D')
    TheGenome.SetValue('Above', 'Near', 'Left', 'D')
    TheGenome.SetValue('Above', 'Far', 'Right', 'D')
    TheGenome.SetValue('Above', 'Med', 'Right', 'D')
    TheGenome.SetValue('Above', 'Near', 'Right', 'D')

    # Jeśli piłka poniżej, ustaw pong-a w góre
    TheGenome.SetValue('Below', 'Far', 'Left', 'U')
    TheGenome.SetValue('Below', 'Med', 'Left', 'U')
    TheGenome.SetValue('Below', 'Near', 'Left', 'U')
    TheGenome.SetValue('Below', 'Far', 'Right', 'U')
    TheGenome.SetValue('Below', 'Med', 'Right', 'U')
    TheGenome.SetValue('Below', 'Near', 'Right', 'U')

    TheGenome.DisplayGenome()
    TheGenome.DisplayFlat()

    print("*** Włącz uczenie  *** ")

    # Uczenie całej populacji (pongów), przez max epok

    while ((EpochCount < MAXEPOCHS) and (not TrainQuit)):
        TrainQuit = EvaluateGenome(TheGenome)

        EpochCount = EpochCount + 1
        #
        HighestScore = TheGenome.score

        print("Epoka: ", EpochCount, "  Wynik: ", HighestScore)
        GameHistory.append((EpochCount, HighestScore))
    # ======================================
    print("*** Koniec uczenia *** ")

    #  Narysuj wykres wyniku uczenia do epok
    x_val = [x[0] for x in GameHistory]
    y_val = [x[1] for x in GameHistory]

    plt.plot(x_val, y_val)
    plt.xlabel("Epoka ")
    plt.ylabel("Najlepszy wynik")
    plt.show()
    # ==========================
    print()
    print("Najlepszy genom z populacji: ")
    TheGenome.DisplayFlat()
    print()
    TheGenome.DisplayGenome()

    print("******** Koniec ********* ")
    print()


def main():
    TrainPopulation()


if __name__ == "__main__":
    main()
