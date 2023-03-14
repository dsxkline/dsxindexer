import traceback
import dsxindexer
import dsxquant

class ABCD(dsxindexer.BaseSindexer):
    """ABCD
    通过继承指标器基类自定义ABCD指标
    """
    # 定义指标名称
    __typename__ = "ABCD"

    def formula(self):
        return """
        long:MACD.LONG;
        金叉:CROSS(MACD.DIF,MACD.DEA);
        死叉:LONGCROSS(MACD.DIF,MACD.DEA,5) AND MACD.DIF<-0.1 ;
        Kjd:"KDJ.K";
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

class MAn(dsxindexer.BaseSindexer):
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
        # logger.setLevel(logging.INFO)
        # 获取K线历史数据
        klines = dsxquant.get_klines("000001",dsxquant.market.SZ).datas()
        klines:list = klines.data
        klines.reverse()
        dsxindexer.logger.info("开始处理....")
        # 指标处理器
        sp = dsxindexer.sindexer(klines)
        # 注册自定义指标
        sp.register(ABCD)
        # 注册系统指标
        sp.register(dsxindexer.INDEXER.WVAD)
        sp.register(MAn)
        # 通过指标工厂自定义指标
        MA10 = dsxindexer.factory.create("MA10","MA10:MA(CLOSE,10);")
        sp.register(MA10)
        # 执行计算结果
        result = sp.execute()
        # 取最后一个
        model = result[-1]
        dsxindexer.logger.info(model.DATE+" %s" % vars(model.ABCD))
        dsxindexer.logger.info(model.DATE+" %s" % vars(model.WVAD))
    except Exception as e:
        dsxindexer.logger.error(e)
        traceback.print_exc()