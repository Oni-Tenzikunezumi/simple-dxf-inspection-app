# -*- coding: utf-8 -*-
"""algorithm_selectorのテスト.

Created on Thu Nov  2 16:20:45 2023.
@author: Yuta Kuronuma
"""

import tkinter as tk
from pprint import pprint as pprint

from frames.algorithm_selector import AlgorithmSelector

from inspector.check_base import CheckBase
# from inspector_test import *


if __name__ == '__main__':
    # a = CheckBase.__subclasses__()
    # pprint(a)
    # for c in a:
    #     print(c.inspect_name, end=', ')
    #     c.inspect_doc()

    root = tk.Tk()
    root.geometry('220x200')
    root.title('AlgorithmSelector test')

    index = tk.IntVar()
    algo = AlgorithmSelector(CheckBase, root)
    # algo.pulldown.bind('<<ComboboxSelected>>',
    #                    lambda e: print('select'))
    algo.pack()

    button = tk.Button(root, text='読み取り', command=lambda:
                       print(algo.get_val().inspect_str))
    button.pack()

    root.mainloop()
