# -*- coding: utf-8 -*-
"""Footerのテスト.

Created on Tue Sep 19 15:28:34 2023.
@author: Yuta Kuronuma
"""

import sys
import os

import tkinter as tk

sys.path.append(os.path.join(os.path.dirname(__file__), '..'))
from frames.footer import Footer
from frames.viewer_conf import ViewerConf

if __name__ == '__main__':

    root = tk.Tk()
    root.title('Footer Test.')

    vc = ViewerConf()
    ft = Footer(root, vc)
    ft.pack(side=tk.BOTTOM)

    path = r'C:\ProgramFiles\SimpleInspector\conf.ini'
    button = tk.Button(master=root,
                       text='set_path',
                       command=lambda: ft.set_filename(path))
    button.pack()

    path2 = None
    button2 = tk.Button(master=root,
                        text='None_path',
                        command=lambda: ft.set_filename(path2))
    button2.pack()

    root.mainloop()
