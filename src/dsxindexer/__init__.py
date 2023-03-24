from dsxindexer.processors.sindexer_processor import SindexerProcessor as sindexer
from dsxindexer.configer import logger
from dsxindexer.sindexer.base_sindexer import BaseSindexer
from dsxindexer.sindexer.sindexer_factory import SindexerFactory as factory
from dsxindexer.sindexer.models.kline_model import KlineModel
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