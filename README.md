# dsxindexer
 量化指标公式编辑器框架

## 使用方法
```python
class ABCD(BaseSindexer):
    """ABCD
    自定义ABCD指标
    """
    # 定义指标名称
    __typename__ = "ABCD"
    # 定义指标导出的变量名
    __exportvars__ = ("A","B","C")

    def formula(self):
        return """
        A:=CLOSE;
        B:=HIGH;
        C:=A*B;
        """
        
if __name__=="__main__":
    try:
        # 获取K线历史数据
        klines = dsxquant.get_klines("000001",dsxquant.market.SZ).datas()
        klines:list = klines.data
        klines.reverse()
        # 指标处理器
        sp = SindexerProcessor(klines)
        # 注册添加一些自定义指标
        sp.register(MACD)
        sp.register(KDJ)
        sp.register(ABCD)
        # 执行计算结果
        result = sp.execute()
        # 取最后一个
        model = result[-1]
        # 标准值 K:70.5 D:60.62 J:90.26
        print(model.DATE,vars(model.MACD))
        print(model.DATE,vars(model.KDJ))
        print(model.DATE,vars(model.ABCD))
    except Exception as e:
        traceback.print_exc()
```