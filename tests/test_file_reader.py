# -*- coding: utf-8 -*-
"""FileReaderのテスト.

Created on Tue Sep 19 16:29:33 2023.
@author: Yuta Kuronuma
"""


import tkinter as tk

from frames.file_reader import FileReader
from frames.viewer_conf import ViewerConf


def print_doc():
    doc, msg = fr.read_file()
    print(doc)
    print(msg)
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
