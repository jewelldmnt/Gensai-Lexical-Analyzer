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
    # if the string starts with a tab (4 spaces) and has non whitespaces
    if string.startswith('    ') and not string.isspace():
        tab_tokens = []
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
    else:
        return []

def compound_statement(lexeme):
    '''
    compound_statement determine whether a specific lexeme is a compound lexeme or just invalid.
    
    Parameters:
        -lexeme (str): a string that may or may not be a compound statements.

    Returns:
        -tab_tokens (list): A list of tuples, containing the indentation and if its valid or not.
        -emptry list
    '''
    tokens = []
    is_comp = False
    before_char = ''
    stringlen = len(lexeme)
    # iterate over each character
    for index, char in enumerate(lexeme):
        if char in SPECIAL_CHAR or (char == '.' and not before_char):
            tokens.append((classify_lexeme(before_char),before_char))
            before_char = char
            continue
        if char.isalpha() or char == '_':
            # check if string is still a valid string
            if before_char.isalnum() and before_char[0].isalpha():
                before_char += char
                if stringlen > index + 1:
                    continue
                else:
                    tokens.append((classify_lexeme(before_char),before_char))
                    continue
            # else if there is no character
            elif not before_char:
                before_char = char
                if stringlen > index + 1:
                    continue
                else:
                    tokens.append((classify_lexeme(before_char),before_char))
                    continue
            else:
                tokens.append((classify_lexeme(before_char),before_char))
                before_char = char
                continue
        if char.isnumeric():
            try:
                if before_char.isnumeric() or not before_char or before_char == '-' or before_char == '.':
                    before_char += char
                    if stringlen > index + 1:
                        continue
                    else:
                        tokens.append((classify_lexeme(before_char),before_char))
                        continue
                float_value = float(before_char)
                before_char += char
                if stringlen > index + 1:
                    continue
                else:
                    tokens.append((classify_lexeme(before_char),before_char))
                    continue
            except ValueError:
                if before_char.isalnum() and before_char[0].isalpha():
                    before_char += char
                    if stringlen > index + 1:
                        continue
                    else:
                        tokens.append((classify_lexeme(before_char),before_char))
                        continue
                else:
                    tokens.append((classify_lexeme(before_char),before_char))
                    before_char = char
                    continue
        if char in '*/-+%><^!=':
            if not before_char:
                if stringlen >= index + 1:
                    tokens.append((classify_lexeme(char),char))
                    continue
                else:
                    before_char = char
                    continue
            if before_char in '*/-+%><^!=' and char == '=':
                tokens.append((classify_lexeme(before_char),before_char))
                before_char = char
                continue
            if before_char.isalnum():
                tokens.append((classify_lexeme(before_char),before_char))
                before_char = char
                continue
            else:
                # if string length is still greater than current index, append the character before it
                if stringlen > index + 1:
                    tokens.append((classify_lexeme(before_char),before_char))
                    continue
                else:
                    # else if lastt state, append both the current and before character/s
                    tokens.append((classify_lexeme(before_char),before_char))
                    tokens.append((classify_lexeme(char),char))
                    continue

        if char == '.':
            try:
                int_value = int(before_char)
                before_char += char
                if stringlen > index + 1:
                    continue
                else:
                    tokens.append((classify_lexeme(before_char),before_char))
                    continue
            except ValueError:
                tokens.append((classify_lexeme(before_char),before_char))
                before_char = char
                if stringlen > index + 1:
                    continue
                else:
                    tokens.append((classify_lexeme(before_char),before_char))
                    continue

        tokens.append((classify_lexeme(before_char), before_char))
        before_char = char
            
    return is_comp, tokens

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
        operator_index = 1     # Flag regarding the number of place the operator character is
        inside_comment = False # Flag to track if its in a comment
        
        for index, char in enumerate(line):
            # If its part of the lexeme and not the end of a line
            if not inside_quotes and not char.isspace() and not index == stringlen - 1:
                # Its a comment
                is_partof_comment = not inside_quotes and char == '#'
                # Its a string literal
                is_partof_string = char in ('\'','"') or inside_quotes
                # Its an alphabet and the previous string consists of alphabet and numbers and the first character is alphabet (variable or data type)
                is_partof_identifier = not inside_quotes and not previous_str or ((char.isalnum() or char == '_') and (char[0].isalpha() or char[0] == '_'))
                # Its a number and the previous string is still a number or part of a number(float or int)
                is_partof_number = not inside_quotes and not previous_str or ((char.isnumeric() or char == '.') and (char[0].isnumeric() or char[0] == '.'))
                # Its a logical operator
                is_partof_operator = not inside_quotes and not previous_str or char in '*/-+%><^!=&'
                
                if is_partof_string:
                    if char in ('\'','"') and inside_quotes:
                        previous_str += char
                        inside_quotes = not inside_quotes
                        tokens.append((classify_lexeme(previous_str), previous_str))
                        break
                    else:
                        previous_str += char
                        continue
                if is_partof_comment:
                    tokens.append((classify_lexeme(line[index:]), line[index:]))
                    break
                if is_partof_identifier:
                    previous_str += char
                if is_partof_number:
                    previous_str += char
                if is_partof_operator:
                    if not previous_str:
                        previous_str = char
                    elif previous_str in '*/-+%><^!=' and char == '=':
                        previous_str += char
                        tokens.append((classify_lexeme(previous_str), previous_str))
                        previous_str = ""
                        continue
            else:
                # classify lexeme
                lexeme_type = classify_lexeme(line)
                # if invalid check if its compound
                if lexeme_type == 'invalid':
                    # if compound combine the tokens
                    compound_tokens = compound_statement(line)
                    tokens = tokens + compound_tokens
                else:
                    tokens.append((lexeme_type, line))
                    

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