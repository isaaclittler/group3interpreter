def repl(prompt='lis.py> '):
    while True:
        val = eval(parse(raw_input(prompt)))
        if val is not None: 
            print(schemestr(val))

def schemestr(exp):
    if isinstance(exp, List):
        return '(' + ' '.join(map(schemestr, exp)) + ')' 
    else:
        return str(exp)
