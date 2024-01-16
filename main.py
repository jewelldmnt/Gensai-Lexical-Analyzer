import pandas as pd
from lexical_analyzer import parse
from output import output
from constants import SPECIAL_CHAR, OPERATORS

def main():
    '''
    'main' program validates a filename then parses the filename for tokenizing within the lexical analyzer. 
    Finally, outputs a csv, pdf file, or just simply prints the tokens

    Parameters:
        None

    Returns:
        pdf file or csv file: data containing the tokens, type of token, and what line it is found on.
    '''
    file_name = input("Enter the file name (without the path, e.g., 'example.gs'): ")
    file_path = f'tester/{file_name}'  # Assuming the files are always inside the 'tester' folder

    try:
        tokens = parse(file_path)
    except:
        print(f"Error: File '{file_path}' not found.")
        return
    
    data = []
    
    number_dot = 0
    for char in file_name:
        if (char in SPECIAL_CHAR or char in OPERATORS) and char !='.':
            print("Error: Invalid file extension. Don't include special character.")
            return
        if char == '.':
            number_dot += 1
        if number_dot >= 2:
            print("Error: Invalid file extension. You must have only one file extension.")
            return

    if not file_path.endswith(".gs"):
        print("Error: Invalid file extension. Only '.gs' files are allowed.")
        return

    for line_num, line_code in enumerate(tokens, start=1):
        for token, lexeme in line_code:
            data.append([line_num, lexeme, token])

    # Create a DataFrame
    df = pd.DataFrame(data, columns=['Line', 'Lexeme', 'Token'])
    
    output(df)

if __name__ == '__main__':
    main()

