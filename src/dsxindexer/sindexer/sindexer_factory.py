from dsxindexer.sindexer.base_sindexer import BaseSindexer
class SindexerFactory:
    def __init__(self) -> None:
        pass
    @staticmethod
    def create(name,formula,typename:str=None):
        if typename==None: typename = name
        def dynamic_method():
            def formula_method(self):
                return formula
            return formula_method

        index_cls:BaseSindexer = type(name, (BaseSindexer,), {"formula":dynamic_method(),"__typename__":typename})
        return index_cls
      

