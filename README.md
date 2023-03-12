# dsxindexer
 量化指标公式编辑器框架

## 使用方法
```python

import dsxquant

class ABCD(BaseSindexer):
    """ABCD
    通过继承指标器基类自定义ABCD指标
    """
    # 定义指标名称
    __typename__ = "ABCD"
    # 定义导出的变量名
    # __exportvars__ = ("A","B","C","D")

    def formula(self):
        return """
        # 这里是注释
        A:CLOSE;#收盘价
        B:HIGH;#最高价
        C:A*B;
        {这里是注释符了}
        D:1000+(A+B*90/(60*C))/90*A-100000/C*100;
        E:IF(A>=B,
        IFF(B>C,D,A),C);
        买线:1000;
        卖线:456 * 买线;
        哈哈:!90;
        """

class MAn(BaseSindexer):
    """MAn
    """
    # 定义指标名称
    __typename__ = "MAn"

    def formula(self):
        return """
        MA5:MA(CLOSE,5);
        MA30:MA(CLOSE,30);
        MA60:MA(CLOSE,60);
        """
        
if __name__=="__main__":
    try:
        logger.setLevel(logging.INFO)
        # 获取K线历史数据
        klines = dsxquant.get_klines("000001",dsxquant.market.SZ).datas()
        klines:list = klines.data
        klines.reverse()
        logger.info("开始处理....")
        # 指标处理器
        sp = SindexerProcessor(klines)
        # 自定义继承类注册
        # sp.register(MACD)
        # sp.register(KDJ)
        # sp.register(ABCD)
        # sp.register(RSI)
        # sp.register(CCI)
        # sp.register(WR)
        # sp.register(DMI)
        # sp.register(BOLL)
        # sp.register(TRIX)
        # sp.register(OBV)
        # sp.register(PSY)
        # sp.register(BRAR)
        sp.register(ROC)
        # sp.register(MAn)
        # 通过指标工厂自定义指标
        MA10 = SindexerFactory.create("MA10","MA10:MA(CLOSE,10);",functioner=sp.functioner)
        # sp.register(MA10)
        # MA30 = SindexerFactory.create("MA30","MA10:MA(CLOSE,30);",functioner=sp.functioner)
        # sp.register(MA30)
        # MA60 = SindexerFactory.create("MA60","MA10:MA(CLOSE,60);",functioner=sp.functioner)
        # sp.register(MA60)
        # 执行计算结果
        result = sp.execute()
        # 取最后一个
        model = result[-1]
        # 标准值 K:70.5 D:60.62 J:90.26
        # logger.info(model.DATE+" %s" % vars(model.MACD))
        # logger.info(model.DATE+" %s" % vars(model.KDJ))
        # logger.info(model.DATE+" %s" % vars(model.ABCD))
        # logger.info(model.DATE+" %s" % vars(model.RSI))
        # logger.info(model.DATE+" %s" % model.CCI)
        # logger.info(model.DATE+" %s" % vars(model.WR))
        # logger.info(model.DATE+" %s" % vars(model.DMI))
        # logger.info(model.DATE+" %s" % vars(model.BOLL))
        # logger.info(model.DATE+" %s" % vars(model.TRIX))
        # logger.info(model.DATE+" %s" % vars(model.OBV))
        # logger.info(model.DATE+" %s" % vars(model.PSY))
        # logger.info(model.DATE+" %s" % vars(model.BRAR))
        logger.info(model.DATE+" %s" % vars(model.ROC))
        # logger.info(model.DATE+" %s" % vars(model.MAn))
        # logger.info(model.DATE+" %s" % model.MA10)
        # logger.info(model.DATE+" %s" % model.MA30)
        # logger.info(model.DATE+" %s" % model.MA60)
 
    except Exception as e:
        logger.error(e)
        traceback.print_exc()
        
```