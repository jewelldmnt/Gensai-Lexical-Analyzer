from Lexical_Analyzer.lexical_analyzer import tokenizer
from Syntax_Analyzer.production_rule import *



class Syntax_Analyzer():
    def __init__(self):
        pass
    
    def parse(self, file):
        """
        Parses the contents of a file using a lexer.

        Parameters:
            file (str): The path to the file to be parsed.

        Returns:
            tokens (list): A list of tokens representing the parsed content.
        """
        
        self.file_path = file
        contents = open(file, 'r').read()
        lex_analysis = tokenizer(contents)
        syntax_errors = self.syntax_analyzer(lex_analysis)
        
        return syntax_errors
    
    
    def syntax_analyzer(self, lex_analysis):
        """
        Performs syntax analysis on the given lexeme analysis results.

        Parameters:
            lex_analysis (dict): A dictionary containing line numbers mapped to their respective token lists.

        Returns:
            all_syntax_errors (dict): A dictionary containing syntax errors mapped to their respective line numbers.
        """
        
        all_syntax_error = {}
        
        for line_num, token_list in lex_analysis.items():
            syntax_error = []
            
            # Extract token elements from the token list and store in syntax list
            syntax = [item[1] for item in token_list]
            code = self.get_code(line_num)
            prod_rule_name, prod_rule_idx, accuracy= self.calculate_accuracy(syntax)
            
            if 'invalid' in syntax:
                syntax_error.append((code, 'Invalid Token', 'This is not recognized by the language'))
            
            elif accuracy == 1:
                continue                
            
            elif accuracy > 0.5:
                syntax_error.append((code, f'Invalid {prod_rule_name}', self.describe_error(syntax, prod_rule_name, prod_rule_idx)))
            
            else: # General Syntax Error
                code = self.get_code(line_num) 
                syntax_error.append((code, f'Invalid Syntax', f'kase mama mo blue'))

            all_syntax_error.update({line_num: syntax_error})
        
        return all_syntax_error
        
        
    def describe_error(self, syntax, rule_name, rule_index):
        """
        Calculates the accuracy of the given syntax against the predefined production rules.

        Parameters:
            syntax (str): The syntax string to be analyzed.
            production_rules (dict): A dictionary containing production rules mapped to their respective arrays.

        Returns:
            matching_rule (str): The name of the matching production rule.
            matching_index (int): The index of the matching production rule array.
            max_accuracy (float): The maximum accuracy achieved.
        """
        # Extract expected elements from the specified production rule
        rule_elements = [element.strip('<>') for element in PRODUCTION_RULE[rule_name][rule_index].split('><')]    
        
        # Pair up actual and expected elements for comparison
        comparison = zip(syntax, rule_elements)
        
        for actual, expected in comparison:
            if actual != expected:
                return f"Expected {expected} but encounted {actual}"
        return None
    
    
        
    def calculate_accuracy(self, syntax):
        """
        Calculates the accuracy of the given syntax against the predefined production rules.

        Parameters:
            syntax (str): The syntax string to be analyzed.
            production_rules (dict): A dictionary containing production rules mapped to their respective arrays.

        Returns:
            matching_rule (str): The name of the matching production rule.
            matching_index (int): The index of the matching production rule array.
            max_accuracy (float): The maximum accuracy achieved.
        """
        
        max_accuracy = 0
        matching_rule = None
        matching_index = None

        # Iterate through each production rule and its array
        for rule_name, rule_array in PRODUCTION_RULE.items():
            
            # Iterate through each rule in the array
            for idx, rule in enumerate(rule_array):
                # Extract elements enclosed in <>
                rule_elements = [element.strip('<>') for element in rule.split('><')]
                
                # Pair up actual and expected elements for comparison
                zipped_tokens = zip(syntax, rule_elements)
                
                # Calculate accuracy as the ratio of correctly matched elements
                accuracy = sum(a == b for a, b in zipped_tokens) / max(len(syntax), len(rule_elements))

                # Update result if current rule has higher accuracy
                if accuracy > max_accuracy:
                    max_accuracy = accuracy
                    matching_rule = rule_name
                    matching_index = idx

        return matching_rule, matching_index, max_accuracy



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
