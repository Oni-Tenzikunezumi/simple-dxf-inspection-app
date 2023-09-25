# -*- coding: utf-8 -*-
"""ViewerConfのテスト

Created on Tue Sep 19 15:01:02 2023.
@author: Yuta Kuronuma
"""

import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

from frames.viewer_conf import ViewerConf

# テスト
if __name__ == '__main__':
    vc = ViewerConf()
    print(vc.get_odapath())

    path = 'test'
    vc.update_odapath(path)
    print(vc.get_odapath())
    print(vc.dirpath)
    print(vc.get_odapath())
    print(vc.is_oda_installed)