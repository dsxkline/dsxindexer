from dsxindexer.processors.base_processor import BaseProcessor
from dsxindexer.configer import TokenType,ExpreItemDirection
from dsxindexer.tokenizer import Token
from dsxindexer.factors.base_factor import BaseFactor


class VariableFactor(BaseFactor):
    # 设置处理标识类型
    type_name = TokenType.VARIABLE

    def call(self):

        # 处理变量命名
        self.parser.eat(self.type_name)
        if self.token.direction==ExpreItemDirection.LEFT:
            self.parser.last_avariable = str(self.token.value)
            return str(self.token.value)
        else:
            # 通过方法名获取方法对象
            result = self.parser.funcer.get_value(self.parser.namespace,self.token.value)
            if result==None:
                # 如果找不到，去函数扩展库找
                for c in self.parser.funcer.function_exs:
                    obj = c
                    # 检查对象是否已实例化
                    if type(obj)==type: obj = c() 
                    # 否则直接查找类的方法
                    if hasattr(obj,self.token.value):
                        result = getattr(obj,self.token.value)
                        break
                        
                    del obj
            print("获取变量值 %s=%s" % (self.token.value,result))
            return result
        