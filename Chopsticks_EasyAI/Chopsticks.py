from easyAI import TwoPlayerGame
1
class Chopsticks(TwoPlayerGame):
    """
    Prosta gra "Chopsticks" w którą możesz zagrać na palcach
    zasady dostępne w pliku redme.md

    """

    def __init__(self, players, numhands=2):
        self.players = players
        self.numplayers = len(self.players)
        self.numhands = numhands
        self.current_player = 1

        hand = [1 for hand in range(self.numhands)]
        self.hands = [hand[:] for player in range(self.numplayers)]

    def possible_moves(self):
        """
            Ruchy możliwe do wykonania

        """
        moves = []
        # rozdzielanie
        for h1 in range(self.numhands):
            for h2 in range(self.numhands):
                if h1 == h2:
                    continue
                hand1 = self.hands[self.current_player - 1][h1]
                hand2 = self.hands[self.current_player - 1][h2]
                for i in range(1, 1 + min(hand1, 5 - hand2)):
                    move = ("rozdziel", h1, h2, i)
                    if hand1 != hand2 + i and self.back_to_startstate(move) == False:
                        moves.append(move)

        # atak
        for i in range(self.numhands):
            for j in range(self.numhands):
                hand_player = self.hands[self.current_player - 1][i]
                hand_opp = self.hands[self.opponent_index - 1][j]
                if hand_player != 0 and hand_opp != 0:
                    moves.append(("atak", i, j, self.hands[self.current_player - 1][i]))
        return moves

    def make_move(self, move):
        """
            Wykonywanie ruch
        """
        type, one, two, value = move
        if type == "rozdziel":
            self.hands[self.current_player - 1][one] -= value
            self.hands[self.current_player - 1][two] += value
        else:
            self.hands[self.opponent_index - 1][two] += value

        for player in range(self.numplayers):
            for hand in range(self.numhands):
                if self.hands[player][hand] >= 5:
                    self.hands[player][hand] = 0

    def lose(self):
        return max(self.hands[self.current_player - 1]) == 0

    def win(self):
        return max(self.hands[self.opponent_index - 1]) == 0

    def is_over(self):
        return self.lose() or self.win()

    def show(self):
        for i in range(self.numplayers):
            print("Player %d: " % (i + 1)),
            for j in range(self.numhands):
                if self.hands[i][j] > 0:
                    print("|" * self.hands[i][j] + "\t"),
                else:
                    print("x\t"),
            print("")

    def scoring(self):
        """
        Zlicza grające ręce
        """
        if self.lose():
            return -100
        if self.win():
            return 100
        alive = [0] * 2
        for player in range(self.numplayers):
            for hand in range(len(self.hands[player])):
                alive[player] += self.hands[player][hand] > 0
        return alive[self.current_player - 1] - alive[self.opponent_index - 1]

    def ttentry(self):
        entry = [
            self.hands[i][j]
            for i in range(self.numplayers)
            for j in range(self.numhands)
        ]
        entry = entry + [self.current_player]
        return tuple(entry)

    def back_to_startstate(self, move):
        """
        Sprawdzenie czy ruch spowoduje powrót do stanu początkowego
        """
        nextstate = self.copy()
        nextstate.make_move(move)
        hands_min = min([min(nextstate.hands[i]) for i in range(self.numplayers)])
        hands_max = max([max(nextstate.hands[i]) for i in range(self.numplayers)])
        return hands_min == 1 and hands_max == 1
