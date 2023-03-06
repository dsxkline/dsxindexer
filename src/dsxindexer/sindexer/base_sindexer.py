
from typing import List

from dsxindexer.configer import Cursor

from dsxindexer.functioner import Functioner

from dsxindexer.parser import Parser

from dsxindexer.tokenizer import Lexer
from dsxindexer.sindexer.fomulas import Formulas
from dsxindexer.sindexer.models.kline_model import KlineModel

class SindexerResult:
    def __init__(self,name:str) -> None:
        self.name:str = name

class BaseSindexer:
    # 继承子类需要重写此字段
    __typename__:str = None
    # 需要从公式的计算结果导出的变量名称
    __exportvars__:tuple = None
    def __init__(self,klines:List[KlineModel],cursor:Cursor) -> None:
        # k线数据
        self.klines:List[KlineModel] = klines
        # 当前索引
        self.cursor:Cursor = cursor
        # 临时数据
        self.temp = []
        pass

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
            result = self.parser(f)
            return result

    def parser(self,expresions):
        # 词法分析器,表达式分词并标记类型
        lexer = Lexer(expresions)
        # 语法解析器，执行操作符，函数等功能
        parser = Parser(lexer)
        # 解析并返回结果
        ps = parser.parse()
        result = SindexerResult(self.__typename__)
        if self.__exportvars__:
            for item in self.__exportvars__:
                if hasattr(ps.funcer,item):
                    val = getattr(ps.funcer,item)
                    # 如果值是公式解析器的返回值类型，直接拿值即可
                    if isinstance(val,SindexerResult):
                        # 直接把所有属性搬出来
                        for (k,v) in vars(val).items():
                            if k!="name":
                                setattr(result,k,v)
                        continue
                    setattr(result,item,val)
        return result

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
        
    



