class Formulas:

    @staticmethod
    def MACD(X="CLOSE",SHORT=12,LONG=26,MID=9): 
        s = """
        SHORT:=%s;
        LONG:=%s;
        MID:=%s;
        DIF:=EMA(%s,SHORT)-EMA(%s,LONG);
        DEA:=EMA(DIF,MID);
        MACD:=(DIF-DEA)*2;
        """
        return s % (SHORT,LONG,MID,X,X)
    
    @staticmethod
    def MACD2(X="CLOSE",SHORT=13,LONG=27,MID=8): 
        s = """
        SHORT:=%s;
        LONG:=%s;
        MID:=%s;
        MACD2:=MACD(%s,SHORT,LONG,MID);
        """
        return s % (SHORT,LONG,MID,X)
