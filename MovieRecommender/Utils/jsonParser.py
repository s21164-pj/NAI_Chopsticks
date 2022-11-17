def build_arg_parser():
    parser = argparse.ArgumentParser(description='Compute similarity score')
    parser.add_argument('--name', dest='name', required=True,
        help='Name of the student/teacher')
    parser.add_argument("--file", dest="file", required=True,
        help='Name of file with data')
    parser.add_argument("--amount", dest="amount", default=5, type=int,
        help='Amount of recommendations you want.')
    parser.add_argument("--neighbours", dest="neighbours", default=3,
        help='Amount of neighbours for the algorythmm.')
    return parser