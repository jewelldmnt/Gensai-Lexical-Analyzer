DIGITS = "0123456789"
KEYWORDS = [
    "and", "as", "assert", "async", "await", "break", "class", "continue",
    "def", "del", "elif", "else", "except", "finally", "for", "from", "global",
    "False", "True", "if", "import", "within", "is", "lambda",
    "None", "not", "or", "pass", "raise", "repeat", "return", "try", "while",
    "int", "float", "double", "char", "str", "bool", "out", "in"
]
ALPHABETS = "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz"



def tokenizer(contents):
    """
    Tokenizes the input content into lexemes and classifies them into different token types.

    Parameters:
        contents (str): The input content to be tokenized.

    Returns:
        all_tokens (list): A list of lists, where each inner list contains tuples representing tokens.
    """
    lines = contents.split('\n')
    all_tokens = []

    for line in lines:
        tokens = []
        temp_str = ""
        quote_count = 0

        for char in line:
            # if the current character is a start or end of a string literal add 1
            if char in ('"', "'"):
                quote_count += 1
            in_quotes = quote_count % 2 == 1 # variable whether a character is part of a string literal
            
            # if the current character an end of a lexem append it to the tokens
            if char in (' ', ':') and not in_quotes:
                if temp_str:
                    tokens.append((classify_lexeme(temp_str), temp_str))
                    temp_str = ""
                if char == ':':
                    tokens.append(('delimiter', ':'))
            else:
                temp_str += char

        if temp_str:
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
        return 'string' if len(lexeme) - 2 > 1 else 'character'
    elif lexeme in KEYWORDS:
        return 'keyword'
    elif lexeme in "+-*/":
        return 'operator'
    elif lexeme.lstrip('-').replace('.', '', 1).isdigit():
        return 'float' if '.' in lexeme else 'integer'
    elif is_valid_identifier(lexeme):
        return 'identifier'
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

    valid_chars = ALPHABETS + DIGITS + "_"
    for char in identifier[1:]:
        if char not in valid_chars:
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