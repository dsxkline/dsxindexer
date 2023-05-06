import copy
import hashlib
import inspect
import json
import os
import re
from dsxindexer.processors.base_processor import BaseProcessor
from dsxindexer.configer import DSX_FIELD_STR, DsxindexerMethodParamMisError, TokenType,ExpreItemDirection,DsxindexerMethodNotFoundError,logger,ASSIGN_CHART
from dsxindexer.tokenizer import Token
from dsxindexer.factors.base_factor import BaseFactor
from dsxindexer.configer import RegRolues,CACHE_PATH
from dsxindexer.functioner import Functioner

class FunctionFactor(BaseFactor):
    # 设置处理标识类型
    type_name = TokenType.FUNCTION
    # 缓存文件
    cache_content = None

    def call(self):
        # 处理函数
        self.parser.eat(self.type_name)
        # 解析函数并返回值
        result = self.parser_func(self.token.value)
        # 解析完函数后，需要继续，有些函数没有返回值会返回 None，需要特殊处理
        if result==None: return self.parser.factor()
        return result
    
    def parser_func(self,expre):
        # 启用解析缓存
        result = self.get_cache_parse(expre)
        if result: return result
        funcs = self.parse_function(expre)
        if funcs:
            func_name = funcs[0]
            func_args = funcs[1]
            # 通过方法名获取方法对象
            method = None
            # 应该优先从命名空间找
            for c in self.parser.funcer.function_exs:
                obj = c
                # 检查对象是否已实例化
                if type(obj)==type: obj = c()
                # 否则直接查找类的方法
                if hasattr(obj,"namespace"):
                    if getattr(obj,"namespace") == self.parser.namespace:
                        # 命名空间继承，命名空间继承后，变量也会继承
                        if hasattr(obj,func_name):
                            mt = getattr(obj, func_name)
                            if callable(mt):
                                # 把变量名继承下来，用于更新前值
                                setattr(obj,"variable_name",self.parser.last_avariable)
                                method = mt
                                break
                del obj
            if not method:
                # 在自己命名空间类中都找不到方法，意味着方法可能在其他类中，例如自定义的指标MACD，可能在MACD类中，那就要去MACD类去查找
                for c in self.parser.funcer.function_exs:
                    obj = c
                    # 检查对象是否已实例化
                    if type(obj)==type: obj = c()
                    # 查找类的方法，这里意思是调用其他指标类实例对象
                    if type(obj).__name__ == func_name:
                        # 命名空间继承，命名空间继承后，变量也会继承
                        setattr(obj,"namespace",self.parser.namespace)
                        setattr(obj,"variable_name",self.parser.last_avariable)
                        method = getattr(obj,"call")
                        break
                    # 或者直接查找
                    if hasattr(obj,func_name):
                        mt = getattr(obj, func_name)
                        if callable(mt):
                            setattr(obj,"variable_name",self.parser.last_avariable)
                            method = mt
                            break
                    del obj
            if method==None:
                # 函数库寻找可调用方法
                methods = [method_name for method_name in dir(self.parser.funcer) if callable(getattr(self.parser.funcer, method_name)) and not method_name.startswith('__')]
                if func_name in methods:
                    method = getattr(self.parser.funcer,func_name)
            if method==None:
                raise DsxindexerMethodNotFoundError("不支持的函数名: %s，TOKEN:%s" % (func_name,self.token.throw_error()))
            
            # 这里我们约定函数第一个为变量名，所以声明的函数需要规定第一个上变量字符串名次，函数内部需要通过这个变量名称获取变量值
            args = []
            # 得到函数参数类型,如果参数类型是需要传变量名称，则传变量名称
            parameters = list(inspect.signature(method).parameters.values())
            if parameters.__len__()!=func_args.__len__():
                raise DsxindexerMethodParamMisError("方法 %s(%s) 参数数量不一致 %s,TOKEN:%s" % (func_name,parameters,func_args,self.token.throw_error()))
            i = 0
            for item in func_args:
                typename = parameters[i].annotation
                if typename==DSX_FIELD_STR:
                    # 如果参数是一个表达式，我们需要自动构建一个变量给这个表达式，方便在未来某个时刻提取出来，也方便储存其历史记录
                    if not re.match(RegRolues.VARIABLE,item):
                        # 用其MD5值构建变量名,有可能同名，所以取得他们的位置信息
                        var_temp = "var_temp_"+self.md5(item)+"_"+str(i)
                        # 构建临时表达式
                        expr_tem = var_temp+ASSIGN_CHART+item+";"
                        # 解析
                        self.parser_func_args(expr_tem,self.parser.namespace)
                        item = var_temp
                    args.append(item)
                        
                else:
                    args.append(self.parser_func_args(item,self.parser.namespace))
                i +=1
            # 调用方法
            result = method(*args)
            logger.debug("正则处理函数:%s(%s)=%s"%(func_name,args,result))
            self.save_cache_parse(expre,result)
            return result
        
    def md5(self,text):
        md5 = hashlib.md5()
        md5.update(text.encode("utf-8"))
        return md5.hexdigest()
    
    def parser_func_args(self,expre,namespace):
        """解析函数参数"""
        from dsxindexer.tokenizer import Lexer
        from dsxindexer.parser import Parser
        # 词法分析器
        lexer = Lexer(expre,ExpreItemDirection.RIGHT,self.token.location[0])
        # 语法解析器
        parser = Parser(lexer,self.parser.funcer,namespace)
        # 解析并返回结果
        ps = parser.parse()
        return ps.result
        
    def parse_function(self,text):
        s = text
        # 解析函数名
        function_name = s.split('(')[0]
        # 解析参数列表
        param_string = s[len(function_name)+1:-1]  # 获取括号内的参数字符串
        params = []
        current_param = ''
        open_brackets = 0
        for c in param_string:
            if c == '(':
                current_param += c
                open_brackets += 1
            elif c == ')':
                current_param += c
                open_brackets -= 1
            elif c == ',' and open_brackets == 0:
                params.append(current_param.strip())
                current_param = ''
            else:
                current_param += c
        params.append(current_param.strip())
        return (function_name,params)
    
    def get_cache_filename(self,expre):
        funcer:Functioner = self.parser.funcer
        symbol = funcer.symbol
        market = funcer.market
        cursor = funcer.cursor
        klines = funcer.klines
        if not symbol or market==None or not cursor or not klines : return (None,None)
        date = str(cursor.index)
        if cursor.index<klines.__len__():
            item = klines[cursor.index]
            date = item.DATE
        key = "%s_%s_%s_%s_%s" % (symbol,market,cursor.index,date,expre)
        # key = funcer.MD5(key)
        path = CACHE_PATH+"/funcer/"+str(market)+"-"+symbol+"/"
        if not os.path.exists(path):
            os.makedirs(path)
        filename = path+"func.txt"
        return (filename,key)
    
    def get_cache_parse(self,expre):
        """从缓存读取解析值
        """
        if not self.parser.funcer.enable_cache:return
        filename,key = self.get_cache_filename(expre)
        if not filename:return
        result = FunctionFactor.cache_content
        if result==None:
            if os.path.exists(filename):
                with open(filename) as f:
                    result = f.read()
                    if result:
                        result:dict = json.loads(result)
                        FunctionFactor.cache_content = result
        if isinstance(result,dict):
            result = result.get(key)
            return result
                
    def save_cache_parse(self,expre,result):
        """把函数解析结果保存到缓存
        """
        if not self.parser.funcer.enable_cache:return
        filename,key = self.get_cache_filename(expre)
        if not filename:return
        content = FunctionFactor.cache_content
        if not content:
            content = {}
        if result!=None and isinstance(content,dict):
            content[key] = result
            FunctionFactor.cache_content = content
            if self.parser.funcer.cursor.index>=self.parser.funcer.cursor.count-1:
                with open(filename,"w") as f:
                    result = json.dumps(FunctionFactor.cache_content)
                    f.write(result)
        
            
        