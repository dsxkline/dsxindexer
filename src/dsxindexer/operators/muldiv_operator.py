from dsxindexer.configer import TokenType
from dsxindexer.tokenizer import Token
from dsxindexer.operators.base_operator import BaseOperator,OperatorNotNumberError

class MulDivOperator(BaseOperator):
    # 设置处理标识类型
    type_name = (TokenType.MUL,TokenType.DIV)

    def call(self):
        result = self.last_result
        while self.parser.current_token.type in (TokenType.MUL,TokenType.DIV):
            op = self.parser.current_token
            self.parser.eat(op.type)
            # 解析乘号的右边表达式
            factor = self.parser.factor()
            if not isinstance(factor,int) and not isinstance(factor,float):
                raise OperatorNotNumberError("乘因子格式错误,非数字 %s=%s" % (op,factor))
            if not isinstance(result,int) and not isinstance(result,float):
                raise OperatorNotNumberError("乘因子格式错误,非数字 %s=%s" % (op,result))
            if op.type==TokenType.MUL:
                result = result * factor
                print("处理相乘：%s * %s = %s"%(self.last_result,factor,result))
            if op.type==TokenType.DIV:
                result = result / factor
                print("处理相除：%s / %s = %s"%(self.last_result,factor,result))
            
        return result
