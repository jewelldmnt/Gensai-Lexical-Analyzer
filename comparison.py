import os
from sys import argv
import pandas as pd
import new_LA as new_LA
import lexical_analyzer as last_la


def main():
    # Specify the folder name
    folder_name = "tester"

    # Ask the user for the file name within the tester folder
    file_name = input(f"Enter the file name within the '{folder_name}' folder: ")

    # Construct the file path
    file_path = os.path.join(folder_name, file_name)

    # Check if the file exists
    if not os.path.exists(file_path):
        print(f"The file '{file_path}' does not exist.")
        return

    new_lexer = new_LA.parse(file_path)
    last_lexer = last_la.parse(file_path)
    data = []

    if new_lexer == last_lexer:
        print("2 lexers are the same")

    else:
        # Print the line number where they differ
        for line_number, (current_token, last_token) in enumerate(zip(new_lexer, last_lexer), start=1):
            if current_token != last_token:
                print(f"Tokens differ at line {line_number}:")
                print(f"Current Lexer Token: {current_token}")
                print(f"Last Lexer Token: {last_token}")
                print("\n")

        # If one lexer has more tokens than the other
        if len(new_lexer) != len(last_lexer):
            min_len = min(len(new_lexer), len(last_lexer))
            print(f"Lexer token lists have different lengths. Remaining tokens start at line {min_len + 1}:")

            for line_number, remaining_token in enumerate(new_lexer[min_len:], start=min_len + 1):
                print(f"Current Lexer Token at line {line_number}: {remaining_token}")

            for line_number, remaining_token in enumerate(last_lexer[min_len:], start=min_len + 1):
                print(f"Last Lexer Token at line {line_number}: {remaining_token}")


if __name__ == '__main__':
    main()