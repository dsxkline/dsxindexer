import re
import dsxindexer.configer as configer

class Functioner:
    # 注册扩展类
    function_exs = []
    
    def __init__(self) -> None:
        pass
    
    @staticmethod
    def register(cls):
        if cls not in Functioner.function_exs:
            Functioner.function_exs.append(cls)

    @staticmethod
    def remove(cls):
        if cls in Functioner.function_exs:
            Functioner.function_exs.remove(cls)

    def print(self,*values):
        print(*values)

    def SUM(self,a,b):
        return a+b
    
    def IF(self,a,b,c):
        if a:return b 
        else : return c