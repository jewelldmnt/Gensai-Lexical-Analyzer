from constants import *

def tab_counter(string):
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
        
        # count the number of starting tabs (indentation) per line then store it in tokens
        tokens = tokens + tab_counter(line)
        line = line.strip()
        
        for char in line:
            # if the current character is a start or end of a string literal add 1
            if char in ('"', "'"):
                quote_count += 1
            in_quotes = quote_count % 2 == 1 # variable whether a character is part of a string literal
            
            # if the current character an end of a lexem append it to the tokens
            if char in (' ', ':') and not in_quotes:
                if temp_str:
                    lexem_type = classify_lexeme(temp_str)
                    # check if an invalid lexem is actually a compound statement else append token
                    if lexem_type == 'invalid':
                        is_comp, comp = compound_statement(temp_str)
                        if not is_comp:
                            # combine all the tokens
                            tokens += comp
                        else:
                            tokens.append((lexem_type, temp_str))
                    else:
                        tokens.append((lexem_type, temp_str))
                    temp_str = ""
                if char == ':':
                    tokens.append(('delimiter', ':'))
            else:
                temp_str += char

        if temp_str:
            tokens.append((classify_lexeme(temp_str), temp_str))

        all_tokens.append(tokens)
        
        # update current indentation

    return all_tokens

def compound_statement(lexeme):
    '''
    
    '''
    tokens = []
    is_comp = False
    before_char = ''
    stringlen = len(lexeme)
    # iterate over each character
    for index, char in enumerate(lexeme): # xsde=1.56=/==*-+7.56yt # 12sde.25
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
                before_char = char
                continue
            if before_char in '*/-+%><^!=':
                tokens.append((classify_lexeme(before_char),before_char))
                before_char = char
                continue
            else:
                tokens.append((classify_lexeme(before_char),before_char))
                before_char = char
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
    elif lexeme == '.':
        return 'dot'
    elif lexeme.lower() in KEYWORDS:
        return KEYWORDS[lexeme.lower()]
    elif lexeme in ASS_OP:
        return ASS_OP[lexeme.lower()]
    elif lexeme in ARITHMETIC_OP:
        return ARITHMETIC_OP[lexeme.lower()]
    elif lexeme in LOGICAL_OP:
        return LOGICAL_OP[lexeme.lower()]
    elif lexeme in COMPARISON_OP:
        return COMPARISON_OP[lexeme.lower()]
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