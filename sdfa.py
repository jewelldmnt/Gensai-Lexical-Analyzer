text = 'asdf asdfefasdf ea "asdfeafsad f" " asdfeafsd\' afefasdf"'

inside_quotes = []
current_word = ''
inside_quote = False
quote_char = ''

for char in text:
    if char in ('"', "'"):
        if not inside_quote:
            inside_quote = True
            quote_char = char
        elif char == quote_char:
            inside_quote = False
            inside_quotes.append(current_word)
            current_word = ''
    elif char.isspace() and not inside_quote:
        if current_word:
            inside_quotes.append(current_word)
            current_word = ''
    else:
        current_word += char

# Add the last word if the text ends inside quotes
if current_word:
    inside_quotes.append(current_word)

print(inside_quotes)