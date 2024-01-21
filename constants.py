DIGITS = "0123456789"
ALPHABETS = "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz"
VALID_CHARS = ALPHABETS + DIGITS + "_"


########################################
# KEYWORDS AND DATA TYPES
########################################
kw = [
    "and", "as", "assert", "async", "await", "stop", "class", "skip",
    "func", "del", "elif", "else", "except", "finally", "for", "from", "global",
    "False", "True", "if", "import", "within", "is", "lambda",
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
# PRE-DEFINED FUNCTIONS
########################################
builtin_func = [
    'cal_velocity',
    'cal_displacement',
    'cal_force',
    'cal_work',
    'find_gene',
    'cal_gc',
    'cal_mw',
    'transcribe_dna',
    'cal_density',
    'cal_pct_vol',
    'cal_moles',
    'cal_concentration',
    'cal_NAI',
    'cal_vol_strain',
    'cal_intensity',
    'cal_magnitude',
    'abs',
    'max',
    'min',
    'len',
    'sorted',
    'reversed',
    'type'    
]

BUILTIN_FUNC = {func: f'{func}_func' for func in builtin_func}

builtin_met = [
    'capitalize',
    'upper',
    'lower',
    'isupper',
    'islower'
]

BUILTIN_MET = {met: f'{met}_met' for met in builtin_met}

########################################
# OPERATORS
########################################
ASS_OP = {
    '=': 'ass',
    '-=': 'sub_ass',
    '+=': 'add_ass',
    '*=': 'mul_ass',
    '/=': 'div_ass',
    '%=': 'mod_ass',
    '^=': 'pow_ass'
}


ARITHMETIC_OP = {
    '+': 'add_op',
    '-': 'sub_op',
    '*': 'mult_op',
    '/': 'div_op',
    '^': 'pow_op'
}

LOGICAL_OP = {
    '&&': 'and_op',
    '||': 'or_op',
    '!': 'not_op'
}

COMPARISON_OP = {
    '==': 'eq_op',
    '!=': 'neq_op',
    '>': 'gt_op',
    '<': 'lt_op',
    '>=': 'gte_op',
    '<=': 'lte_op'
}

OPERATORS = {**ASS_OP, **ARITHMETIC_OP, **LOGICAL_OP, **COMPARISON_OP}


########################################
# SPECIAL CHARACTERS
########################################

SPECIAL_CHAR = {
    ':': 'colon_delim',
    '(': 'l_paren',
    ')': 'r_paren',
    '[': 'l_bracket',
    ']': 'r_bracket',
    '{': 'l_curly',
    '}': 'r_curly',
    ';': 'semi_colon',
    '"': 'd_quo',
    "'": 's_quo',
    ".": 'period_delim',
    ",": 'comma_delim',
    "\\": 'backslash'
}