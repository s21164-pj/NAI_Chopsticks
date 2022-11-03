from easyAI.AI.DictTranspositionTable import DictTranspositionTable
from easyAI.AI.Hashes import JSWHashTranspositionTable
from easyAI.Player import Human_Player

from Chopsticks import Chopsticks

if __name__ == "__main__":
    from easyAI import Negamax, AI_Player, SSS, DUAL
    from easyAI.AI.TranspositionTable import TranspositionTable

    ai_algo_neg = Negamax(4)
    ai_algo_sss = SSS(4)
    dict_tt = DictTranspositionTable(32, JSWHashTranspositionTable())
    ai_algo_dual = DUAL(4, tt=TranspositionTable(dict_tt))

    print("Wskazówka - komenda 'show moves' pokaże wszystkie dostępne ruchy.")
    print("Zasady znajdzie w pliku readme.md")

    print("Wybierz tryb gry: ")
    print("1. AI vs AI")
    print("2. Gracz vs AI")
    gameMode = input()
    print(gameMode)

    if gameMode == "1":
        Chopsticks(
            [AI_Player(ai_algo_dual), AI_Player(ai_algo_dual)]
        ).play()
    elif gameMode == "2":
        order = input('Startujesz jako 1 czy 2: ')
        if order == "1":
            Chopsticks(
                [Human_Player(), AI_Player(ai_algo_dual)]
            ).play()
        elif order == "2":
            Chopsticks(
                [AI_Player(ai_algo_dual), Human_Player()]
            ).play()


    print("-" * 10)
