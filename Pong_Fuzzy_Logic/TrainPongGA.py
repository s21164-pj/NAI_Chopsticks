# Program potrzebuje następujących bibliotek:
# pygame, numpy, matplotlib, keras

# import gry Pong
from PongGame import PongGame  # import The Pong Game
from PongGenome import PongGenome
#
import random
import matplotlib.pyplot as plt
import operator


MAX_EVALUATE_FRAMES = 500
MAXEPOCHS = 31


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

    if (DeltaY >= 15):
        HString = 'Below'
    if (DeltaY < -15):
        HString = 'Above'

    """
        Wyliczanie wznoszenia/opadania piłki: 
    """
    if (BDirection < 0):
        DirString = 'Left'
    else:
        DirString = 'Right'

    return DString, HString, DirString


def CopyGenome(OriginalGenome):
    NewGenome = PongGenome()
    NewGenome.DistanceValues = OriginalGenome.DistanceValues
    NewGenome.HeightValues = OriginalGenome.HeightValues
    NewGenome.BallDirection = OriginalGenome.BallDirection
    NewGenome.LengthGenome = OriginalGenome.LengthGenome
    NewGenome.score = -1
    NewGenome.PongGN = list(OriginalGenome.PongGN)
    return NewGenome


"""
   Główna metoda Fuzzy Logic
"""
def EvaluateGenome(TheGenome):
    FrameTime = 0

    #  Tworzenie instancji gry Pong
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


        #  Zastosuj najbardziej odpowiednią akcję w grze
        FrameCount, PMissed, GameQuit = TheGame.PlayNextMove(AppliedAction)

        #  Przejdź do kolejnej klatki
        FrameTime = FrameTime + 1

    TheGenome.SetScore(FrameTime)

    return GameQuit


def TrainPopulation():
    print()
    print("Creating Player Population set")

    EpochCount = 0
    HighestScore = 0
    TrainQuit = False

    GameHistory = []

    # Tworzenie najlepszego w historii genomy do zachowania
    BestEverScore = 0
    BestEverGenome = PongGenome()

    # Tworzenie początkowej populacji 14 genomów
    PlayerPopulation = []
    for ix in range(14):
        PlayerPopulation.append(PongGenome())

    print("Wyświetl początkową populację: ")
    for AGenome in PlayerPopulation:
        AGenome.DisplayFlat()

    print("*** Teraz uruchom oceny epoki  *** ")
    # Teraz trenuj całą populację przez MAXEPOCHS
    while ((EpochCount < MAXEPOCHS) and (not TrainQuit)):

        # Do oceny każdego z genomów w populacji
        for AGenome in PlayerPopulation:
            TrainQuit = EvaluateGenome(AGenome)
            if (TrainQuit):
                break

        # Dzielenie populacji na jalepsze wyniki
        PlayerPopulation.sort(key=operator.attrgetter('score'), reverse=True)

        HighestScore = PlayerPopulation[0].score
        # Sprawdź najlepszy w historii genom
        if (HighestScore > BestEverScore):
            BestEverScore = HighestScore
            BestEverGenome = CopyGenome(PlayerPopulation[0])
            BestEverGenome.SetScore(BestEverScore)

        if EpochCount % 5 == 0:
            # Wyświetlanie najlepszego genomu
            print()
            print("Nalepszy obecnie genom: ")
            BestEverGenome.DisplayGenome()
            for AGenome in PlayerPopulation:
                AGenome.DisplayFlat()
            print()

        PlayerPopulation[0] = CopyGenome(BestEverGenome)
        PlayerPopulation[0].SetScore(HighestScore)

        PlayerPopulation[2] = CopyGenome(PlayerPopulation[0])
        PlayerPopulation[2].Mutate()
        PlayerPopulation[3] = CopyGenome(PlayerPopulation[0])
        PlayerPopulation[3].Mutate()
        PlayerPopulation[4] = CopyGenome(PlayerPopulation[0])
        PlayerPopulation[4].Mutate()

        PlayerPopulation[5] = CopyGenome(PlayerPopulation[1])
        PlayerPopulation[5].Mutate()
        PlayerPopulation[6] = CopyGenome(PlayerPopulation[1])
        PlayerPopulation[6].Mutate()
        PlayerPopulation[7] = CopyGenome(PlayerPopulation[1])
        PlayerPopulation[7].Mutate()

        PlayerPopulation[8] = PongGenome()
        PlayerPopulation[8].InheritFromParents(PlayerPopulation[0], PlayerPopulation[1])
        PlayerPopulation[9] = PongGenome()
        PlayerPopulation[9].InheritFromParents(PlayerPopulation[0], PlayerPopulation[1])
        PlayerPopulation[10] = PongGenome()
        PlayerPopulation[10].InheritFromParents(PlayerPopulation[0], PlayerPopulation[1])
        PlayerPopulation[11] = PongGenome()
        PlayerPopulation[11].InheritFromParents(PlayerPopulation[0], PlayerPopulation[1])

        PlayerPopulation[12] = PongGenome()
        PlayerPopulation[13] = PongGenome()

        EpochCount = EpochCount + 1

        print("Epoka: ", EpochCount, "  Najlepszy wynik: ", HighestScore)
        GameHistory.append((EpochCount, HighestScore))

    print("*** Koniec epok testowych*** ")

    #  Narysuj Wynik vs Epoki
    x_val = [x[0] for x in GameHistory]
    y_val = [x[1] for x in GameHistory]

    plt.plot(x_val, y_val)
    plt.xlabel("Epoka ")
    plt.ylabel("Najlepszy wynik")
    plt.show()

    print()
    print("Najlepszy genom: ")
    PlayerPopulation[0].DisplayFlat()
    print()
    PlayerPopulation[0].DisplayGenome()

    print(" *** Rozgrywka najlepszego genomu *** ")
    TrainQuit = EvaluateGenome(PlayerPopulation[0])

    print("******** Koniec ********* ")
    print()



def main():
    # Główna metoda
    TrainPopulation()

if __name__ == "__main__":
    main()
