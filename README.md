# dsxindexer
 基于麦语言的量化指标公式编辑器框架,目前支持部分通达信公式，因为公式太多，所以慢慢完善中，有兴趣的朋友可以自己实现哦。

## 安装

```
pip install dsxindexer
```

## 使用

```python
# 导入包
import dsxindexer
# 导入数据工具箱
import dsxquant
# 首先获取K线历史数据
klines = dsxquant.get_klines("000001",dsxquant.market.SZ).datas()
klines:list = klines.data
klines.reverse()
# 创建指标处理器
sp = dsxindexer.sindexer(klines)
# 注册系统指标
sp.register(dsxindexer.INDEXER.MACD)
# 执行计算结果
result = sp.execute()
```

## 自定义指标公式


```python
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

# 获取K线历史数据
klines = dsxquant.get_klines("000001",dsxquant.market.SZ).datas()
klines:list = klines.data
klines.reverse()
dsxindexer.logger.info("开始处理....")
# 指标处理器
sp = dsxindexer.sindexer(klines)
# 注册自定义指标
sp.register(ABCD)
# 执行计算结果
result = sp.execute()
# 取最后一个
model = result[-1]
dsxindexer.logger.info(model.DATE+" %s" % vars(model.ABCD))

```

## 指标编写方式

目前指标支持系统指标，自定义指标，自定义可分为两种方式：继承和工厂方式

### 继承方式

```python
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
# 指标处理器
sp = dsxindexer.sindexer(klines)
sp.register(MAn)
# 执行计算结果
result = sp.execute()
```

### 工厂方式

```python
# 指标处理器
sp = dsxindexer.sindexer(klines)
# 通过指标工厂自定义指标
MA10 = dsxindexer.factory.create("MA10","MA10:MA(CLOSE,10);")
sp.register(MA10)
# 执行计算结果
result = sp.execute()
```

## 使用系统指标

目前支持大概几十个系统指标，后续不断完善中....


### 常用系统指标
```python
# 系统默认指标
class INDEXER:
    BOLL="BOLL"
    BRAR="BRAR"
    CCI="CCI"
    CDP="CDP"
    CR="CR"
    DMA="DMA"
    EMV="EMV"
    EXPMA="EXPMA"
    KDJ="KDJ"
    MACD="MACD"
    MIKE="MIKE"
    OBV="OBV"
    PSY="PSY"
    ROC="ROC"
    RSI="RSI"
    TRIX="TRIX"
    VR="VR"
    WR="WR"
    WVAD="WVAD"
```

