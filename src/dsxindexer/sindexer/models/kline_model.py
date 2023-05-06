
class KlineModel:
    def __init__(self) -> None:
        self.DATE:str
        self.TIME:str
        self.YEAR:int
        self.MONTH:int
        self.DAY:int
        self.WEEK:int
        self.HOUR:int
        self.MINUTE:int
        self.OPEN:float
        self.HIGH:float
        self.LOW:float
        self.CLOSE:float
        self.VOL:float
        self.AMOUNT:float

    def setvalue(self,key,value):
        self.__setattr__(key,value)
    