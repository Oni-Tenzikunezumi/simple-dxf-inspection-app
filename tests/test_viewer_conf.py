# -*- coding: utf-8 -*-
"""ViewerConfのテスト

Created on Tue Sep 19 15:01:02 2023.
@author: Yuta Kuronuma
"""

from frames.viewer_conf import ViewerConf

# テスト
if __name__ == '__main__':
    vc = ViewerConf(initialize_conf=True)
    print('latest path: ', vc.get_odapath())

    path = 'test'
    # vc.update_odapath(path)

    print()
    print('ODApath: ', vc.get_odapath())
    print('confPath: ', vc.dirpath)
    print('Is ODAinstalled: ', vc.is_oda_installed)
