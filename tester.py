from Syntax_Analyzer.production_rule import *
import re

actual_syntax = ['elif_kw', 'l_paren', '[CONDITION]', 'r_paren', 'colon_delim']

lex_analyzer = {1: [('if', 'if_kw'), ('(', 'l_paren'), ('a', 'identifier'), ('==', 'eq_op'), ('b', 'identifier'), (')', 'r_paren'), (':', 'colon_delim')], 2: [('out', 'out_kw'), (':', 'colon_delim'), ('a', 'identifier')], 3: [('elif', 'elif_kw'), ('(', 'l_paren'), ('a', 'identifier'), ('==', 'eq_op'), ('b', 'identifier'), ('and', 'and_kw'), ('b', 'identifier'), ('==', 'eq_op'), ('a', 'identifier'), (')', 'r_paren'), (':', 'colon_delim')], 4: [('a', 'identifier'), ('=', 'ass'), ('in', 'in_kw'), ('(', 'l_paren'), (')', 'r_paren')]}
if actual_syntax[0] == 'elif_kw' and any('if_kw' in [t[1] for t in lex_analyzer[line]] for line in range(1, len(lex_analyzer) + 1)):    
    print(True)

def extract_parameters(actual_syntax):
    """
    Extract parameters from the given actual_syntax.

    Parameters:
    - actual_syntax (list): The list of tokens representing the actual syntax.

    Returns:
    parameters (list) or None: The list of tokens representing the extracted parameters or None if no match is found.
    """
    actual_syntax = ' '.join(actual_syntax)
    
    # Define the pattern to match the desired syntax
    pattern = r"l_paren (.+? r_paren)"

    # Use regular expression to find matches
    matches = re.findall(pattern, actual_syntax)

    # Extract the parameters if matches are found
    if matches:
        # Get the last match (most inner content between l_paren and r_paren)
        inner_content = matches[-1]
        parameters = inner_content.split()
        return parameters
    else:
        return None



def converter(actual_syntax):
    """
    Converts the specific data types into 'dt' for bnf purposes in production rules.
    While checking first

    Parameters:
        syntax (list): List of actual syntax where certain tokens will be converted.

    Returns:
        matching_rule (list): ist of converted syntax.

    """
    converted_syntax = ['dt' if token in DATA_TYPES else token for token in actual_syntax]
    converted_syntax = ['lit' if token.endswith("_lit") else token for token in converted_syntax]
    converted_syntax = ['op' if token.endswith("_op") and token not in ("and_op", "or_op") else token for token in converted_syntax]

    return converted_syntax


rule_name = "If Statement"
rule_syntax = ["if_kw", "l_paren", "[CONDITION]", "r_paren"]
actual_syntax = ["if_kw", "l_paren", "l_paren", "identifier", "eq_op", "int_lit", "and_kw", "identifier", "eq_op", "int_lit", "r_paren", "r_paren", "colon_delim"]

print(extract_parameters(actual_syntax))


if rule_name == 'If Statement':
    rule_syntax = rule_syntax[:2] # <if_kw> <l_paren>
    actual_syntax = converter(actual_syntax)
    
    condtl_stmt =  extract_parameters(actual_syntax)
    # print(f"Condtl_stmt: {condtl_stmt}")
    condtl_list = []
    current_cond = []
    
    for idx, token in enumerate(condtl_stmt):
        if token not in ("and_kw", "or_kw"):
            current_cond.append(token)
        else:
            if current_cond:
                condtl_list.append(current_cond)
                condtl_list.append(token)
            current_cond = []
    
    if current_cond:
        condtl_list.append(current_cond)
    current_cond = []
    # print(f"condtl_list: {condtl_list}")

    
    for idx, cond in enumerate(condtl_list):
        if cond not in ("and_kw", "or_kw"):
            condition = ''.join(f"<{token}>" for token in cond)
        else:
            condition = f"<{cond}>"
        # print(f"\ncondition: {condition}")
        if condition in LOGICAL_STMT or condition in RELATIONAL_STMT:
            rule_syntax.extend(condition[1:-1].split('><'))
            # print(f"\rule_syntax iteration {idx}: {rule_syntax}")
        elif condition in ("<and_kw>", "<or_kw>"):
            rule_syntax.append(condition[1:-1])
            # print(f"\rule_syntax iteration {idx}: {rule_syntax}")
        else:
            break
    rule_syntax.extend(['r_paren', 'colon_delim'])    

# print(f"rule_syntax: {rule_syntax}")
    

