from dsxindexer.functioner import Functioner
from dsxindexer.sindexer.base_sindexer import BaseSindexer
class SindexerFactory:
    def __init__(self) -> None:
        pass
    @staticmethod
    def create(name,formula,typename:str=None,functioner=Functioner()):
        if typename==None: typename = name
        def dynamic_method():
            def formula_method(self):
                return formula
            return formula_method

        index_cls:BaseSindexer = type(name, (BaseSindexer,), {"formula":dynamic_method(),"__typename__":typename,"functioner":functioner})
        return index_cls
      

