# -*- coding: utf-8 -*-
"""check_baseのテスト.

Created on Wed Nov  1 10:44:25 2023.
@author: Yuta Kuronuma
"""

import ezdxf
from pprint import pprint

import sys
import os.path as path
sys.path.append(path.join(path.dirname(__file__), '../..'))
from inspector.check_base import CheckBase

file_path = r'../../dxf/700.dxf'
doc = ezdxf.readfile(file_path)


document, col, data = CheckBase.inspect_doc(doc)
print(document)
print(col)
pprint(data)
