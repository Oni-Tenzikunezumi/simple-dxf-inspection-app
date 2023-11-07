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

if __name__ == '__main__':
    file_path = r'../../dxf/700.dxf'
    doc = ezdxf.readfile(file_path)

    document, col, data = CheckBase.inspect_doc(doc)
    pprint(document)
    pprint(col)
    pprint(data[0:2])

"""
document
    <ezdxf.document.Drawing object at 0x00000279420C2620>

col
    ('owner', 'handle')

data[0:2]
    [{'end': Vec3(1610.0, 1234.968796065397, 0.0),
      'handle': '2EE',
      'layer': '外形線',
      'owner': '1F',
      'start': Vec3(1610.0, 960.0, 0.0)},
     {'end': Vec3(2010.0, 960.0, 0.0),
      'handle': '2F0',
      'layer': '外形線',
      'owner': '1F',
      'start': Vec3(2010.0, 1234.968796065397, 0.0)}]
"""
