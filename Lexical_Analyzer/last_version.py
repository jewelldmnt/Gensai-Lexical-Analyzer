from constants import *
################################################################################
# This the version of what we presented in f2f lexical analyzer presentation 
# where: 
# 1.2.3 is not invalid 
# +++ is not invalid
################################################################################


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
        line = line.strip()
        temp_str = ""
        is_char_partof_str = False # Flag to track whether the current character is inside quotes or not
        start_quote = ""
        idx_end_quote = ""
        idx_right_brace = ""
        is_char_partof_braces = False

        for index, char in enumerate(line):
            next_char = line[index+1] if index+1 < len(line) else '' 
            
            ################################################################################
            # CHECKING OF COMMENTS
            ################################################################################
            if char == "#" and not is_char_partof_str:
                if temp_str:
                    tokens.append((classify_lexeme(temp_str), temp_str))
                temp_str = line[index:] # Extracts the substring from the 'index' position to the end of the 'line'.
                tokens.append((classify_lexeme(temp_str), temp_str))
                temp_str = ""
                break
                
            #################git###############################################################
            # CHECKING OF STRINGS, OPERATORS, AND SPECIAL CHARACTERS
            ################################################################################
            if (char.isspace()):
                if not is_char_partof_str and temp_str:
                    tokens.append((classify_lexeme(temp_str), temp_str))
                    temp_str = ""
                elif is_char_partof_str:
                    temp_str += char
                continue

            # Check if it's a space, operator, or special character.
            is_char_op_specialchar = char in OPERATORS or char in SPECIAL_CHAR
            
            # Check if the combination of the current character and the previous characters forms a compound operator.
            is_compound_op = temp_str+char in OPERATORS and temp_str
            
            # Check if the current character, combined with the next character, forms a compound operator.
            is_char_partof_compound_op = char+next_char in OPERATORS and char in OPERATORS and not temp_str
            
            # Check if the current character is not part of a compound operator but is a standalone operator.
            is_char_single_op = not char+next_char in OPERATORS and char in OPERATORS
            
            # Check if there are succeeding quotes of the same kind as the current character (char) in the remaining part of the line
            has_succeeding_quotes = any(c in ('"', "'") and c == char for c in line[index+1:])
            
            # Check for the start of the string
            if char in ('"', "'") and has_succeeding_quotes and not start_quote:
                start_quote = char
                substring = line[index+1:]
                
                idx_end_quote = line[index+1:].find(start_quote) 
                idx_end_quote = idx_end_quote + index + 1
                
                is_char_partof_str = True
                if temp_str:
                    temp_str = temp_str.strip()
                    tokens.append((classify_lexeme(temp_str), temp_str))
                    temp_str = ""
                    
                tokens.append((classify_lexeme(char), char))
                continue
            
            # Check for the end of the string
            elif index == idx_end_quote and is_char_partof_str:
                is_char_partof_str = False
                if temp_str:
                    temp_str = temp_str.strip()
                    tokens.append((classify_lexeme(temp_str, is_partof_str=True), temp_str))

                tokens.append((classify_lexeme(char), char))
                temp_str = ""
                start_quote = ""
                idx_end_quote = ""
                continue
            
            # Check for identifier inside braces
            elif is_char_partof_str and char in '{}':
                if char == '{' and '}' in line:
                    idx_right_brace = line.find('}')
                    idx_left_braces = line.find('{')
                    
                    if idx_right_brace > idx_left_braces and idx_right_brace < idx_end_quote:
                        is_char_partof_braces = True
                        if temp_str:
                            tokens.append((classify_lexeme(temp_str, is_partof_str=True), temp_str))
                            temp_str = ""
                        tokens.append((classify_lexeme(char), char))
                    else:
                        if temp_str:
                            tokens.append((classify_lexeme(temp_str), temp_str))
                        tokens.append((classify_lexeme(char), char))
                        temp_str = ""
                        idx_right_brace = ""
                        idx_left_brace = ""
                        
                elif index == idx_right_brace:
                        is_char_partof_braces = False
                        idx_right_brace = ""
                        if temp_str:
                            tokens.append((classify_lexeme(temp_str), temp_str))
                        tokens.append((classify_lexeme(char), char))
                        temp_str = ""
                        
                else:
                    if temp_str:
                        tokens.append((classify_lexeme(temp_str, is_partof_str=True), temp_str))
                        temp_str = ""
                    tokens.append((classify_lexeme(char), char))                      
                    
            # Check for identifier inside braces
            elif is_char_partof_str and not is_char_op_specialchar and not is_char_partof_braces:
                temp_str += char  
                continue
                  
            # Checking of operators and special char
            elif is_char_op_specialchar:
                # Check if the character 'char' is a period and if it is not part of a valid number
                is_char_partof_number = (temp_str.replace('.', '').isdigit() and char == '.') and (not is_char_partof_str or is_char_partof_braces)
                if temp_str and temp_str not in OPERATORS and not is_char_partof_number:
                    if is_char_partof_str and not is_char_partof_braces:
                        tokens.append((classify_lexeme(temp_str, is_partof_str=True), temp_str))
                    else:
                        temp_str = temp_str.strip()
                        tokens.append((classify_lexeme(temp_str), temp_str))
                    temp_str = ""

                if is_compound_op:
                    temp_str += char
                    tokens.append((classify_lexeme(temp_str), temp_str))
                    temp_str = ""
                    continue    
                    
                elif is_char_single_op:
                    tokens.append((classify_lexeme(char), char))  
                    continue           
                                    
                elif is_char_partof_compound_op:
                    temp_str += char
                
                elif char in SPECIAL_CHAR:
                    # Check if the character 'char' is a period and if it is part of a valid number
                    is_period_partof_number = (temp_str.replace('.', '').isdigit() or next_char.isdigit() and char == '.') and (not is_char_partof_str or is_char_partof_braces)
                    if  is_period_partof_number:
                        temp_str += char
                    else:
                        tokens.append((classify_lexeme(char), char))
                        continue                    
            else:
                temp_str += char
                
                
            ################################################################################
            # CHECKING OF VALID NUMBERS
            ################################################################################
            if next_char == '.' and temp_str and not is_char_partof_str:
                # Check for cases like a1
                if is_valid_identifier(temp_str):
                    temp_str = temp_str.strip()
                    tokens.append((classify_lexeme(temp_str), temp_str))
                    temp_str = ""                    
            
            # Check if the next character is not part of a number
            next_char_is_not_partof_number = temp_str.replace('.', '').isdigit() and not next_char.isdigit()
            if next_char_is_not_partof_number: 
                
                # Check if it is a complete decimal
                is_decimal_full = next_char == '.' and temp_str.count('.') == 1
                if is_decimal_full:
                    temp_str = temp_str.strip()
                    tokens.append((classify_lexeme(temp_str), temp_str))
                    temp_str = ""  
                
                # Check if the current temp_str is not followed by a digit or a period
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


def classify_lexeme(lexeme, is_partof_str=None):
    """
    Classifies a lexeme into different token types.

    Parameters:
    - lexeme (str): The lexeme to be classified.

    Returns:
    - str: The token type.
    """
    if is_partof_str and lexeme: 
        return 'str_lit' if len(lexeme) > 1 else 'char_lit'
    elif lexeme.lower() in KEYWORDS:
        return KEYWORDS[lexeme.lower()]
    elif lexeme.lower() in BUILTIN_FUNC:
        return BUILTIN_FUNC[lexeme.lower()]
    elif lexeme.lower() in BUILTIN_MET:
        return BUILTIN_MET[lexeme.lower()]
    elif lexeme in OPERATORS:
        return OPERATORS[lexeme.lower()]
    elif lexeme in SPECIAL_CHAR:
        return SPECIAL_CHAR[lexeme]
    elif lexeme.replace('.', '') and lexeme.count('.') == 1:
        return 'float_lit'
    elif lexeme.isdigit() and not lexeme.startswith('0') or lexeme == '0':
        return 'int_lit'
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