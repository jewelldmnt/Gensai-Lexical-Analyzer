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
        temp_str = ""
        tokens = tokens + tab_counter(line)
        line = line.strip()
        
        for index, char in enumerate(line):
            next_char = line[index+1] if index+1 < len(line) else '' 
            
            ################################################################################
            # CHECKING OF COMMENTS
            ################################################################################
            if char == "#":
                if temp_str:
                    tokens.append((classify_lexeme(temp_str), temp_str))
                temp_str = line[index:] # Extracts the substring from the 'index' position to the end of the 'line'.
                tokens.append((classify_lexeme(temp_str), temp_str))
                temp_str = ""
                break
            
            
            #################git###############################################################
            # CHECKING OF STRINGS, OPERATORS, AND SPECIAL CHARACTERS
            ################################################################################
                     
            is_char_space_op_specialchar = char.isspace() or char in OPERATORS or char in SPECIAL_CHAR
            is_compound_op = temp_str+char in OPERATORS and temp_str
            is_not_partof_compound_op = not char+next_char in OPERATORS and char in OPERATORS
            is_partof_compound_op = char+next_char in OPERATORS and char in OPERATORS and not temp_str
            
            # Check for the beginning or end of quotes
            is_inside_quotes = False # Flag to track whether the current character is inside quotes or not
            if char in ('"', "'"):
                is_inside_quotes = not is_inside_quotes
                temp_str += char
                
            elif not is_inside_quotes and is_char_space_op_specialchar:
                if temp_str and temp_str not in OPERATORS:
                    temp_str = temp_str.strip()
                    tokens.append((classify_lexeme(temp_str), temp_str))
                    temp_str = ""

                is_negative_sign = char == '-' and (not tokens or tokens[-1][1] == ':')
                if is_negative_sign:
                    temp_str += char
                    continue

                elif is_compound_op:
                    temp_str += char
                    tokens.append((classify_lexeme(temp_str), temp_str))
                    temp_str = ""
                    continue    
                    
                elif is_not_partof_compound_op:
                    tokens.append((classify_lexeme(char), char))  
                    continue           
                                    
                elif is_partof_compound_op:
                    temp_str += char
                
                elif char in SPECIAL_CHAR:
                    tokens.append((classify_lexeme(char), char))
                    continue                    
            else:
                temp_str += char
                
                
            ################################################################################
            # CHECKING OF VALID NUMBERS
            ################################################################################
            if next_char == '.' and temp_str and not is_inside_quotes:
                # Check for cases like a1
                if is_valid_identifier(temp_str):
                    temp_str = temp_str.strip()
                    tokens.append((classify_lexeme(temp_str), temp_str))
                    temp_str = ""                    
            
            # Check if the next character is not part of a number
            next_char_is_not_partof_number = temp_str.replace('-', '').replace('.', '').isdigit() and not next_char.isdigit()
            if next_char_is_not_partof_number: 
                
                # Check if it is a complete decimal
                is_decimal_full = next_char == '.' and temp_str.count('.') == 1
                if is_decimal_full:
                    temp_str = temp_str.strip()
                    tokens.append((classify_lexeme(temp_str), temp_str))
                    temp_str = ""  
                
                # Check for cases like 1a
                elif not next_char.isdigit() and next_char != '.':
                    temp_str = temp_str.strip()
                    tokens.append((classify_lexeme(temp_str), temp_str))
                    temp_str = ""  
        
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