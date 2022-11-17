def calcSimilarityForAllValuesFromRatingsFile():
    global tmpDf, m
    # Oblicz podobieństwo dla wszystkich wartości
    knn = NearestNeighbors(metric='cosine', algorithm='brute')
    knn.fit(df.values)
    distances, indices = knn.kneighbors(
        df.values, n_neighbors=args.neighbours)
    USER_INDEX = df.columns.tolist().index(args.name)  # Index args.name w dataframe
    tmpDf = df.copy()  # Tymczasowe dla obliczeń
    # m - liczba wierszy filmów w df
    # t - movie_title
    for m, t in enumerate(df.index):
        # Jeśli film nie ma oceny podanej przez użytkownika
        if df.iloc[m, USER_INDEX] == 0:
            sim_movies = indices[m].tolist()  # podobne filmy
            movie_distances = distances[m].tolist()  # 'Odległość' filmów

            # Jeśli znaleziono podobne filmy
            if m in sim_movies:
                id_movie = sim_movies.index(m)
                sim_movies.remove(m)
                movie_distances.pop(id_movie)
            # Jeśli nie ma innych ocen tego filmu
            else:
                sim_movies = sim_movies[:args.neighbours - 1]
                movie_distances = movie_distances[:args.neighbours - 1]

            # Obliczanie podobieństwa
            movie_similarity = [1 - x for x in movie_distances]
            movie_similarity_copy = movie_similarity.copy()
            nominator = 0

            # Dla każdego znalezionego podobnego filmu
            for s in range(0, len(movie_similarity)):
                # Jeśli nie ma oceny
                if df.iloc[sim_movies[s], USER_INDEX] == 0:
                    # Ignoruje ocenę
                    if len(movie_similarity_copy) == (args.neighbours - 1):
                        movie_similarity_copy.pop(s)
                    # Oblicz przewidywaną ocenę
                    else:
                        movie_similarity_copy.pop(
                            s - (len(movie_similarity) - len(movie_similarity_copy)))
                # Ocena i prawdopodobieństwo używane w obliczeniach
                else:
                    nominator = nominator + movie_similarity[s] * df.iloc[sim_movies[s], USER_INDEX]

            # Sprawdzanie czy istnieją oceny
            if len(movie_similarity_copy) > 0:
                # Sprawdzanie czy oceny są miarodajne
                if sum(movie_similarity_copy) > 0:
                    tmpDf.iloc[m, USER_INDEX] = nominator / sum(movie_similarity_copy)
                else:
                    tmpDf.iloc[m, USER_INDEX] = 0
            else:
                tmpDf.iloc[m, USER_INDEX] = 0
