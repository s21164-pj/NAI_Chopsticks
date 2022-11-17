def proceed_with_file():
    global df
    with open(args.file, 'r') as f:
        data = json.loads(f.read())
    df = pd.DataFrame.from_dict(data)
    df = df.fillna(0)