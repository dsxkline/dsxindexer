from dsxindexer.configer import TokenType,ExpreItemDirection
from dsxindexer.tokenizer import Token
from dsxindexer.factors.base_factor import BaseFactor


class NewlineFactor(BaseFactor):
    # 设置处理标识类型
    type_name = TokenType.NEWLINE

    def call(self):
        # 处理换行符
        self.parser.eat(self.type_name)
        # 换行符表示新开始一条表达式
        result = self.parser.expr()
        return result
        