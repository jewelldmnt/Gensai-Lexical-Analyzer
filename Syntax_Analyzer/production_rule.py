########################################
# ASSIGNMENT STATEMENTS
########################################
ASS = [
    "<identifier> <ass> <int_lit>",
    "<identifier> <ass> <str_lit>",
    "<identifier> <ass> <float_lit>",
    "<identifier> <ass> <bool_lit>"
    ]
ASS = [stmt.replace(" ", "") for stmt in ASS]


########################################
# DECLARATION STATEMENTS
########################################
DECLARATION_STMT = [
    "<int_dt> <colon_delim> <identifier> <ass> <int_lit>", 
    "<float_dt> <colon_delim> <identifier> <ass> <float_lit>",
    "<str_dt> <colon_delim> <identifier> <ass> <s tr_lit>",
    "<char_dt> <colon_delim> <identifier> <ass> <char_lit>",
    "<bool_dt> <colon_delim> <identifier> <ass> <bool_lit>"
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
    "<out_kw> <colon_delim> <bool_lit>"
]
OUT_STMT = [stmt.replace(" ", "") for stmt in OUT_STMT]


########################################
# PRODUCTION RULE
########################################
PRODUCTION_RULE = {
    "Declaration Statement": DECLARATION_STMT,
    "Output Statement": OUT_STMT
}

