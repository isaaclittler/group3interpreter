
counter = 0
#converts a string to a list of tokens
def tokenize(source): #source: str
        return source.replace('(',' ( ').replace(')',' ) ').replace(';', ' ; ').replace('#|', ' #| ').replace('|#', ' |# ').split() #returns list


#reads a list of tokens and does stuff accordingly
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
                return type(token)

#makes the token either int, float, or symbol (the only options)
def type(token): #token: str
        try: return int(token) #returns int
        except ValueError:
                try: return float(token) #returns float
                except ValueError:
                        return token #Symbol(token)
                
#parses the program
def parse(code):
        L = tokenize(code)
        if len(L) == 0 or L[0] == ';':
                return []
              #  OR raise SyntaxError('write some code')
        elif L[0] != '(' and L[0] != '#|':
                raise SyntaxError('wrong start')
        else:
                return read_from_tokens(tokenize(code))

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
