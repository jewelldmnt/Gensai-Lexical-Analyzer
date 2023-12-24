from constants import *


def tokenizer(contents):
    """
    Tokenizes the input content into lexemes and classifies them into different token types.

    Parameters:
        contents (str): The input content to be tokenized.

    Returns:
        all_tokens (list): A list of lists, where each inner list contains tuples representing tokens.
    """
    all_tokens = []

    # Iterate through each line in the input content
    for line in contents.split('\n'):
        tokens = []
        temp_str = ""
        is_inside_quotes = False # Flag to track whether the current character is inside quotes or not
        
        # Iterate through each character in the line
        for index, char in enumerate(line):
            next_char = line[index+1] if index+1 < len(line) else '' 
            
            # Check for the beginning of a comment
            if char == "#":
                temp_str = line[index:]
                tokens.append((classify_lexeme(temp_str), temp_str))
                temp_str = ""
                break
            
            # Check for the beginning or end of quotes
            if char in ('"', "'"):
                is_inside_quotes = not is_inside_quotes
                temp_str += char
                
            # Check for whitespace, operators, or special characters
            elif not is_inside_quotes and (char.isspace() or char in OPERATORS or char in SPECIAL_CHAR):
                if temp_str:
                    temp_str = temp_str.strip()
                    tokens.append((classify_lexeme(temp_str), temp_str))
                    temp_str = ""

                if char in SPECIAL_CHAR or char in OPERATORS:
                    tokens.append((classify_lexeme(char), char))
                    
            else:
                temp_str += char
                
                
            # check for digits
            # ex instance: a1.
            if next_char == '.' and temp_str and not is_inside_quotes:
                # ex instance: a1
                if is_valid_identifier(temp_str):
                    temp_str = temp_str.strip()
                    tokens.append((classify_lexeme(temp_str), temp_str))
                    temp_str = ""                    
            
            # ex instance: 1.a 
            if temp_str.replace('-', '').replace('.', '').isdigit() and not next_char.isdigit(): 
                # ex instance: 1.9.
                if next_char == '.' and temp_str.count('.') == 1:
                    temp_str = temp_str.strip()
                    tokens.append((classify_lexeme(temp_str), temp_str))
                    temp_str = ""  
                
                # ex instance: 1a
                elif not next_char.isdigit() and next_char != '.':
                    temp_str = temp_str.strip()
                    tokens.append((classify_lexeme(temp_str), temp_str))
                    temp_str = ""  
                continue
        
        # Add any remaining non-empty string as a token
        if temp_str:
            temp_str = temp_str.strip()
            tokens.append((classify_lexeme(temp_str), temp_str))
        
        all_tokens.append(tokens)

    return all_tokens



def classify_lexeme(lexeme):
    """
    Classifies a lexeme into different token types.

    Parameters:
    - lexeme (str): The lexeme to be classified.

    Returns:
    - str: The token type.
    """
    if lexeme.startswith(('"', "'")) and lexeme.endswith(('"', "'")):
        return 'str_lit' if len(lexeme) - 2 > 1 else 'char_lit'
    elif lexeme.lower() in KEYWORDS:
        return KEYWORDS[lexeme.lower()]
    elif lexeme in OPERATORS:
        return OPERATORS[lexeme.lower()]
    elif lexeme in SPECIAL_CHAR:
        return SPECIAL_CHAR[lexeme]
    elif lexeme.lstrip('-').replace('.', '', 1).isdigit():
        return 'float_lit' if '.' in lexeme else 'int_lit'
    elif is_valid_identifier(lexeme):
        return 'identifier'
    elif lexeme.startswith("#"):
        return 'comment'
    else:
        return 'invalid'



def is_valid_identifier(identifier):
    """
    Checks if the given identifier follows the specified rules.

    Parameters:
    - identifier (str): The identifier to be checked.

    Returns:
    - bool: True if the identifier is valid, False otherwise.
    """
    if not identifier or not identifier[0].isalpha() and identifier[0] != '_':
        return False

    for char in identifier[1:]:
        if char not in VALID_CHARS:
            return False

    if identifier in KEYWORDS:
        return False

    if len(identifier) > 79:
        return False

    return True



def parse(file):
    """
    Parses the contents of a file using a lexer.

    Parameters:
        file (str): The path to the file to be parsed.

    Returns:
        tokens (list): A list of tokens representing the parsed content.
    """
    contents = open(file, 'r').read()
    tokens = tokenizer(contents)
    return tokens