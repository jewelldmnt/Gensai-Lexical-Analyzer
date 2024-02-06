DATA_TYPES = [
    'int_dt', 'float_dt', 'str_dt', 'char_dt', 'bool_dt'
]
COMPARISON_OP = [
    'eq_op',
    'neq_op',
    'gt_op',
    'lt_op',
    'gte_op',
    'lte_op'
]

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
# INPUT STATEMENTS
########################################
IN_STMT = [
    "<in_kw> <l_paren> <r_paren>",
    "<in_kw> <l_paren> <s_quo> <str_lit> <s_quo> <r_paren>",
    "<in_kw> <l_paren> <d_quo> <str_lit> <d_quo> <r_paren>",
    "<in_kw> <l_paren> <d_quo> <char_lit> <d_quo> <r_paren>",
    "<in_kw> <l_paren> <s_quo> <char_lit> <s_quo> <r_paren>",
    "<in_kw> <l_paren> <str_lit> <r_paren>",
    "<in_kw> <l_paren> <identifier> <r_paren>",
    "<in_kw> <l_paren> <s_quo> <identifier> <s_quo> <r_paren>",
    "<in_kw> <l_paren> <d_quo> <identifier> <d_quo> <r_paren>",
    "<in_kw> <l_paren> <d_quo> <str_lit> <l_curly> <identifier> <r_curly> <str_lit> <d_quo> <r_paren>",
    "<in_kw> <l_paren> <d_quo> <str_lit> <l_curly> <identifier> <r_curly> <d_quo> <r_paren>",
    "<in_kw> <l_paren> <d_quo> <l_curly> <identifier> <r_curly> <str_lit> <l_curly> <identifier> <r_curly> <str_lit> <d_quo> <r_paren>",
    "<in_kw> <l_paren> <d_quo> <l_curly> <identifier> <r_curly> <str_lit> <l_curly> <identifier> <r_curly> <d_quo> <r_paren>",
]
IN_STMT = [stmt.replace(" ", "") for stmt in IN_STMT]

########################################
# OUTPUT STATEMENTS
########################################
OUT_STMT = [
    "<out_kw> <colon_delim> <identifier>",
    "<out_kw> <colon_delim> <int_lit>",
    "<out_kw> <colon_delim> <float_lit>",
    "<out_kw> <colon_delim> <identifier>",
    "<out_kw> <colon_delim> <bool_lit>",
    "<out_kw> <colon_delim> <d_quo> <str_lit> <d_quo>",
    "<out_kw> <colon_delim> <s_quo> <str_lit> <s_quo>",
    "<out_kw> <colon_delim> <d_quo> <char_lit> <d_quo>",
    "<out_kw> <colon_delim> <s_quo> <char_lit> <s_quo>",
    "<out_kw> <colon_delim> <s_quo> <identifier> <s_quo>",
    "<out_kw> <colon_delim> <d_quo> <identifier> <d_quo>",
    "<out_kw> <colon_delim> <d_quo> <str_lit> <l_curly> <identifier> <r_curly> <str_lit> <d_quo>",
    "<out_kw> <colon_delim> <d_quo> <str_lit> <l_curly> <identifier> <r_curly> <d_quo>",
    "<out_kw> <colon_delim> <d_quo> <l_curly> <identifier> <r_curly> <str_lit> <l_curly> <identifier> <r_curly> <str_lit> <d_quo>",
    "<out_kw> <colon_delim> <d_quo> <l_curly> <identifier> <r_curly> <str_lit> <l_curly> <identifier> <r_curly> <d_quo>",
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

########################################
# LOGICAL STATEMENTS
########################################
LOGICAL_STMT = [
    "<identifier> <and_op> <identifier>",
    "<identifier> <or_op> <identifier>",
    "<not_op> <identifier>"
]
LOGICAL_STMT = [stmt.replace(" ", "") for stmt in LOGICAL_STMT]
########################################
# CONDITIONAL STATEMENTS
########################################
CONDT_STMT = [
    "<if_kw> <l_paren> <[CONDITION]> <r_paren> <colon_delim>"
]
CONDT_STMT = [stmt.replace(" ", "") for stmt in CONDT_STMT]

########################################
# LOOP STATEMENTS
########################################
LOOP_STMT = [
    # repeat loops
    "<repeat_kw> <int_lit> <colon_delim>",
    "<repeat_kw> <identifier> <colon_delim>",
    "<repeat_kw> <func> <l_paren> <r_paren> <colon_delim>",
    "<repeat_kw> <func> <l_bracket> <int_lit> <r_bracket> <colon_delim>",
    "<repeat_kw> <func> <l_bracket> <identifier> <r_bracket> <colon_delim>",
    "<repeat_kw> <identifier> <l_paren> <r_paren> <colon_delim>",
    # loop controls
    "stop_kw",
    "skip_kw",
    # for loops
    "<for_kw> <identifier> <in_kw> <identifier> <colon_delim>",
    "<for_kw> <identifier> <in_kw> <identifier> <l_bracket> <int_lit> <r_bracket> <colon_delim>",
    "<for_kw> <identifier> <in_kw> <identifier> <l_bracket> <r_bracket> <colon_delim>",
    "<for_kw> <identifier> <in_kw> <identifier> <l_bracket> <identifier> <r_bracket> <colon_delim>",
    "<for_kw> <identifier> <in_kw> <identifier> <l_paren> <identifier> <r_paren> <colon_delim>",
    "<for_kw> <identifier> <in_kw> <identifier> <l_paren> <r_paren> <colon_delim>",
    "<for_kw> <identifier> <within_kw> <identifier> <colon_delim>",
    "<for_kw> <identifier> <within_kw> <identifier> <l_bracket> <int_lit> <r_bracket> <colon_delim>",
    "<for_kw> <identifier> <within_kw> <identifier> <l_bracket> <r_bracket> <colon_delim>",
    "<for_kw> <identifier> <within_kw> <identifier> <l_bracket> <identifier> <r_bracket> <colon_delim>",
    "<for_kw> <identifier> <within_kw> <identifier> <l_paren> <identifier> <r_paren> <colon_delim>",
    "<for_kw> <identifier> <within_kw> <identifier> <l_paren> <r_paren> <colon_delim>",
    # while loops
    "<while_kw> <lit> <comp_op> <lit> <colon_delim>",
    "<while_kw> <lit> <colon_delim>",
    "<while_kw> <> <> <> <>",
    "<> <> <> <> <>",
]
LOOP_STMT = [stmt.replace(" ", "") for stmt in LOOP_STMT]

########################################
# ASSIGNMENT STATEMENTS
########################################
ASS_STMT = [
    '<identifier> <ass> <lit>',
    '<identifier> <ass> <identifier>',
    '<identifier> <ass> <s_quo> <lit> <s_quo>',
    '<identifier> <ass> <d_quo> <lit> <d_quo>',
    '<identifier> <ass> <identifier> <l_bracket> <r_bracket>',
    '<identifier> <ass> <identifier> <l_bracket> <lit> <r_bracket>',
    '<identifier> <ass> <identifier> <l_bracket> <identifier> <r_bracket>',
    '<identifier> <ass> <identifier> <l_paren> <r_paren>',
    '<identifier> <ass> <identifier> <l_paren> <identifier> <r_paren>',
    '<while_kw> <identifier> <comp_op> <>'
]
ASS_STMT = [stmt.replace(" ", "") for stmt in ASS_STMT]


########################################
# PRODUCTION RULE
########################################
PRODUCTION_RULE = {
    "Declaration Statement": DECLARATION_STMT,
    "Output Statement": OUT_STMT,
    "Input Statement": IN_STMT,
    "Import Statement": IMP_STMT,
    "Function Statement": FNC_STMT,
    "Comment Statement": COMMENT_STMT,
    "If Statement": CONDT_STMT,
    "Loop Statement":LOOP_STMT,
    "Assignment Statement": ASS_STMT
}

