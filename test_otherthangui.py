import vars
import var_manage as vm
vars.init()
vm.add_var(key="22222",value=222222222)
print(vars.var_dict)
vm.add_var(key='ddd',value='dededededede')

print(vars.var_dict)
vm.rm_var(key='ddd',dict=vars.var_dict)
print(vars.var_dict)
vm.rm_var(key='dddedede',dict=vars.var_dict)
print(vars.var_dict)