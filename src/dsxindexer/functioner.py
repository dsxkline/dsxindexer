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
    
    def IF(self,a,b,c=None):
        if c==None:
            if a:return a
            else: return b
        if a:return b 
        else : return c

    def MAX(self,a,b):
        return max(a,b)

    def MIN(self,a,b):
        return min(a,b)
    
    def ABS(self,a):
        return abs(a)
    

    def set_value(self,namespace:str,name:str,value:any,func_name:str=None):
        """保存变量值

        Args:
            namespace (str): 命名空间
            name (str): 变量名称
            value (any): 变量值
            func_name (str): 函数内部变量
        """
        g = {}
        if namespace:
            if namespace in list(self.variables.keys()):
                g = self.variables.get(namespace)
                if func_name and isinstance(g,dict):
                    # 会进入函数内部变量场景
                    if func_name in g.keys():
                        g = g.get(func_name)
                    else:
                        g = {}
                        self.variables[namespace][func_name] = g
            elif func_name:
                self.variables[namespace] = g

        g[name] = value
        if func_name:
            self.variables[namespace][func_name] = g
        else:
            self.variables[namespace] = g

    def clear_variables(self):
        """一般一个过程计算完后需要清理
        一个表达式为一个过程，整个表达式计算完即清理
        """
        self.variables.clear()
    
    def get_value(self,namespace:str,name:str,func_name:str=None):
        """获取变量值

        Args:
            namespace (str): 命名空间
            name (str): 变量名称
            func_name (str): 函数内部变量
        """
        g = {}
        ns = None
        if namespace:
            if namespace in list(self.variables.keys()):
                ns = self.variables.get(namespace)
                if func_name and isinstance(ns,dict):
                    if func_name in ns.keys():
                        g = ns.get(func_name)
                else:
                    g = self.variables.get(namespace)
        if g.__len__()<=0 and self.variables.__len__()>0:
            # 找最新一个
            g:dict = list(self.variables.values())[-1]

        if name in list(g.keys()):
            return g.get(name)
        # 有时候函数内部引用外部命名空间的变量
        if ns:
            if name in ns.keys():
                return ns.get(name)
    