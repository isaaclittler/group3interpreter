import math
import operator as op
from collections import ChainMap as Environment

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

class Procedure(object): #scheme procedure
    def __init__(self, parms, body, env):
        self.parms, self.body, self.env = parms, body, env
    def __call__(self, *args):
        env =  Environment(dict(zip(self.parms, args)), self.env)
        return eval(self.body, env)

def tokenize(source): #source: str
    #returns list
    return source.replace('(',' ( ').replace(')',' ) ').replace(';', ' ; ').replace('#|', ' #| ').replace('|#', ' |# ').split()

counter = 0
def read_from_tokens(tokens): #tokens: list
        token = tokens.pop(0)
        if token == '(':
                tree = []
                global counter
                counter += 1
                while tokens[0] != ')':
                        temp = read_from_tokens(tokens)
                        if temp is not None:
                                tree.append(temp)
                        if counter<0:
                                raise SyntaxError('incorrect parenthesis')
                tokens.pop(0) #removes ')'
                counter -= 1
                if (counter > 0):
                        return tree #tree: list
                else:
                        if len(tokens) == 0 or tokens.pop(0) == ';':
                                return tree
                        else:
                                raise SyntaxError('extra stuff after last parenthesis')
                                
        elif token == ')':
                raise SyntaxError('you forgot a ( for your )')
        elif token == ';':
                return tree
        elif token == '#|':
                while len(tokens) > 0 and tokens[0] != '|#':
                        tokens.pop(0)
                if(len(tokens) == 0):
                        return -1
                else:
                        tokens.pop(0) #removes '|#'
                        if len(tokens) > 0:
                                return read_from_tokens(tokens)
                        else:
                                return []
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

def run(filename):
    code = read_from_file(filename)
    for i in range(len(code)):
        if code[i] != []:
            print(eval(code[i]))


def read_from_file(filename):
        flag = False
        L = []
        with open(filename) as f:
                for line in f:
                      if(flag):
                               s = line
                               test = tokenize(s)
                               try:
                                    index = test.index('|#')
                               except ValueError:  
                                    index = -1
                               if(index != -1):
                                        while test[0] != '|#':
                                             test.pop(0)
                                        test.pop(0)
                                        test = "".join(test)
                                        temp =  parse(test)
                                        flag = False
                               else:
                                        continue
                      else:
                              temp =  parse(line)
                      if(temp == -1):
                              flag = True
                              continue
                      L.append(temp) #return
                if(flag):
                      raise SyntaxError('you forgot to end the comment')
        return L

def eval(x, env = global_env):
    if isinstance(x, Symbol):        
        return env[x]
    elif isinstance(x, Number):      
        return x
    elif x[0] == 'quote':
        (_, exp) = x
        return exp
    elif x[0] == 'if':
        test = x[1]
        conseq = x[2]
        alt = x[3]
        #(_, test, conseq, alt) = x 
        return eval((conseq if eval(test, env) else alt), env)
    elif x[0] == 'define':           
        (_, symbol, exp) = x
        env[symbol] = eval(exp, env)
    elif x[0] == 'lambda':
        (_, parms, body) = x
        return Procedure(parms, body, env)
    else:                            
        proc = eval(x[0], env)
        args = [eval(arg, env) for arg in x[1:]]
        return proc(*args)
