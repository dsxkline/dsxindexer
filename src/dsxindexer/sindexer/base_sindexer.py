
from typing import List

from dsxindexer.configer import Cursor

from dsxindexer.functioner import Functioner

from dsxindexer.parser import Parser

from dsxindexer.tokenizer import Lexer
from dsxindexer.sindexer.fomulas import Formulas
from dsxindexer.sindexer.models.kline_model import KlineModel

class SindexerVarNotFoundError(BaseException):
    pass

class SindexerResult:
    def __init__(self,name:str) -> None:
        self.name:str = name

class BaseSindexer:
    # 继承子类需要重写此字段
    __typename__:str = None
    # 需要从公式的计算结果导出的变量名称
    __exportvars__:tuple = None
    # 临时数据
    temp = []
    def __init__(self,klines:List[KlineModel],cursor:Cursor) -> None:
        # k线数据
        self.klines:List[KlineModel] = klines
        # 当前索引
        self.cursor:Cursor = cursor
        # 自己也注册进公式解析器函数库
        Functioner().register(self)
        # 命名空间
        self.namespace = None

    def formula(self):
        pass

    def save_temp(self,name,val):
        obj = {}
        if self.cursor.index<self.temp.__len__():
            obj = self.temp[self.cursor.index]
        else:
            self.temp.append(obj)
        obj[name] = val
        self.temp[self.cursor.index] = obj
    
    def get_temp(self,name,index):
        if index<self.temp.__len__():
                obj:dict = self.temp[index]
                if name in list(obj.keys()):
                    return obj.get(name)

    def execute(self):
        f = self.formula()
        if f:
            # 命名空间初始化为公式主名称，递归会继承
            self.namespace = self.__typename__
            result = self.parser(f)
            return result

    def parser(self,expresions):
        # 词法分析器,表达式分词并标记类型
        lexer = Lexer(expresions)
        # 语法解析器，执行操作符，函数等功能
        parser = Parser(lexer,namespace=self.namespace)
        # 解析并返回结果
        ps = parser.parse()
        # 导出变量
        result = self.export_variables(ps)
        # 保存当页变量
        self.save_variables(ps)
        return result
    
    def export_variables(self,parser:Parser):
        result = SindexerResult(self.__typename__)
        if self.__exportvars__:
            for item in self.__exportvars__:
                if self.__typename__ in parser.funcer.variables.keys():
                    values:dict = parser.funcer.variables.get(self.__typename__)
                    if item in values.keys():
                        val = values.get(item)
                        # 如果值是公式解析器的返回值类型，直接拿值即可
                        if isinstance(val,SindexerResult):
                            # 直接把所有属性搬出来
                            for (k,v) in vars(val).items():
                                if k!="name":
                                    setattr(result,k,v)
                            continue
                        setattr(result,item,val)
        return result
    
    def save_variables(self,parser:Parser):
        for group in parser.funcer.variables:
            values = None
            if isinstance(group,str):
                values = parser.funcer.variables.get(group)
            if isinstance(group,dict):
                values = group
            if values:
                for (k,v) in values.items():
                    self.save_temp(k,v)


    # 如果需要系统支持自定义的公式，要手动实现call方法
    def call(self):
        pass

    @property
    def OPEN(self):
        if self.klines:return self.klines[self.cursor.index].OPEN
    @property
    def HIGH(self):
        if self.klines:return self.klines[self.cursor.index].HIGH
    @property
    def LOW(self):
        if self.klines:return self.klines[self.cursor.index].LOW
    @property
    def CLOSE(self):
        if self.klines:return self.klines[self.cursor.index].CLOSE
    @property
    def VOL(self):
        if self.klines:return self.klines[self.cursor.index].VOL
    @property
    def AMOUNT(self):
        if self.klines:return self.klines[self.cursor.index].AMOUNT
    @property
    def DATE(self):
        if self.klines:return self.klines[self.cursor.index].DATE
    
    def GET(self,X,index:int=None):
        if index==None:index=self.cursor.index
        # 首先查找X是否是一个变量
        if hasattr(self,X) and index==self.cursor.index:return getattr(self,X)
        if self.klines:
            if hasattr(self.klines[index],X):
                return getattr(self.klines[index],X)
        
        # 去函数库命名空间找
        funcer = Functioner()
        result = funcer.get_value(self.namespace,X)
        if result!=None:
            return result
        # 去注册函数库找
        for item in funcer.function_exs:
            if hasattr(item,X):
                return getattr(item,X)
            
        rs = self.get_temp(X,index)
        if rs!=None:return rs
            
        raise SindexerVarNotFoundError("找不到变量值 %s" % X)
    
    def REF(self,X:str,N:int=1):
        """向前引用
        """
        i = self.cursor.index - N
        if i>=0: 
            item = self.klines[i]
            if hasattr(item,X):
                return getattr(item,X)
            # 找不到就拿临时数据
            return self.get_temp(X,i)

    def LLV(self,X:str,N:int=1):
        """周期内最小值

        Args:
            X (str): 搜索的字段
            N (int, optional): _description_. Defaults to 1.
        """
        result = self.GET(X)
        index = self.cursor.index
        for i in range(N):
            index = self.cursor.index - i
            if index>=0:
                result = min(result,self.GET(X,index))
            else:
                break
        return result
    
    def HHV(self,X:str,N:int=1):
        """周期内最大值

        Args:
            X (str): 搜索的字段
            N (int, optional): _description_. Defaults to 1.
        """
        result = self.GET(X)
        index = self.cursor.index
        for i in range(N):
            index = self.cursor.index - i
            if index>=0:
                result = max(result,self.GET(X,index))
            else:
                break
        return result

        
    


