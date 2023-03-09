from concurrent.futures import ThreadPoolExecutor,wait,as_completed
import datetime
import time

from dsxindexer.configer import Cursor,logger
from dsxindexer.sindexer.MA import MA

from dsxindexer.sindexer.fomulas import Formulas
from dsxindexer.sindexer.models.kline_model import KlineModel
from dsxindexer.parser import Parser
from dsxindexer.sindexer.SMA import SMA
from dsxindexer.tokenizer import Lexer
from dsxindexer.functioner import Functioner
from dsxindexer.processors.base_processor import BaseProcessor
from dsxindexer.sindexer.EMA import EMA
from dsxindexer.sindexer.base_sindexer import BaseSindexer
from typing import List

class SindexerProcessor(BaseProcessor):

    # 内置一些底层函数
    processors:List[BaseSindexer] = [
        EMA,
        SMA,
        MA,
    ]

    def __init__(self,klines:list=None) -> None:
        # k线数据
        self.klines:List[KlineModel] = self.cover_to_model(klines)
        # 当前游标
        self.cursor = Cursor()
        pass
    
    def cover_to_model(self,klines:list):
        newklines = []
        if klines:
            for item in klines:
                d,o,h,l,c,v,a = type(item)==list and item or item.split(",")
                date = self.get_date(d)
                m = KlineModel()
                m.DATE = d
                m.TIME = date.strftime("%H%M")
                m.YEAR = date.year
                m.MONTH = date.month
                m.DAY = date.day
                m.WEEK = date.weekday()
                m.HOUR = date.hour
                m.MINUTE = date.minute
                m.OPEN = float(o)
                m.HIGH = float(h)
                m.LOW = float(l)
                m.CLOSE = float(c)
                m.VOL = float(v)
                m.AMOUNT = float(a)
                newklines.append(m)
            klines.clear()
        return newklines
    
    def get_date(self,date:str):
        # K线日期
        if len(date)==8:
            return datetime.datetime.strptime(date+" 15:00:00","%Y%m%d %H:%M:%S")
        # 分钟线时间格式 
        if len(date)==12:
            return datetime.datetime.strptime(date,"%Y%m%d%H%M")
    
    def next(self):
        self.cursor.index += 1
    
    def execute(self):
        t = time.time()
        # 把指标公式都注册进解析器函数库
        self.regs()
        for item in self.klines:
            # 计算所有注册指标
            # with ThreadPoolExecutor(max_workers=self.processors.__len__()) as executor:
            #     futures = []
            #     for sindexer in self.processors:
            #         # 得到指标的值
            #         future = executor.submit(sindexer.execute)
            #         setattr(future,"__typename__",sindexer.__typename__)
            #         futures.append(future)
            #     wait(futures)
            #     for future in futures:
            #         result = future.result()
            #         if result:
            #             setattr(item,future.__typename__,result)
            
            for sindexer in self.processors:
                # 得到指标的值
                result = sindexer.execute()
                if result:
                    setattr(item,sindexer.__typename__,result)
            self.next()
        t = time.time() - t
        logger.info("编译用时:%s s" % t)
        return self.klines

    def regs(self):
        # 把指标公式器都注册并实例化
        ps = []
        for item in self.processors:
            obj = item(self.klines,self.cursor)
            Functioner().register(obj)
            ps.append(obj)
        self.processors = ps
        