unexpected_errors = [
    'func_kw error identifier',
    'import_kw error identifier',
    'from_kw error identifier',
    'l_paren error dt',
    'out_kw error colon_delim',
    'dt error colon_delim',
    'colon_delim error identifier',
    'int_dt error colon_delim',
    'float_dt error colon_delim',
    'str_dt error colon_delim',
    'char_dt error colon_delim',
    'bool_dt error colon_delim',
]
UNEXPECTED_ERRORS = [error.replace(" ", " ") for error in unexpected_errors]

EXPECTED_ERRORS = {
    'dt error':'colon_delim',
    'out_kw error':'colon_delim'
}
