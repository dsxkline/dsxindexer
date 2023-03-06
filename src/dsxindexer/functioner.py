import re
import dsxindexer.configer as configer

def singleton(cls):
    instances = {}
    def get_instance(*args, **kwargs):
        if cls not in instances:
            instances[cls] = cls(*args, **kwargs)
        return instances[cls]
    return get_instance

@singleton
class Functioner:
    # 注册扩展类

    def __init__(self) -> None:
        self.function_exs = []
        self.variables = {}
        pass
    
    def register(self,cls):
        if cls not in self.function_exs:
            self.function_exs.append(cls)

    def remove(self,cls):
        if cls in self.function_exs:
            self.function_exs.remove(cls)

    def print(self,*values):
        print(*values)

    def SUM(self,a,b):
        return a+b
    
    def IF(self,a,b,c):
        if a:return b 
        else : return c

    def set_value(self,group:str,name:str,value:any):
        """保存变量值

        Args:
            group (str): 分支
            name (str): 变量名称
            value (any): 变量值
        """
        g = {}
        if group:
            if group in list(self.variables.keys()):
                g = self.variables.get(group)
        g[name] = value
        self.variables[group] = g

    def clear_variables(self):
        """一般一个过程计算完后需要清理
        一个表达式为一个过程，整个表达式计算完即清理
        """
        self.variables.clear()
    
    def get_value(self,group:str,name:str):
        """获取变量值

        Args:
            group (str): 分支
            name (str): 变量名称
        """
        g = {}
        if group:
            if group in list(self.variables.keys()):
                g = self.variables.get(group)
        if g.__len__()<=0 and self.variables.__len__()>0:
            # 找最新一个
            g:dict = list(self.variables.values())[-1]

        if name in list(g.keys()):
            return g.get(name)
    