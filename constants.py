DIGITS = "0123456789"
ALPHABETS = "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz"
VALID_CHARS = ALPHABETS + DIGITS + "_"


########################################
# KEYWORDS AND DATA TYPES
########################################
kw = [
    "and", "as", "assert", "async", "await", "break", "class", "continue",
    "def", "del", "elif", "else", "except", "finally", "for", "from", "global",
    "False", "True", "if", "import", "withi n", "is", "lambda",
    "None", "not", "or", "pass", "raise", "repeat", "return", "try", "while",
    "out", "in"
]

DATA_TYPES = {
    'int': 'int_dt',
    'float': 'float_dt',
    'str': 'string_dt',
    'char': 'char_dt',
    'bool': 'bool_dt'
}

KEYWORDS = {keyword: f'{keyword}_kw' for keyword in kw}
KEYWORDS.update(DATA_TYPES)



########################################
# OPERATORS
########################################
ASS_OP = {
    '=': 'assign_op',
    '+=': 'add_assign_op',
    '-=': 'subtract_assign_op',
    '*=': 'multiply_assign_op',
    '/=': 'divide_assign_op',
    '%=': 'modulo_assign_op',
    '^=': 'power_assign_op'
}

ARITHMETIC_OP = {
    '+': 'addition_op',
    '-': 'subtraction_op',
    '*': 'multiplication_op',
    '/': 'division_op',
    '^': 'power_op',
    '%': 'modulus_op'
}


LOGICAL_OP = {
    '&': 'and_op',
    '||': 'or_op',
    '!': 'not_op'
}

COMPARISON_OP = {
    '==': 'equal_op',
    '!=': 'not_equal_op',
    '>': 'greater_than_op',
    '<': 'less_than_op',
    '>=': 'greater_than_or_equal_op',
    '<=': 'less_than_or_equal_op'
}

OPERATORS = {**ASS_OP, **ARITHMETIC_OP, **LOGICAL_OP, **COMPARISON_OP}


########################################
# SPECIAL CHARACTERS
########################################

SPECIAL_CHAR = {
    ':': 'colon_delim',
    '(': 'left_paren',
    ')': 'right_paren',
    '[': 'left_bracket',
    ']': 'right_bracket',
    '{': 'left_curly',
    '}': 'right_curly',
    ';': 'semi_colon',
    '"': 'double_quotation',
    "'": 'single_quotation'
    
}