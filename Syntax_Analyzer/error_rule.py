unexpected_errors = [
    'func_kw error identifier',
    'import_kw error identifier',
    'from_kw error identifier',
    'l_paren error dt',
    'out_kw error colon_delim',
    'dt error colon_delim',
    'colon_delim error identifier',
]
UNEXPECTED_ERRORS = [error.replace(" ", " ") for error in unexpected_errors]

expected_errors = [
    'str_dt identifier'
]
EXPECTED_ERRORS = [error.replace(" ", " ") for error in expected_errors]