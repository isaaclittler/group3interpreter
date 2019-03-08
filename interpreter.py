#Scheme types and how python will read them
Symbol = str              
Number = (int, float)
Atom   = (Symbol, Number)
List   = list
Exp    = (Atom, List)

def tokenize(chars: str):

def read_from_tokens(tokens: list):
    #Takes a sequence of tokens, and reads them
    if len(tokens) == 0:
        print("Nothing to intepret")
    token = tokens.pop(0) #removes and returns element 0 from list of tokens
    if token == "(":
        L = []
        while tokens[0] != ")":
            L.append(read_from_tokens(tokens)) # calls itself on updated tokens list
        tokens.pop(0) #removes ')'
        return L
    elif token == ")":
        print("unexpected )")
    else:
        return atom(token)

def atom(token: str):
    #Numbers are read as numbers, everything else is a symbol for now"
    try: return int(token) 
    except ValueError: #if token cant be returned as int
        try: return float(token)
        except ValueError: #if token cant be returned as float
            return Symbol(token)

