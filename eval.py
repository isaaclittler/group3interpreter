def eval(x: Exp, env=global_env):
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
