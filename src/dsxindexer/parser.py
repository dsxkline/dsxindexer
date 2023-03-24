"""
语法解析器
主体框架由ChatGPT生成，dsxquant进行了封装扩展，感谢ChatCPT教会我写了一个解析器 ^_^

Created on Tue Nov 15 16:00:04 2022

@author: dsxquant
@email: 934476300@qq.com
@website: www.dsxquant.com
"""
from dsxindexer.operators.andor_operator import AndOrOperator
from dsxindexer.operators.muldiv_operator import MulDivOperator
from dsxindexer.operators.plusminus_operator import PlusMinusOperator
from dsxindexer.processors.operator_processor import OperatorProcessor
from dsxindexer.tokenizer import ExpreItemDirection
from dsxindexer.functioner import Functioner
from dsxindexer.tokenizer import Lexer,TokenType
from dsxindexer.processors.factor_processor import FactorProcessor

class Parser:
    def __init__(self, lexer:Lexer,funcer:Functioner=Functioner(),namespace:str=None,cache_tokens:list=None,func_name:str=None):
        # 已解析词法TOKEN,用于已编译解析,避免重复扫描词法
        self.cache_tokens = cache_tokens
        # 当前游标
        self.cursor = 0
        # 传入词法解析器，把表达式转换为Token集合
        self.lexer = lexer
        # 这里相当于取得第一个词法解析器的Token
        self.current_token = self.get_next_token()
        # 上一个变量名,解析等于号的时候需要把右边的值赋值给左边的变量
        self.last_avariable = None
        # 函数源，里面可以自由定义语法支持的函数集
        self.funcer = funcer
        # 项处理器，主要处理操作符、函数等
        self.operator_processor= OperatorProcessor()
        # 因子处理器，主要处理数据类型等
        self.factor_processor = FactorProcessor()
        # 最终返回结果
        self.result = None
        # 变量的命名空间，整个输入流会分配一个命名空间
        self.namespace = namespace
        # 函数内部，解析函数内部的时候命名空间需要开辟函数内部空间
        self.func_name = func_name
        # TOKEN树,可以保存解析语句
        self.token_tree = [self.current_token]
        # 需要导出变量的变量名，在公式中用单个冒号赋值就是需要导出的变量
        self.export = []

    def parse(self):
        self.result = self.expr()
        # 整个表达式计算完后清理变量缓存
        # self.funcer.clear_variables()
        return self

    # 表达式字符串 递归开始
    def expr(self):
        # 处理项开始
        result = self.term()
        result = AndOrOperator(self.current_token,self,result).call()
        # 最后处理加减
        result = PlusMinusOperator(self.current_token,self,result).call()
        return result

    # 处理表达式项，就是表达式里面操作符函数等，意思是一个表达式有多少个操作项组合而成，分别处理这些项
    def term(self):
        # 处理因子，如果是最小因子了，无法分解了，就返回结果
        result = self.factor()
        # 项处理器 处理操作符函数等
        result = self.operator_processor.call(self.current_token,self,result)
        return result

    # 处理因子
    def factor(self):
        token = self.current_token
        # 这里需要处理每一个表达式因子，就是表达式里面的最小单位，例如 变量，数值，字符串，函数等数据类型
        # 因子处理器
        return self.factor_processor.call(token,self)

    # 继续下一个
    def eat(self, token_type):
        if self.current_token.type == token_type:
            self.current_token = self.get_next_token()
            self.token_tree.append(self.current_token)
        else:
            raise Exception('Syntax error')
    
    def get_next_token(self):
        if self.cache_tokens:
            result = self.cache_tokens[self.cursor]
            self.cursor += 1
            return result
        else:
            return self.lexer.get_next_token()
    


