
import hashlib
import inspect
import math
import re
import sys
from typing import List

from dsxindexer.configer import Cursor,DSX_FIELD_STR,SindexerVarNotFoundError,RegRolues,logger

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
        # 函数库
        self.functioner = None
        # 命名空间
        self.namespace = None
        # 保存每个公式的TOKEN_TREE
        self.token_tree = {}
    
    def set_functioner(self,functioner:Functioner):
        if functioner:
            self.functioner = functioner
            self.functioner.register(self)

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
                # 函数内部空间不能跟命名空间相同
                if func_name != None and func_name!=self.namespace:
                    if func_name in obj.keys():
                        obj = obj.get(func_name)

            if not isinstance(obj,dict):
                return obj

            if name in list(obj.keys()):
                result = obj.get(name)
                if isinstance(result,SindexerResult):
                    if hasattr(result,name):
                        result = getattr(result,name)
                return result 
                

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
        parser = Parser(lexer,namespace=self.namespace,funcer=self.functioner,cache_tokens=self.get_token_tree(),func_name=func_name)
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
                        if self.__exportvars__.__len__()==1: 
                            return val
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
            if values!=None:
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
        if isinstance(index,float):index = int(index)
        # 首先查找X是否是一个变量
        if hasattr(self,X) and index==self.cursor.index:
            result = getattr(self,X)
            return getattr(self,X)
        if self.klines:
            if hasattr(self.klines[index],X):
                result = getattr(self.klines[index],X)
                if isinstance(result,SindexerResult):
                    # 解决变量名与命名空间冲突问题
                    if hasattr(result,X):
                        return getattr(result,X)
                else:
                    return result
        
        rs = self.get_temp(X,index,self.__typename__)
        if rs!=None:return rs
        if index==self.cursor.index:
            # 去函数库命名空间找
            funcer = self.functioner
            result = funcer.get_value(self.namespace,X,self.__typename__)
            if result!=None:
                return result
            # 去注册函数库找
            for item in funcer.function_exs:
                if hasattr(item,X):
                    return getattr(item,X)
        return None
        # raise SindexerVarNotFoundError("找不到变量值 %s" % (X))

    staticmethod
    def reg_modules(module):
        logger.debug("正则注册函数模块: %s " % module.__name__)
        # 获取模块中的所有函数
        functions = inspect.getmembers(sys.modules[module.__name__], inspect.isfunction)
        # 将所有函数注册到类中
        for function in functions:
            setattr(BaseSindexer, function[0], function[1])
        # 属性方法
        # 获取模块中的属性方法并注册到类中
        for attr_name in dir(module):
            attr = getattr(module, attr_name)
            if isinstance(attr, property):
                # 得到属性的get方法
                setattr(BaseSindexer, attr_name, property(attr.fget))
                if attr.fset:
                    setattr(BaseSindexer, attr_name, attr.fset)

 
# 导入常用函数
import dsxindexer.sindexer.base.cons_funcs as cons_funcs
BaseSindexer.reg_modules(cons_funcs)
# 导入逻辑函数
import dsxindexer.sindexer.base.logical_funcs as logical_funcs
BaseSindexer.reg_modules(logical_funcs)
# 导入行情函数
import dsxindexer.sindexer.base.price_funcs as price_funcs
BaseSindexer.reg_modules(price_funcs)
# 导入数学和统计函数
import dsxindexer.sindexer.base.math_funcs as math_funcs
BaseSindexer.reg_modules(math_funcs)
# 导入大盘函数
import dsxindexer.sindexer.base.large_funcs as large_funcs
BaseSindexer.reg_modules(large_funcs)
# 导入引用函数
import dsxindexer.sindexer.base.refer_funcs as refer_funcs
BaseSindexer.reg_modules(refer_funcs)
# 导入指标函数
import dsxindexer.sindexer.base.index_funcs as index_funcs
BaseSindexer.reg_modules(index_funcs)
        
    



