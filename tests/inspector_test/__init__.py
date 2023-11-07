# -*- coding: utf-8 -*-
"""inspectorテスト用.

Created on Mon Nov  6 14:41:16 2023.
@author: Yuta Kuronuma
"""

# from .test_class1 import TestClass1
# from .test_class2 import TestClass2
# from .test_class3 import TestClass3
import os

# _で始まるファイル以外のファイル名を取得
__all__ = [k[0:-3] for k in filter(lambda x: x[0] != '_',
                                   os.listdir(os.path.dirname(__file__)))]

# print('import inspector_test')
# from . import *
# print(__all__)
# print(os.listdir(os.path.dirname(__file__)))
# print(os.path.dirname(__file__))
# print(__file__)
