
import importlib
import inspect
import re
import traceback
from dsxindexer.configer import RegRolues

class BaseProcessor:

    # 注册
    processors:list = [
    ]

    def __init__(self) -> None:
        pass

    def register(self,processor):
        self.assosiation_import(processor)
        # 传字符串的话就去sindexer去查找模块
        if isinstance(processor,str):
            processor = self.import_str(processor)
            if processor==None:return
        if processor not in self.processors:
            self.processors.append(processor)
    
    def import_str(self,strname):
        processor = None
        try:
            path = "dsxindexer.sindexer.%s" % strname
            module = importlib.import_module(path)
            # 获取模块中的所有成员
            members = inspect.getmembers(module)
            # 查找类
            for name, obj in members:
                if inspect.isclass(obj) and name == strname:
                    processor = obj
                    break
        except Exception as e:
            traceback.print_exc()
        return processor
    
    def assosiation_import(self,processor):
        """导入关联的类

        Args:
            processor (_type_): _description_
        """
        # from dsxindexer.sindexer.base_sindexer import BaseSindexer
        if not hasattr(processor,"formula"):return
        # 首先取得模块的公式
        if type(processor)==type : processor = processor(None,None)
        if hasattr(processor,"formula"):
            formula = getattr(processor,"formula")()
            # 识别公式的点号引用
            matchlist = re.findall(RegRolues.OBJ_POINT_VAR,formula)
            lastname = []
            for item in matchlist:
                if item not in lastname:
                    self.register(item)
                lastname.append(item)
        del processor

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
        