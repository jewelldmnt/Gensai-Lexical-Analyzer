from sys import argv
import pandas as pd
from lexical_analyzer import parse

def main():
    file_path = argv[1]
    tokens = parse(file_path)
    data = []

    if not file_path.endswith(".gs"):
        print("Error: Invalid file extension. Only '.gs' files are allowed.")
        return


    for line_num, line_code in enumerate(tokens, start=1):
        for token, lexeme in line_code:
            data.append([line_num, token, lexeme])

    # Create a DataFrame
    df = pd.DataFrame(data, columns=['Line', 'Token', 'Lexeme'])

    print(df.to_string(index=False))

if __name__ == '__main__':
    main()

