from sys import *
from lexical_analyzer import *

if __name__ == '__main__':
    file_path = argv[1]
    tokens = parse(file_path)

    for line_tokens in tokens:
        for token_type, token_value in line_tokens:
            print(f"{token_type}: {token_value}")
        print()  
