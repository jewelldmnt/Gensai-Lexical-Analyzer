from constants import *

def tab_counter(string):
    '''
    tab_counter counts all valid indentation(4 spaces) and returns the valid and invalid indentations.
    
    Parameters:
        -string (str): The line that may or may have indetations.

    Returns:
        -tab_tokens (list): A list of tuples, containing the indentation and if its valid or not.
        -emptry list
    '''
    tab_tokens = []
    # if the string starts with a tab (4 spaces) and has non whitespaces
    if string.startswith('    ') and not string.isspace():
        temp_tab = ''
        # iterate over the string per 4 places
        for char in range(0, len(string), 4):
            temp_tab = string[char:char+4]
            if temp_tab == '    ':
                temp_tab = ''
                tab_tokens.append(('indent', '\t'))
            # if the first character in the segment is a whitespace and any of the preceeding three are not, add invalid indent token
            elif temp_tab[0] == ' ' and any(c != ' ' for c in temp_tab[1:3]):
                whitespace = ''
                for char2 in temp_tab:
                    if char2.isspace():
                        whitespace += char2
                    else:
                        break
                tab_tokens.append(('invalid_indent', whitespace))
                break
            else:
                break
        return tab_tokens
    elif string.startswith(' '):
        whitespace = ''
        for x in string:
            if x.isspace():
                whitespace+=x
            else:
                break
        tab_tokens.append(('invalid_indent', whitespace))
        return tab_tokens
    else:
        return []

def categorizer(string, character, inside_quotes):
    # Its a comment
    is_partof_comment = not inside_quotes and character == '#'
    
    # Its a string literal
    is_start_string = character in ('\'','"')

    # If not an empty string
    if string:
        belongsto_operator = string[0] in '*/-+%><^!=&' and not inside_quotes
        
        # It belongs to an identifier
        belongsto_identifier = (string[0].isalpha() or string[0] == '_') and not inside_quotes
        
        # It belongs to a number
        belongsto_number = (string[0].isnumeric() or string[0] == '.') and not inside_quotes
    else:
        belongsto_operator, belongsto_identifier, belongsto_number = False, False, False
    
    # Its a logical operator
    is_operator = character in '*/-+%><^!=&'
    is_partof_operator = is_operator and belongsto_operator
    
    # Its a valid character in an identifier
    is_identifer = character.isalnum() or character == '_'
    is_partof_identifier = is_identifer and belongsto_identifier
    
    # Its a number or dot
    is_number = character.isnumeric() or character == '.'
    is_partof_number = is_number and belongsto_number
    
    return is_partof_comment, is_start_string, is_operator, is_partof_operator, is_identifer, is_partof_identifier, is_number, is_partof_number
        
def tokenizer(contents):
    """
    Tokenizes the input content into lexemes and classifies them into different token types.

    Parameters:
        contents (str): The input content to be tokenized.

    Returns:
        all_tokens (list): A list of lists, where each inner list contains tuples representing tokens.
    """
    all_tokens = []

    for line in contents.split('\n'):
        tokens = []
        previous_str = ""
        
        # Count the number of starting tabs (indentation) per line then store it in tokens
        tokens = tokens + tab_counter(line)
        line = line.strip()
        
        inside_quotes = False  # Flag to track whether the current character is inside quotes or not
        stringlen = len(line)  # Flag to track the length of the current line
        
        for index, char in enumerate(line):
            # If its part of the lexeme and not the end of a line
            if not char.isspace() and index < stringlen:
                # Categorize where the character should go
                (is_partof_comment, is_start_or_end_string, is_operator, is_partof_operator, is_identifer, is_partof_identifier, 
                is_number, is_partof_number) = categorizer(previous_str, char, inside_quotes)
                
                if is_start_or_end_string:
                    inside_quotes = not inside_quotes
                    previous_str += char
                    continue
                elif inside_quotes:
                    previous_str += char
                    continue
                if is_partof_comment:
                    tokens.append((classify_lexeme(line[index:]), line[index:]))
                    previous_str = ""
                    inside_quotes = False
                    break
                if is_identifer:
                    if is_partof_identifier:
                        previous_str += char
                        continue
                    elif previous_str:
                        tokens.append((classify_lexeme(previous_str), previous_str))
                        previous_str = ""
                        inside_quotes = False
                    else:
                        previous_str += char
                        continue
                if is_operator:
                    if is_partof_operator:
                        previous_str += char
                        operator_type = classify_lexeme(previous_str)
                        if operator_type == 'invalid':
                            tokens.append((classify_lexeme(previous_str[0]), previous_str[0]))
                            tokens.append((classify_lexeme(char), char))
                        else:
                            tokens.append((operator_type, previous_str))
                        previous_str = ""
                        inside_quotes = False
                        continue
                    elif (is_identifer or is_partof_comment or inside_quotes or is_number) and previous_str:
                        tokens.append((classify_lexeme(previous_str), previous_str))
                        previous_str = ""
                        inside_quotes = False
                        continue
                    else:
                        if not index == stringlen - 1:
                            previous_str += char
                            continue
                        else:
                            tokens.append((classify_lexeme(char), char))
                            previous_str = ""
                            inside_quotes = False
                            continue
                if is_number:
                    if is_partof_number:
                        previous_str += char
                        continue
                    else:
                        tokens.append((classify_lexeme(previous_str), previous_str))
                        previous_str = ""
                        inside_quotes = False

            else:
                if not previous_str or previous_str.isspace():
                    continue
                # classify lexeme
                tokens.append((classify_lexeme(previous_str), previous_str))

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