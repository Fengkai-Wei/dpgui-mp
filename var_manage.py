import vars 
def add_var(key,value):
    vars.var_dict.update({key:value})
def rm_var(key,dict):
    if key in dict:
        del dict[key]
    else:
        pass