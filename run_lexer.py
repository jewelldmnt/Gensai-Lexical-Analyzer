import prettytable
from Lexical_Analyzer.lexical_analyzer import parse
from Lexical_Analyzer.output import output
from Lexical_Analyzer.constants import SPECIAL_CHAR, OPERATORS

def main():
    '''
    'main' program validates a filename then parses the filename for tokenizing within the lexical analyzer. 
    Finally, outputs a csv, pdf file, or just simply prints the tokens

    Parameters:
        None

    Returns:
        pdf file or csv file: data containing the tokens, type of token, and what line it is found on.
    '''
    file_name = input("Enter the file name (without the path, e.g., 'example.gsai'): ")
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

    if not file_path.endswith(".gsai"):
        print("Error: Invalid file extension. Only '.gsai' files are allowed.")
        return

    table = prettytable.PrettyTable(["Line Number", "Lexeme", "Token"])
    table.align["Lexeme"] = "l"
    table.align["Token"] = "l"

    for line_num, token_list in tokens.items():
        for lexeme, token in token_list:
            table.add_row([line_num, lexeme, token])

    print("Tokens in Tabular Form:")
    print(table)

if __name__ == '__main__':
    main()

