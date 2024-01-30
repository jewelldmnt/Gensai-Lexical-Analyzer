from Lexical_Analyzer.lexical_analyzer import tokenizer
from Syntax_Analyzer.production_rule import *
from copy import copy
from itertools import zip_longest




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
            
            else: # General Syntax Error
                code = self.get_code(line_num) 
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
            actual_syntax = self.converter(actual_syntax)
        elif actual_syntax[0] == "comment":
            rule_name = "Comment Statement"
        else:
            return None, None, actual_syntax, 0    
        
        
        for rule in PRODUCTION_RULE[rule_name]:
            rule_syntax = [element.strip('<>') for element in rule.split('><')]

            if len(rule_syntax) < len(actual_syntax) and rule_syntax[0] == actual_syntax[0]:
                 # Zipping the compound elements
                rule_syntax = self.compound_checker(rule_name, rule_syntax, actual_syntax)

            zipped_tokens = zip(actual_syntax, rule_syntax)
            
            # Calculate accuracy as the ratio of correctly matched elements
            accuracy = sum(a == b for a, b in zipped_tokens) / max(len(actual_syntax), len(rule_syntax))

            # Update result if current rule has higher accuracy
            if accuracy > max_accuracy:
                max_accuracy = accuracy
                matching_rule = rule_name
                expected_syntax = rule_syntax

        return matching_rule, expected_syntax, actual_syntax, max_accuracy


    
    def compound_checker(self, rule_name, rule_syntax, actual_syntax):
        """
        Converts the specific data types into 'dt' for BNF purposes in production rules.

        Parameters:
            rule_name (str): The name of the production rule.
            rule_syntax (list): List representing the production rule syntax.
            actual_syntax (list): List of actual syntax where certain tokens will be converted.

        Returns:
            converted_syntax (list): List of converted syntax.
        """
        excess_actual_syntax = len(actual_syntax) - len(rule_syntax)
        if rule_name == 'Import Statement':
            while excess_actual_syntax > 0:
                rule_syntax.append('comma_delim')
                rule_syntax.append('identifier')
                excess_actual_syntax -= 2
        
        elif rule_name == 'Function Statement':
            # Rule Syntax without the r_paren and colon_delim
            rule_syntax = rule_syntax[:-2]  
            while excess_actual_syntax > 0:
                rule_syntax.append('comma_delim')
                rule_syntax.append('dt')
                rule_syntax.append('colon_delim')
                rule_syntax.append('identifier')
                excess_actual_syntax -= 4
            rule_syntax.extend(['r_paren', 'colon_delim'])
        
        return rule_syntax
        
    
    def converter(self, syntax):
        """
        Converts the specific data types into 'dt' for bnf purposes in production rules

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
