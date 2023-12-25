from sys import argv
import pandas as pd
from lexical_ver2 import parse

def main():
    file_path = argv[1]
    tokens = parse(file_path)
    data = []

    for line_num, line_code in enumerate(tokens, start=1):
        for token, lexeme in line_code:
            data.append([line_num, token, lexeme])

    # Create a DataFrame
    df = pd.DataFrame(data, columns=['Line', 'Token', 'Lexeme'])

    print(df.to_string(index=False))

if __name__ == '__main__':
    main()

