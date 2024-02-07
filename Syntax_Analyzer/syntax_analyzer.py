from Lexical_Analyzer.lexical_analyzer import tokenizer
from Syntax_Analyzer.production_rule import *
from copy import copy
from itertools import zip_longest, groupby
from Syntax_Analyzer.error_rule import UNEXPECTED_ERRORS, EXPECTED_ERRORS
import re



class Syntax_Analyzer():
    def __init__(self, file):
        self.file_path = file
        self.contents = open(file, 'r').read()
        self.lex_analysis = None
        self.syntax_errors = None
        self.all_syntax_error = {}
        self.already_checked = False
        self.in_loop = False
        self.is_if_present = False
        self.currect_line_num = ""
    
    
    def parse(self):
        """
        Parses the contents of a file using a lexer.

        Parameters:
            file (str): The path to the file to be parsed.

        Returns:
            tokens (list): A list of tokens representing the parsed content.
        """
        self.lex_analysis = tokenizer(self.contents)
        self.syntax_errors = self.syntax_analyzer(self.lex_analysis)
        return copy(self.syntax_errors)
    
    
    def syntax_analyzer(self, lex_analysis):
        """
        Performs syntax analysis on the given lexeme analysis results.

        Parameters:
            lex_analysis (dict): A dictionary containing line numbers mapped to their respective token lists.

        Returns:
            all_syntax_errors (dict): A dictionary containing syntax errors mapped to their respective line numbers.
        """
        # print(self.lex_analysis)
        for line_num, token_list in lex_analysis.items():
            self.already_checked = False
            specific_errors = None
            invalid_indent = False
            syntax_error = []
            self.currect_line_num = line_num
            
            # Extract token elements from the token list and store in syntax list
            syntax = [item[1] for item in token_list]
            syntax = [item for item in syntax if item != '\\t']
            code = self.get_code(line_num)

            # Check for invalid spaces then break if found and continue to the next iteration
            for item in token_list:
                # Check if the current item starts with '\s', '\s\s', or '\s\s\s'
                if item[0] == 'invalid_indent':
                    invalid_indent = True
                    syntax_error.append((code, f'Invalid Indent number', f'Expected 4 spaces or 1 tab'))
                    self.all_syntax_error.update({line_num: syntax_error})
                    break
                else:
                    break
            if invalid_indent == True:
                continue

            # Call function that calculates the accuracy of the syntax
            prod_rule_name, rule_syntax, actual_syntax, accuracy= self.calculate_accuracy(syntax)

            # If outside loop
            if self.in_loop == False and prod_rule_name == 'None' and rule_syntax == None:
                syntax_error.append((code, 'Invalid Loop Control', 'Must be inside loop statement'))
                self.all_syntax_error.update({line_num: syntax_error})
                continue
            
            if 'invalid' in syntax:
                syntax_error.append((code, 'Invalid Token', 'This is not recognized by the language'))
            
            elif accuracy == 1:
                continue                
            
            elif accuracy > 0.5:
                syntax_error.append((code, f'Invalid {prod_rule_name}', self.describe_error(actual_syntax, rule_syntax)))
            
            else: # Possible General Syntax Error
                if self.already_checked == False:
                    specific_errors = self.general_error_handler(actual_syntax)
                code = self.get_code(line_num)
                # If the syntax in that line has a specific error base on the error rules, append the specific description
                if specific_errors:
                    for error in specific_errors:
                         # Get the tokens that made the specific error (example: token token token !!!error_token error_token!!! token token)
                        syntax_error.append((code, f'Unexpected Token', error))
                # Else append, general description
                else:
                    syntax_error.append((code, f'Invalid Syntax', f'Syntax Error'))

            self.all_syntax_error.update({line_num: syntax_error})
        
        return copy(self.all_syntax_error)
        
    def describe_error(self, actual_syntax, rule_syntax):
        """
        Describes the error of the function by stating the actual and expected tokens.

        Parameters:
            actual_syntax (str): The actual terminal syntax in string format.
            rule_syntax (str): The expected terminal syntax in string format.

        Returns:
            expected (str): The expected token in the 'actual' token.
            actual (int): The actual token that is syntactically incorrect.
        """

        # Pair up actual and expected elements for comparison
        comparison = zip_longest(actual_syntax, rule_syntax, fillvalue='None')
        for actual, expected in comparison:
            if actual != expected:
                return f"Expected {expected} but encounted {actual}"
        return None
    
        
    def calculate_accuracy(self, actual_syntax):
        """
        Calculates the accuracy of the given syntax against the predefined production rules.

        Parameters:
            syntax (str): The syntax string to be analyzed.
            production_rules (dict): A dictionary containing production rules mapped to their respective arrays.

        Returns:
            matching_rule (str): The name of the matching production rule.
            max_accuracy (float): The maximum accuracy achieved.
        """
        
        max_accuracy = 0
        matching_rule = None
        rule_name = ""
        expected_syntax = ""
        
        if actual_syntax[0].endswith("_dt"):
            rule_name = "Declaration Statement"
        elif actual_syntax[0] == "out_kw":
            rule_name = "Output Statement"
            actual_syntax = self.normalize(actual_syntax)
        elif len(actual_syntax) >= 3 and actual_syntax[2] == "in_kw":
            rule_name = "Input Statement"
            actual_syntax = self.normalize(actual_syntax)
        elif actual_syntax[0] in ("import_kw", "from_kw"):
            rule_name = "Import Statement"
        elif actual_syntax[0] in ("while_kw","for_kw","repeat_kw"):
            self.in_loop = True
            actual_syntax = self.normalize(actual_syntax)
            rule_name = "Loop Statement"
        elif actual_syntax[0] == "func_kw":
            rule_name = "Function Statement"
            actual_syntax = self.converter(actual_syntax)
        elif actual_syntax[0] == "identifier":
            rule_name = "Assignment Statement"
            actual_syntax = self.converter(actual_syntax)
            actual_syntax = ['identifier' if x =='lit' else x for x in actual_syntax]
            actual_syntax = ['func' if x.endswith('_func') else x for x in actual_syntax]
        elif actual_syntax[0] == "comment":
            rule_name = "Comment Statement"
        elif actual_syntax[0] in ["if_kw", "elif_kw", "else_kw"]:
            if actual_syntax[0] == "if_kw":
                self.is_if_present = True
            elif actual_syntax[0] in ('elif_kw', 'else_kw') and not self.is_if_present:
                return None, None, actual_syntax, 0   
            
            ln = list(self.lex_analysis.keys())
            idx = ln.index(self.currect_line_num) if self.currect_line_num in ln else -1  # Find the index or set to -1 if not found
            ln = ln[idx+1:]
            
            is_else_kw_present = any('else_kw' in [t[1] for t in self.lex_analysis[line] if t] for line in ln)

            if actual_syntax[0] == "else_kw" or (actual_syntax[0] == "elif_kw" and not is_else_kw_present):  
                self.is_if_present = False

            rule_name = "If Statement"
            actual_syntax = self.converter(actual_syntax)
            
        elif actual_syntax[0] == "while_kw":
            rule_name = "While Statement"
            actual_syntax = self.converter(actual_syntax)

        elif ('skip_kw' in actual_syntax or 'stop_kw' in actual_syntax) and self.in_loop == True:
            rule_name = "Loop Statement"
            self.in_loop = False
            
        elif ('skip_kw' in actual_syntax or 'stop_kw' in actual_syntax) and self.in_loop == False:
            return 'None', None, actual_syntax, 0

        else:
            return None, None, actual_syntax, 0    
        
        for rule in PRODUCTION_RULE[rule_name]:
            rule_syntax = [element.strip('<>') for element in rule.split('><')]

            if len(rule_syntax) < len(actual_syntax) and rule_syntax[0] == actual_syntax[0]:
                 # Zipping the compound elements
                rule_syntax = self.generate_compound_prod_rules(rule_name, rule_syntax, actual_syntax)

            # print(f'Actual Syntax: {actual_syntax}\n Rule syntax: {rule_syntax}')

            zipped_tokens = zip(actual_syntax, rule_syntax)
            # Calculate accuracy as the ratio of correctly matched elements
            accuracy = sum(a == b for a, b in zipped_tokens) / max(len(actual_syntax), len(rule_syntax))

            # Update result if current rule has higher accuracy
            if accuracy > max_accuracy:
                max_accuracy = accuracy
                matching_rule = rule_name
                expected_syntax = rule_syntax

        return matching_rule, expected_syntax, actual_syntax, max_accuracy
    
    def normalize(self, actual_syntax):
        input_string = ' '.join(actual_syntax)

        if 'd_quo' in input_string:
            quo_tag = 'd_quo'
        elif 's_quo' in input_string:
            quo_tag = 's_quo'
        else:
            quo_tag = None

        # Replace the substrings matching the pattern with 'str_lit'
        input_string = re.sub(r'(?:d_quo|s_quo).+?l_curly', f'{quo_tag} str_lit l_curly', input_string, flags=re.DOTALL)
        input_string = re.sub(r'r_curly\s+(.*?)\s+(d_quo|s_quo)', f'r_curly str_lit {quo_tag}', input_string, flags=re.DOTALL)
        input_string = re.sub(r'\b\w+_func\b', 'func', input_string)

        # Split the output string back into a list
        return input_string.split()



    def generate_compound_prod_rules(self, rule_name, rule_syntax, actual_syntax):
        """
        Generate compound production rules based on the given rule_name and actual_syntax.

        Parameters:
            rule_name (str): The name of the production rule.
            rule_syntax (list): The current list of tokens representing the base production rule.
            actual_syntax (list): The list of tokens representing the actual syntax.

        Returns:
            rule_syntax (list): The updated rule_syntax after applying the compound production rules.
        """
        excess_actual_syntax = len(actual_syntax) - len(rule_syntax)

        if rule_name == 'Import Statement':
           while excess_actual_syntax > 0:
                rule_syntax.append('comma_delim')
                rule_syntax.append('identifier')
                excess_actual_syntax -= 2

        elif rule_name == 'Function Statement':
            rule_syntax = rule_syntax[:3] # <func_kw> <identifier> <l_paren>
            
            # Extract the parameters from the actual_syntax
            whole_parameter = self.extract_parameters(actual_syntax)
            
            # Group consecutive elements without 'comma_delim'
            param_list = [list(g) for k, g in groupby(whole_parameter, lambda x: x == 'comma_delim') if not k]

            for idx, param in enumerate(param_list):
                # Build a parameter string with '<>' around each token
                parameter = ''.join(f"<{token}>" for token in param)

                if parameter in DECLARATION_STMT or parameter in ASS_STMT:
                    # Add the parameter tokens to rule_syntax
                    rule_syntax.extend(parameter[1:-1].split('><'))
                    if idx < len(param_list) - 1:
                        rule_syntax.extend(['comma_delim'])
                else:
                    # Stop processing if the parameter is not in DECLARATION_STMT
                    break
            
            # Add closing tokens for function statement
            rule_syntax.extend(['r_paren', 'colon_delim'])
            
        if rule_name == 'If Statement':
            if f'{actual_syntax[0]} {actual_syntax[1]}' not in ["if_kw l_paren", "elif_kw l_paren"] or f'{actual_syntax[-2]} {actual_syntax[-1]}' != "r_paren colon_delim":
                if f'{actual_syntax[0]} {actual_syntax[1]}' not in ["if_kw l_paren", "elif_kw l_paren"] and f'{actual_syntax[-2]} {actual_syntax[-1]}' != "r_paren colon_delim":
                    rule_syntax = [actual_syntax[0], 'l_paren'] + actual_syntax[1:-2]
                    rule_syntax.extend('r_paren', 'colon_delim')
                    return rule_syntax
                elif f'{actual_syntax[0]} {actual_syntax[1]}' not in ["if_kw l_paren", "elif_kw l_paren"] and f'{actual_syntax[-2]} {actual_syntax[-1]}' == "r_paren colon_delim":
                    rule_syntax = [actual_syntax[0], 'l_paren'] + actual_syntax[1:]
                    return rule_syntax
                else:
                    rule_syntax = [actual_syntax[0:-2]]
                    rule_syntax.extend(['r_paren', 'colon_delim'])
                    return rule_syntax
                
            rule_syntax = rule_syntax[:2] # <if_kw> <l_paren>
            
            rule_syntax = self.check_compound_condt(rule_syntax, actual_syntax)

        elif rule_name == "While Statement":
            rule_syntax = rule_syntax[:2] # <while_kw> <l_paren>
            rule_syntax = self.check_compound_condt(rule_syntax, actual_syntax)

        if rule_name == 'Assignment Statement':
            actual_syntax = [item for item in actual_syntax if item != 'd_quo' and item != 's_quo']
            actual_syntax = ['identifier' if item == 'lit' else item for item in actual_syntax]
            excess_actual_syntax = len(actual_syntax) - len(rule_syntax)
            if excess_actual_syntax > 0:
                while excess_actual_syntax > 0:
                    if 'r_paren' in rule_syntax:
                        rule_syntax.remove('r_paren')
                    rule_syntax.append('comma_delim')
                    rule_syntax.append('identifier')
                    excess_actual_syntax -= 2
                rule_syntax.append('r_paren')

        return rule_syntax


    def extract_parameters(self, actual_syntax):
        """
        Extract parameters from the given actual_syntax.

        Parameters:
        - actual_syntax (list): The list of tokens representing the actual syntax.

        Returns:
        parameters (list) or None: The list of tokens representing the extracted parameters or None if no match is found.
        """
        start_index = actual_syntax.index('l_paren') + 1
        end_index = len(actual_syntax) - actual_syntax[::-1].index('r_paren') - 1

        result = actual_syntax[start_index:end_index]
        return result
    
    
    
    def converter(self, actual_syntax):
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
        converted_syntax = ['op' if token.endswith("_op") and token not in ["and_op", "or_op", "not_op"] else token for token in converted_syntax]

        return converted_syntax


    def get_code(self, line_number):
        """
        Retrieves the code corresponding to the given line number from the parsed file.

        Parameters:
            line_number (int): The line number for which the code is to be retrieved.

        Returns:
            code (str): The code on the specified line.
        """
        
        with open(self.file_path, 'r') as file:
            lines = file.readlines()
            return lines[line_number - 1].strip()
        
    def general_error_handler(self, actual_syntax):
        """
        Handles the general error. Finds the exact error using a dictionary to map
        the specific syntactical errors.

        Parameters:
            actual_syntax (list of tokens): list of tokens of the actual syntax that will be checked

        Return:
            list_of_errors (list of strings): list containing the error messages
        """

        list_of_errors = []  # List of errors if there are any

        # Batch processing in chunks of 3 tokens
        for i in range(2, len(actual_syntax)):
            chunk = actual_syntax[i - 2:i]
            list_of_returned_errors = self.in_error(chunk, actual_syntax[i - 3:i])
            
            if list_of_returned_errors:
                list_of_errors.extend(list_of_returned_errors)
                break

        return list_of_errors if list_of_errors else None
    
    def in_error(self, two_tokens, three_tokens=None):
        """
        Checks the dictionary and list in error_rule.py and returns a corresponding error message

        Parameters:
            two_tokens (list of tokens): list of tokens that are a size of 2 that is used for finding expected errors
            three_tokens (list of tokens or None): list of tokens that are a size of 3 that is used for finding unexpected errors

        Return:
            errors (list of strings): list containing the error messages
        """
        # Initialize variables and format the lists into strings
        errors = []
        two_bit_token = ' '.join(two_tokens)
        # Normalize the token using regular expression
        modified_token = re.sub(r'dt (\w+)', lambda match: f"dt {'error' if match.group(1) != 'colon_delim' else 'colon_delim'}", two_bit_token)
        if modified_token != 'dt error':
            modified_token = re.sub(r'dt (\w+)|out_kw (\w+)', lambda match: f"out_kw {'error' if match.group(2) and match.group(2) != 'colon_delim' else 'colon_delim' if match.group(1) == 'colon_delim' else 'error'}", two_bit_token)
        modified_token = re.sub(r'colon_delim (\w+)_kw|colon_delim (\w+)_met|colon_delim (\w+)_func', lambda match: f"colon_delim {'key' if match.group(2) and match.group(2) != 'colon_delim' else 'colon_delim' if match.group(3) == 'colon_delim' else 'error'}", modified_token)

        if three_tokens is not None and len(three_tokens) >= 2:
            temp = three_tokens[1]
            three_tokens[1] = 'error'
            three_bit_token = ' '.join(three_tokens)
        else:
            three_bit_token = None

        # Append to the error list the syntactic error
        if three_bit_token in UNEXPECTED_ERRORS and len(three_tokens) == 3:
            errors.append("Got an unexpected {} after {}".format(temp, three_tokens[0]))
        
        if modified_token in EXPECTED_ERRORS:
            expected_token = EXPECTED_ERRORS[modified_token]
            errors.append("Expected {} but encountered {}".format(expected_token, two_tokens[1]))
        
        if errors:
            self.already_checked = True
            return errors
        else:
            return None
        
        
    def check_compound_condt(self, rule_syntax, actual_syntax):
        condtl_stmt =  self.extract_parameters(actual_syntax)
        # print(f"condtl_stmt: {condtl_stmt}")

        condtl_list = []
        current_cond = []
        
        for idx, token in enumerate(condtl_stmt):
            if token not in ["and_kw", "or_kw", "r_paren", "l_paren", "and_op", "or_op"]:
                current_cond.append(token)
            else:
                if current_cond:
                    condtl_list.append(current_cond)
                condtl_list.append(token)
                current_cond = []
        
        if current_cond:
            condtl_list.append(current_cond)
        current_cond = []

        lparen_count = 0
        for idx, cond in enumerate(condtl_list):
            if cond == "l_paren" and (idx == 0 or condtl_list[idx-1] in ["and_kw", "or_kw", "and_op", "or_op"]):
                idx_rparen = next((idx for idx, val in reversed(list(enumerate(condtl_list))) if val == "r_paren"), None)
                if "r_paren" in condtl_list[idx + 1:] and (idx_rparen+1 == len(condtl_list) or condtl_list[idx+1] in ["and_kw", "or_kw", "and_op", "or_op"]):
                    lparen_count = 1
                    rule_syntax.append(cond)
                    continue
            elif cond == "r_paren" and lparen_count == 1 and  (idx+1 == len(condtl_list) or condtl_list[idx+1] in ["and_kw", "or_kw", "and_op", "or_op"]):
                lparen_count = 0
                rule_syntax.append(cond)
                continue
            elif cond in ["and_kw", "or_kw", "and_op", "or_op"]:
                rule_syntax.append(cond)
            else:
                condition = ''.join(f"<{token}>" for token in cond)
                if condition in LOGICAL_STMT or condition in RELATIONAL_STMT or condition == "<identifier>" or condition == "<bool_lit>":
                    rule_syntax.extend(condition[1:-1].split('><'))
                else:
                    break
        rule_syntax.extend(['r_paren', 'colon_delim'])  
        
        return rule_syntax