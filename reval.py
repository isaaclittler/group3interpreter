def eval(x, env=global_env):
    if isinstance(x, Symbol):   
        return env.find(x)[x]
    elif not isinstance(x, List):
        return x   
    op, *args = x       
    if op == 'quote':            
        return args[0]
    elif op == 'if':             
        (test, conseq, alt) = args
        exp = (conseq if eval(test, env) else alt)
        return eval(exp, env)
    elif op == 'define':        
        (symbol, exp) = args
        env[symbol] = eval(exp, env)
    elif op == 'set!':           
        (symbol, exp) = args
        env.find(symbol)[symbol] = eval(exp, env)
    elif op == 'lambda':         
        (parms, body) = args
        return Procedure(parms, body, env)
    else:                       
        proc = eval(op, env)
        vals = [eval(arg, env) for arg in args]
        return proc(*vals)
