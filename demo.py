import math
import operator as op

def standard_env():
    env = {}
    env.update(vars(math)) 
    env.update({
        '+':op.add, '-':op.sub, '*':op.mul, '/':op.truediv, 
        '>':op.gt, '<':op.lt, '>=':op.ge, '<=':op.le, '=':op.eq, 
        'abs':     abs,
        'append':  op.add,  
        'apply':   lambda proc, args: proc(*args),
        'begin':   lambda *x: x[-1],
        'car':     lambda x: x[0],
        'cdr':     lambda x: x[1:], 
        'cons':    lambda x,y: [x] + y,
        'eq?':     op.is_, 
        'equal?':  op.eq, 
        'length':  len, 
        'list':    lambda *x: list(x), 
        'list?':   lambda x: isinstance(x,list), 
        'map':     lambda *args: list(map(*args)),
        'max':     max,
        'min':     min,
        'not':     op.not_,
        'null?':   lambda x: x == [], 
        'number?': lambda x: isinstance(x, Number),   
        'procedure?': callable,
        'round':   round,
        'symbol?': lambda x: isinstance(x, Symbol),
    })
    return env

global_env = standard_env()

#Scheme types and how python will read them
Symbol = str              
Number = (int, float)
Atom   = (Symbol, Number)
List   = list
Exp    = (Atom, List)

def tokenize(source): #source: str
    #returns list
    return source.replace('(',' ( ').replace(')',' ) ').replace(';', ' ; ').replace('#|', ' #| ').replace('|#', ' |# ').split()

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

def atom(token): #token is a string
    #Numbers are read as numbers, everything else is a symbol for now"
    try: return int(token) 
    except ValueError: #if token cant be returned as int
        try: return float(token)
        except ValueError: #if token cant be returned as float
            return Symbol(token)
                
#parses the program
def parse(code):
        L = tokenize(code)
        if len(L) == 0:
                return []
              #  OR raise SyntaxError('write some code')
        elif L[0] == ';':
               return [];
        elif L[0] != '(' and L[0] != '#|':
                raise SyntaxError('wrong start')
        else:
            return read_from_tokens(tokenize(code))

def read_from_file(filename):
    L = []
    with open(filename) as f:
        for line in f:
            L.append(parse(line)) #return
    return L

def eval(x, env = global_env):
    if isinstance(x, Symbol):        
        return env[x]
    elif isinstance(x, Number):      
        return x                
    elif x[0] == 'if':
        test = x[1]
        conseq = x[2]
        alt = x[3]
        #(_, test, conseq, alt) = x 
        return eval((conseq if eval(test, env) else alt), env)
    elif x[0] == 'define':           
        (_, symbol, exp) = x
        env[symbol] = eval(exp, env)
    else:                            
        proc = eval(x[0], env)
        args = [eval(arg, env) for arg in x[1:]]
        return proc(*args)
