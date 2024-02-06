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
        for line_num, token_list in lex_analysis.items():
            syntax_error = []
            
            # Extract token elements from the token list and store in syntax list
            syntax = [item[1] for item in token_list]
            code = self.get_code(line_num)
            # Call function that calculates the accuracy of the syntax
            prod_rule_name, rule_syntax, actual_syntax, accuracy= self.calculate_accuracy(syntax)
            
            if 'invalid' in syntax:
                syntax_error.append((code, 'Invalid Token', 'This is not recognized by the language'))
            
            elif accuracy == 1:
                continue                
            
            elif accuracy > 0.5:
                syntax_error.append((code, f'Invalid {prod_rule_name}', self.describe_error(actual_syntax, rule_syntax)))
            
            else: # Possible General Syntax Error
                specific_errors = self.general_error_handler(actual_syntax)
                code = self.get_code(line_num)
                # If the syntax in that line has a specific error base on the error rules, append the specific description
                if specific_errors:
                    for error in specific_errors:
                         # Get the tokens that made the specific error (example: token token token !!!error_token error_token!!! token token)
                        syntax_error.append((code, f'Unexpected Token', error))
                # Else append, general description
                else:
                    syntax_error.append((code, f'Invalid Syntax', f'kase mama mo blue'))

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
        
        if actual_syntax[0].endswith("_dt"):
            rule_name = "Declaration Statement"
        elif actual_syntax[0] == "out_kw":
            rule_name = "Output Statement"
        elif actual_syntax[0] in ("import_kw", "from_kw"):
            rule_name = "Import Statement"
        elif actual_syntax[0] == "func_kw":
            rule_name = "Function Statement"
        elif actual_syntax[0] == "comment":
            rule_name = "Comment Statement"
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

                if parameter in DECLARATION_STMT:
                    # Add the parameter tokens to rule_syntax
                    rule_syntax.extend(parameter[1:-1].split('><'))
                    if idx < len(param_list) - 1:
                        rule_syntax.extend(['comma_delim'])
                else:
                    # Stop processing if the parameter is not in DECLARATION_STMT
                    break
            
            # Add closing tokens for function statement
            rule_syntax.extend(['r_paren', 'colon_delim'])

        return rule_syntax


    def extract_parameters(self, actual_syntax):
        """
        Extract parameters from the given actual_syntax.

        Parameters:
        - actual_syntax (list): The list of tokens representing the actual syntax.

        Returns:
        parameters (list) or None: The list of tokens representing the extracted parameters or None if no match is found.
        """
        actual_syntax = ' '.join(actual_syntax)
        
        # Define the pattern to match the desired syntax
        pattern = r"l_paren (.+?) r_paren"

        # Use regular expression to find matches
        matches = re.search(pattern, actual_syntax)

        # Extract the parameters if matches are found
        if matches:
            parameters = matches.group(1).split()
            return parameters
        else:
            return None
    
    
    
    def converter(self, syntax):
        """
        Converts the specific data types into 'dt' for bnf purposes in production rules.
        While checking first

        Parameters:
            syntax (list): List of actual syntax where certain tokens will be converted.

        Returns:
            matching_rule (list): ist of converted syntax.

        """
        converted_syntax = ['dt' if token in DATA_TYPES else token for token in syntax]
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
        modified_token = re.sub(r'(\w+)_dt (\w+)', lambda match: f"dt {'error' if match.group(2) != 'colon_delim' else 'colon_delim'}", two_bit_token)
        modified_token = re.sub(r'(\w+)_dt (\w+)|out_kw (\w+)', lambda match: f"out_kw {'error' if match.group(2) and match.group(2) != 'colon_delim' else 'colon_delim' if match.group(3) == 'colon_delim' else 'error'}", modified_token)

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
            errors.append("Expected a {} but encountered {}".format(expected_token, two_tokens[1]))
        
        if errors:
            return errors
        else:
            return None