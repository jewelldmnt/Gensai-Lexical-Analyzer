# Import modules
from sys import argv
import pandas as pd
from lexical_analyzer import parse
from output import output

def main():
    '''
    'main' program validates a filename then parses the filename for tokenizing within the lexical analyzer. 
    Finally, outputs a csv, pdf file, or just simply prints the tokens

    Parameters:
        None

    Returns:
        pdf file or csv file: data containing the tokens, type of token, and what line it is found on.
    '''
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
    
    output(df)

if __name__ == '__main__':
    main()

