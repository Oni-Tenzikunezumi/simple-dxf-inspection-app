# -*- coding: utf-8 -*-
"""FileReaderのテスト.

Created on Tue Sep 19 16:29:33 2023.
@author: Yuta Kuronuma
"""

import sys
import os

import tkinter as tk

sys.path.append(os.path.join(os.path.dirname(__file__), '..'))
from frames.file_reader import FileReader
from frames.viewer_conf import ViewerConf


def print_doc():
    fr.read_file()
    doc = fr.doc
    print(doc)
    print('テスト側の実行')


if __name__ == '__main__':
    root = tk.Tk()
    vc = ViewerConf()

    fr = FileReader(root, vc)
    fr.pack()
    # fr.executing_button.config(command=print_doc)
    button = tk.Button(root, text='読み込み',
                       command=print_doc)

    button.pack()
    root.mainloop()
