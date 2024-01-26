# -*- coding: utf-8 -*-
"""

Created on Tue Nov  7 15:29:01 2023.
@author: Yuta Kuronuma
"""
import os

from inspector.check_base import *

from inspector.check_circle import *
from inspector.check_arc import *
# from inspector.check_lines import *

from inspector.check_frame import *
from inspector.check_titleblock import *
from inspector.check_outer_object import *
from inspector.check_outline_connectivity import *

if __name__ == '__main__':
    __all__ = [k[0:-3] for k in filter(lambda x: x[0: 6] == 'check_',
                                       os.listdir(os.path.dirname(__file__)))]
    form = 'from inspector.{} import *'
    for mod in __all__:
        if mod != 'check_result':
            print(form.format(mod))
