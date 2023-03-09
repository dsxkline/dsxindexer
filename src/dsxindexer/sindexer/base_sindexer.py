
import hashlib
import re
from typing import List

from dsxindexer.configer import Cursor,DSX_FIELD_STR,SindexerVarNotFoundError,RegRolues

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
        # 保存每个公式的TOKEN_TREE
        self.token_tree = {}

    def formula(self):
        pass
    
    def compiled(self):
        """已编译
        注册的指标公式我们定义为一个已编译函数
        函数的地址我们用公式代码的MD5值
        函数的参数
        函数的逻辑
        """
        pass
    
    def save_temp(self,name,val,func_name=None):
        """这里保存是每一页都保存起来，类似 REF 这种函数就要查找历史数据

        Args:
            name (_type_): 变量名
            val (_type_): 变量值
            func_name (str): 函数内部
        """
        obj = {}
        if self.cursor.index<self.temp.__len__():
            obj = self.temp[self.cursor.index]
        else:
            self.temp.append(obj)
        if self.namespace not in obj.keys():
            # 初始化命名空间
            obj[self.namespace] = {}
        if func_name!=None:
            if func_name not in obj[self.namespace].keys():
                # 初始化内部空间
                obj[self.namespace][func_name] = {}
            obj[self.namespace][func_name][name]=val
        else:
            obj[self.namespace][name]=val
        self.temp[self.cursor.index] = obj
    
    def get_temp(self,name,index,func_name=None):
        if index<self.temp.__len__():
            obj:dict = self.temp[index]
            if self.namespace in obj.keys():
                obj = obj.get(self.namespace)
                if func_name != None:
                    if func_name in obj.keys():
                        obj = obj.get(func_name)
                        
            if name in list(obj.keys()):
                    return obj.get(name)  
                

    def execute(self):
        f = self.formula()
        if f:
            # 命名空间初始化为公式主名称，递归会继承
            self.namespace = self.__typename__
            result = self.parser(f)
            return result

    def parser(self,expresions,func_name:str=None):
        # 词法分析器,表达式分词并标记类型
        lexer = Lexer(expresions)
        # 语法解析器，执行操作符，函数等功能
        parser = Parser(lexer,namespace=self.namespace,cache_tokens=self.get_token_tree(),func_name=func_name)
        # 解析并返回结果
        ps = parser.parse()
        # 导出变量
        result = self.export_variables(ps)
        # 保存当页变量
        self.save_variables(ps)
        # 保存TOKEN_TREE
        self.save_token_tree(ps)
        return result
    
    def export_variables(self,parser:Parser):
        result = SindexerResult(self.__typename__)
        if parser.export.__len__()>0:
            # 公式中单独一个冒号表示赋值并导出变量，表明公式中已指定导出变量名,公式中的优先
            self.__exportvars__ = list(set(parser.export + list(self.__exportvars__ and self.__exportvars__ or [])))

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
                        # 单个变量导出直接导出数值格式
                        if self.__exportvars__.__len__()==1: return val
                        setattr(result,item,val)
        else:
            # 如果没有设置导出变量，默认取最后一个变量的值
            if parser.last_avariable:
                return parser.funcer.get_value(self.namespace,parser.last_avariable,parser.func_name)
            else:
                return parser.result
        return result
    
    # 保存解析返回的变量值
    def save_variables(self,parser:Parser):
        for namespace in parser.funcer.variables:
            values = None
            if isinstance(namespace,str):
                values = parser.funcer.variables.get(namespace)
            if isinstance(namespace,dict):
                values = namespace
            if values:
                for (k,v) in values.items():
                    self.save_temp(k,v,parser.func_name)

    def save_token_tree(self,parser:Parser):
        fstr = self.formula()
        if fstr:
            fid = self.md5(self.formula())
            token_tree = parser.token_tree
            self.token_tree[fid] = token_tree

    def get_token_tree(self):
        fstr = self.formula()
        if fstr:
            fid = self.md5(self.formula())
            if fid in self.token_tree:
                return self.token_tree.get(fid)

    def md5(self,text):
        md5 = hashlib.md5()
        md5.update(text.encode("utf-8"))
        return md5.hexdigest()

    # 如果需要系统支持自定义的公式，要手动实现call方法
    def call(self):
        pass

    def GET(self,X,index:int=None):
        if index==None:index=self.cursor.index
        # 如果X不是一个字段名字符串，是一个数值，就直接返回数值
        if not isinstance(X,str):return X
        # 首先查找X是否是一个变量
        if hasattr(self,X) and index==self.cursor.index:return getattr(self,X)
        if self.klines:
            if hasattr(self.klines[index],X):
                return getattr(self.klines[index],X)
        
        # 去函数库命名空间找
        funcer = Functioner()
        result = funcer.get_value(self.namespace,X,self.__typename__)
        if result!=None:
            return result
        # 去注册函数库找
        for item in funcer.function_exs:
            if hasattr(item,X):
                return getattr(item,X)
            
        rs = self.get_temp(X,index,self.__typename__)
        if rs!=None:return rs
            
        raise SindexerVarNotFoundError("找不到变量值 %s" % (X))

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
    
    def REF(self,X:DSX_FIELD_STR,N:int=1):
        """向前引用，向前引用必须跟公式MD5命名空间一致，否则多个调用之间会产生命名冲突
        """
        i = self.cursor.index - N
        if i<0:i=0
        if i>=0: 
            item = self.klines[i]
            if hasattr(item,X):
                return getattr(item,X)
            # 找不到就拿临时数据
            return self.get_temp(X,i,self.__typename__)

    def LLV(self,X:DSX_FIELD_STR,N:int=1):
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
    
    def HHV(self,X:DSX_FIELD_STR,N:int=1):
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
    
    def AVEDEV(self,X:DSX_FIELD_STR,N:int=1):
        """计算数据与数据集均值之间的偏差大小的平均值。

        Args:
            X (DSX_FIELD_STR): 变量名或表达式
            N (int, optional): _description_. Defaults to 1.
        """
        XX = self.GET(X)
        # 统计数据集均值
        result = XX
        index = self.cursor.index
        for i in range(N):
            index = self.cursor.index - i
            if index>=0:
                # 计算数据集总和
                result += self.GET(X,index)
            else:
                break
        # 计算与数据集均值
        avgs = result / N
        # 计算数据与数据集均值之间的偏差
        result = XX - avgs
        return result


        
    



