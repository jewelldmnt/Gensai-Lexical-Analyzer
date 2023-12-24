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
        temp_str = ""
        inside_quotes = False # Flag to track whether the current character is inside quotes or not
        
        # count the number of starting tabs (indentation) per line then store it in tokens
        tokens = tokens + tab_counter(line)
        line = line.strip()
        stringlen = len(line)
        operator_index = 1
        
        for index, char in enumerate(line):
            # Check for the beginning of a comment
            if char == "#":
                temp_str = line[index:]
                tokens.append((classify_lexeme(temp_str), temp_str))
                temp_str = ""
                break
            
            # Check if a special character then append instantly the previous lexeme and the current special character
            if char in SPECIAL_CHAR and char not in '"\'':
                if temp_str != '':
                    tokens.append((classify_lexeme(temp_str), temp_str))
                tokens.append((classify_lexeme(char), char))
                temp_str = ""
                continue
            
            # Check if an operator or part of a logical operator and is the first character of a compound logical operator
            if (char in OPERATORS or char in '&|%') and operator_index == 1:
                if char == '&':
                    tokens.append((classify_lexeme(char), char))
                    continue
                operator_index +=1
                temp_str += char
                if stringlen > index + 1:
                    continue
                else:
                    tokens.append((classify_lexeme(char), char))
                    operator_index = 1
                    temp_str = ""
                    continue
            # Check if the lexeme is a assignment or comparison operator
            elif temp_str in '*/-+%><^!=' and operator_index == 2 and char == '=':
                temp_str += char
                tokens.append((classify_lexeme(temp_str), temp_str))
                operator_index = 1
                temp_str = ""
                continue
            # Check if its a valid or_op or occasionally a compoound statement
            elif (char in OPERATORS or char in '|') and operator_index == 2:
                has_both = any(c.isalpha() for c in temp_str) and any(c.isdigit() for c in temp_str)
                if has_both:
                    is_comp, comp = compound_statement(temp_str)
                    if not is_comp:
                        tokens += comp
                        tokens.append((classify_lexeme(char), char))
                        has_both = False
                        operator_index = 1
                        temp_str = ""
                        continue
                if temp_str == char and temp_str == '|':
                    tokens.append((classify_lexeme(temp_str + char), temp_str+char))
                    operator_index = 1
                    temp_str = ""
                    continue
                tokens.append((classify_lexeme(temp_str), temp_str))
                tokens.append((classify_lexeme(char), char))
                temp_str = ""
                operator_index = 1
                continue
            
            # Check for the beginning or end of quotes
            if char in ('"', "'"):
                inside_quotes = not inside_quotes
                temp_str += char
                
            # Check if lexeme is not inside a quote and char is whitespace or its the end of a lexeme
            elif not inside_quotes and (char.isspace() or stringlen == index+1):
                operator_index = 1
                if stringlen == index+1:
                    temp_str += char
                lexem_type = classify_lexeme(temp_str)
                if temp_str:
                    # Check if an invalid lexem is a compound statement else append token
                    if lexem_type == 'invalid':
                        is_comp, comp = compound_statement(temp_str)
                        if not is_comp:
                            # Combine all the tokens
                            tokens += comp
                        else:
                            tokens.append((lexem_type, temp_str))
                    else:
                        tokens.append((lexem_type, temp_str))
                    temp_str = ''
            else:
                temp_str += char

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