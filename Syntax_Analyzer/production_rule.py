DATA_TYPES = [
    'int_dt', 'float_dt', 'str_dt', 'char_dt', 'bool_dt'
]

########################################
# ASSIGNMENT STATEMENTS
########################################
ASS = [
    "<identifier> <ass> <int_lit>",
    "<identifier> <ass> <str_lit>",
    "<identifier> <ass> <float_lit>",
    "<identifier> <ass> <bool_lit>",
    "<identifier> <ass> <char_lit>"
    ]
ASS = [stmt.replace(" ", "") for stmt in ASS]

########################################
# DECLARATION STATEMENTS
########################################
DECLARATION_STMT = [
    # Declaration for literals
    "<int_dt> <colon_delim> <identifier> <ass> <int_lit>", 
    "<float_dt> <colon_delim> <identifier> <ass> <float_lit>",
    "<str_dt> <colon_delim> <identifier> <ass> <s_quo> <str_lit> <s_quo>",
    "<str_dt> <colon_delim> <identifier> <ass> <d_quo> <str_lit> <d_quo>",
    "<char_dt> <colon_delim> <identifier> <ass> <char_lit>",
    "<bool_dt> <colon_delim> <identifier> <ass> <bool_lit>",
    
    # Declerations for variables or identifier
    "<int_dt> <colon_delim> <identifier> <ass> <identifier>", 
    "<float_dt> <colon_delim> <identifier> <ass> <identifier>",
    "<str_dt> <colon_delim> <identifier> <ass> <identifier>",
    "<char_dt> <colon_delim> <identifier> <ass> <identifier>",
    "<bool_dt> <colon_delim> <identifier> <ass> <identifier>",
    
    # Declarations of identifier but without values
    "<int_dt> <colon_delim> <identifier>",
    "<float_dt> <colon_delim> <identifier>",
    "<str_dt> <colon_delim> <identifier>",
    "<char_dt> <colon_delim> <identifier>",
    "<bool_dt> <colon_delim> <identifier>"
]
DECLARATION_STMT = [stmt.replace(" ", "") for stmt in DECLARATION_STMT]

########################################
# OUTPUT STATEMENTS
########################################
OUT_STMT = [
    "<out_kw> <colon_delim> <identifier>",
    "<out_kw> <colon_delim> <int_lit>",
    "<out_kw> <colon_delim> <float_lit>",
    "<out_kw> <colon_delim> <identifier>",
    "<out_kw> <colon_delim> <bool_lit>",
    "<out_kw> <colon_delim> <str_lit>"
]
OUT_STMT = [stmt.replace(" ", "") for stmt in OUT_STMT]

########################################
# IMPORT STATEMENTS
########################################
IMP_STMT = [
    "<import_kw> <identifier>",
    "<from_kw> <identifier> <import_kw> <identifier>",
    "<import_kw> <identifier> <as_kw> <identifier>",
    "<from_kw> <identifier> <import_kw> <identifier> <as_kw> <identifier>"
]
IMP_STMT = [stmt.replace(" ", "") for stmt in IMP_STMT]

########################################
# FUNCTION RULE
########################################
FNC_STMT = [
    "<func_kw> <identifier> <l_paren> <r_paren> <colon_delim>",
    "<func_kw> <identifier> <l_paren> <int_dt> <colon_delim> <identifier> <r_paren> <colon_delim>",
    "<func_kw> <identifier> <l_paren> <float_dt> <colon_delim> <identifier> <r_paren> <colon_delim>",
    "<func_kw> <identifier> <l_paren> <str_dt> <colon_delim> <identifier> <r_paren> <colon_delim>",
    "<func_kw> <identifier> <l_paren> <char_dt> <colon_delim> <identifier> <r_paren> <colon_delim>",
    "<func_kw> <identifier> <l_paren> <bool_dt> <colon_delim> <identifier> <r_paren> <colon_delim>",
    "func_kw> <identifier> <l_paren> <int_dt> <colon_delim> <identifier> <ass> <int_lit> <r_paren> <colon_delim>", 
    "func_kw> <identifier> <l_paren> <float_dt> <colon_delim> <identifier> <ass> <float_lit> <r_paren> <colon_delim>",
    "func_kw> <identifier> <l_paren> <str_dt> <colon_delim> <identifier> <ass> <s_quo> <str_lit> <s_quo> <r_paren> <colon_delim>",
    "func_kw> <identifier> <l_paren> <str_dt> <colon_delim> <identifier> <ass> <d_quo> <str_lit> <d_quo> <r_paren> <colon_delim>",
    "func_kw> <identifier> <l_paren> <char_dt> <colon_delim> <identifier> <ass> <char_lit> <r_paren> <colon_delim>",
    "func_kw> <identifier> <l_paren> <bool_dt> <colon_delim> <identifier> <ass> <bool_lit> <r_paren> <colon_delim>",
]
FNC_STMT = [stmt.replace(" ", "") for stmt in FNC_STMT]

########################################
# COMMENT RULE
########################################
COMMENT_STMT = ["<comment>"]

########################################
# CONDITIONAL STATEMENTS
########################################
RELATIONAL_STMT = [
    "<identifier> <op> <lit>",
    "<identifier> <l_paren> <op> <r_paren> <lit>",
    "<identifier> <op> <identifier>",
    "<identifier> <l_paren> <op> <r_paren> <identifier>",
    "<lit> <op> <lit>",
    "<lit> <l_paren> <op> <r_paren> <lit>"
]
RELATIONAL_STMT = [stmt.replace(" ", "") for stmt in RELATIONAL_STMT]

LOGICAL_STMT = [
    "<identifier> <and_op> <identifier>",
    "<identifier> <or_op> <identifier>",
    "<identifier> <and_kw> <identifier>",
    "<identifier> <or_kw> <identifier>",
    "<not_op> <identifier>",
    "<not_kw> <identifier>"
]
LOGICAL_STMT = [stmt.replace(" ", "") for stmt in LOGICAL_STMT]

IF_STMT = [
    "<if_kw> <l_paren> <identifier> <r_paren> <colon_delim>",
    "<elif_kw> <l_paren> <identifier> <r_paren> <colon_delim>",
    "<if_kw> <l_paren> <lit> <r_paren> <colon_delim>",
    "<elif_kw> <l_paren> <lit> <r_paren> <colon_delim>",
    "<else_kw> <colon_delim>"
]
IF_STMT = [stmt.replace(" ", "") for stmt in IF_STMT]


########################################
# CONDITIONAL STATEMENTS
########################################
WHILE_STMT = [
    "<while_kw> <l_paren> <identifier> <r_paren> <colon_delim>",
    "<while_kw> <l_paren> <lit> <r_paren> <colon_delim>"
]
WHILE_STMT = [stmt.replace(" ", "") for stmt in WHILE_STMT]

########################################
# PRODUCTION RULE
########################################
PRODUCTION_RULE = {
    "Declaration Statement": DECLARATION_STMT,
    "Output Statement": OUT_STMT,
    "Import Statement": IMP_STMT,
    "Function Statement": FNC_STMT,
    "Comment Statement": COMMENT_STMT,
    "If Statement": IF_STMT,
    "While Statement": WHILE_STMT
}

