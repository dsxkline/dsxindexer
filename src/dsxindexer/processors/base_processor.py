
class BaseProcessor:

    # 注册
    processors:list = [
    ]

    def __init__(self) -> None:
        pass

    def register(self,processor):
        if processor not in self.processors:
            self.processors.append(processor)

    def remove(self,processor):
        if processor in self.processors:
            self.processors.remove(processor)
    
    def hasmethod(self,method_name):
        """查找方法

        Args:
            method_name (str): 方法名称
        """
        for item in self.processors:
            if item.type_name==method_name:
                return True
        return False
    
    def hasattr(self,attr_name):
        """查找属性

        Args:
            attr_name (str): 属性名称
        """
        for item in self.processors:
            obj = item
            # 检查对象是否已实例化
            if type(obj)==type: obj = item()
            if hasattr(obj,attr_name):
                return obj
            del obj
        return None
    

    def call(self,type_name,*args):
        pass
        