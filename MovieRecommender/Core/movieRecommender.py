def movieRecommender():
    # Lista filmów obejrzanych przez użytkownika
    print('The list of the movies', args.name, 'watched')
    for i, movie in enumerate(df[df[args.name] > 0][args.name].index.tolist()):
        print("{:<3}| {:<40}".format(i + 1, movie))
    if args.amount > 0:
        # Przygotowanie listy polecanych filmów
        recommended_movies = []
        for m in df[df[args.name] == 0].index.tolist():
            index_df = df.index.tolist().index(m)
            predicted_rating = tmpDf.iloc[index_df, tmpDf.columns.tolist().index(args.name)]
            recommended_movies.append((m, predicted_rating))
        recommended_movies = sorted(recommended_movies, key=lambda x: x[1], reverse=True)

        # Listuje rekomendacje
        print('The list of the Recommended Movies')
        for i, movie in enumerate(recommended_movies[:args.amount]):
            print("{:<3}| {:<40} {:<4}".format(i + 1, movie[0], movie[1]))

    elif args.amount < 0:
        # Przygotowanie listy nie polecanych filmów
        recommended_movies = []
        for m in df[df[args.name] == 0].index.tolist():
            index_df = df.index.tolist().index(m)
            predicted_rating = tmpDf.iloc[index_df, tmpDf.columns.tolist().index(args.name)]
            recommended_movies.append((m, predicted_rating))
        recommended_movies = sorted(recommended_movies, key=lambda x: x[1], reverse=True)

        # Listuje filmy nie polecane
        print('The list of the NOT Recommended Movies')
        for i, movie in enumerate(recommended_movies[args.amount:]):
            print("{:<3}| {:<40} {:<4}".format(-5 + i, movie[0], movie[1]))