"""
Podstawowa klasa genomu
"""
import random
class PongGenome:
    def __init__(self):
        self.HeightValues = ('Above', 'Same', 'Below')  # tuple
        self.DistanceValues = ('Far', 'Med', 'Near')  # tuple
        self.BallDirection = ('Left', 'Right')

        self.LengthGenome = len(self.HeightValues) * len(self.DistanceValues) * len(self.BallDirection)
        self.score = -11
        # dla celów wyświetlania
        self.PongGN = ['S' for ix in range(self.LengthGenome)]

        # Randomizacja wartości początkowych
        for ix in range(self.LengthGenome):
            rdm = random.randrange(100)
            if (rdm > 66):
                self.PongGN[ix] = 'U'
            elif (rdm < 33):
                self.PongGN[ix] = 'D'

    def SetValue(self, Height, Distance, Direction, NewValue):
        GIndex = self.BallDirection.index(Direction) * len(self.DistanceValues) * len(
            self.HeightValues) + self.HeightValues.index(Height) * len(self.DistanceValues) + self.DistanceValues.index(
            Distance)
        self.PongGN[GIndex] = NewValue

    def Clear(self):
        for ix in range(self.LengthGenome):
            self.PongGN[ix] = 'S'

    def RtnAction(self, Height, Distance, Direction):
        GIndex = self.BallDirection.index(Direction) * len(self.DistanceValues) * len(
            self.HeightValues) + self.HeightValues.index(Height) * len(self.DistanceValues) + self.DistanceValues.index(
            Distance)
        return self.PongGN[GIndex]

    def RtnAction(self, Height, Distance, Direction):
        GIndex = self.BallDirection.index(Direction) * len(self.DistanceValues) * len(
            self.HeightValues) + self.HeightValues.index(Height) * len(self.DistanceValues) + self.DistanceValues.index(
            Distance)
        return self.PongGN[GIndex]

    def SetScore(self, NewScore):
        self.score = NewScore

    def Mutate(self):
        index_mutate = int(random.random() * len(self.PongGN))
        rdm = random.randrange(100)
        if (rdm > 66):
            self.PongGN[index_mutate] = 'U'
        elif (rdm < 33):
            self.PongGN[index_mutate] = 'D'
        else:
            self.PongGN[index_mutate] = 'S'

        #  ****  No Flip state, as Action is Tri State value -- Makes awkard for a Flip

    def InheritFromParents(self, Parent1, Parent2):

        SplitPoint1 = int(random.randrange(0, len(self.PongGN) // 2))  # // is an integer division
        SplitPoint2 = int(random.randrange(SplitPoint1, len(self.PongGN)))

        Parentchoice = (random.randrange(100) > 50)  # Binary random Choice

        # Up To Split Point1
        for ix in range(0, SplitPoint1):
            if (Parentchoice):
                self.PongGN[ix] = Parent1.PongGN[ix]
            else:
                self.PongGN[ix] = Parent2.PongGN[ix]
                # Between Split Points
        for ix in range(SplitPoint1, SplitPoint2):
            if (Parentchoice):
                self.PongGN[ix] = Parent2.PongGN[ix]
            else:
                self.PongGN[ix] = Parent1.PongGN[ix]
                # Beyond second Split Point
        for ix in range(SplitPoint2, len(self.PongGN)):
            if (Parentchoice):
                self.PongGN[ix] = Parent1.PongGN[ix]
            else:
                self.PongGN[ix] = Parent2.PongGN[ix]

    def DisplayGenome(self):
        print("\tLeft Direction Values: \t\tRight DirectionValues: ")
        header = str(self.score) + "\t"
        for hdri in range(len(self.DistanceValues)):
            header = header + self.DistanceValues[hdri] + "\t"
        header = header + "\t"
        for hdri in range(len(self.DistanceValues)):
            header = header + self.DistanceValues[hdri] + "\t"
        print(header)
        # Dukuje wartość wiersza
        for rowi in range(len(self.HeightValues)):
            rowstring = self.HeightValues[rowi] + "\t"

            # Pierwsza połowa genomu
            for hdri in range(len(self.DistanceValues)):
                rowstring = rowstring + self.PongGN[rowi * len(self.DistanceValues) + hdri] + "\t"

            rowstring = rowstring + "\t"
            # Druga połowa genomu
            for hdri in range(len(self.DistanceValues)):
                rowstring = rowstring + self.PongGN[
                    len(self.HeightValues) * len(self.DistanceValues) + rowi * len(self.DistanceValues) + hdri] + "\t"

            print(rowstring)

    def DisplayFlat(self):
        GString = str(self.score) + "\t"
        # dolna część genomu - kierunek
        for rowi in range(len(self.HeightValues)):
            for hdri in range(len(self.DistanceValues)):
                GString = GString + self.PongGN[rowi * len(self.HeightValues) + hdri]

        GString = GString + " "
        # kolejna część genomu
        for rowi in range(len(self.HeightValues)):
            for hdri in range(len(self.DistanceValues)):
                GString = GString + self.PongGN[
                    len(self.HeightValues) * len(self.DistanceValues) + rowi * len(self.DistanceValues) + hdri]

        print(GString)
