# -*- coding: utf-8 -*-
"""SimpleViewMenuのテスト.

Created on Tue Sep 19 14:48:04 2023.
@author: Yuta Kuronuma
"""

import sys
import os
import tkinter as tk

sys.path.append(os.path.join(os.path.dirname(__file__), '..'))
from frames.menubar import SimpleViewMenu
from frames.viewer_conf import ViewerConf

if __name__ == '__main__':

    root = tk.Tk()
    root.title('Menu Test')
    root.geometry('{}x{}+200+200'.format(500, 100))
    vc = ViewerConf(initialize_conf=True)

    menu = SimpleViewMenu(root, vc)

    root.mainloop()
