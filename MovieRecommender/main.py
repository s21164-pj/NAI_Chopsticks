"""
+ ==========================================+
| @Made by Daniel Chabowski, Szymon Dejewski|
L___________________________________________|

Program do rekomendacji filmów na podstawie ogólnej oceny użytkowników z pliku ratings.json.

Przygotowanie:
    1. Otwórz program, za pomocą IDE Intellij
    2. Pobierz wymagane biblioteki
    3. Uruchom według poniższej instrukcji

Instrukcja:
    Upewnij się, że Twoje środowisko jest przygotowane, czyli:
    1.  Posiadasz zainstalowane biblioteki
            a. numpy
            b. sklearn
            c. pandas
    2.  Zapoznaj się z podpunktem uruchomienie, w którym poznasz odpowiednie komendy do
        przetestowania programu

Uruchomienie:
    NAZWA:
        >>> python3 main.py

    SKŁADNIA:
        >>> python3 main.py [[--name <your_name>] [--file <json_file_with_rates>] [--amount -<number>]]

    PRZYKŁAD:
        >>> python3 main.py --name "Daniel Chabowski" --file "ratings.json" --amount -3
        >>> python3 main.py --name "Szymon Dejewski" --file "ratings.json"
"""

import numpy as np
import pandas as pd
import json
import argparse

from Core.calcSimilarityForAllValuesFromRatingsFile import calcSimilarityForAllValuesFromRatingsFile
from Core.movieRecommender import movieRecommender
from Utils.fileProceeder import proceed_with_file
from Utils.jsonParser import build_arg_parser
from sklearn.neighbors import NearestNeighbors


# Parser do obsługi argumentów wejściowych
args = build_arg_parser().parse_args()

# Otwieranie pliku i przygotowanie do przetwarzania
proceed_with_file()

# Obliczanie podobieństwa na podstawie ocen filmów
calcSimilarityForAllValuesFromRatingsFile()

# Listowanie filmów polecanych i nie polecanych
movieRecommender()
