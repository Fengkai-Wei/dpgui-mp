import vars 
def add_var(key,value):
    vars.var_dict.update({key:value})
def rm_var(key):
    if key in vars.var_dict:
        del vars.var_dict[key]
    else:
        pass