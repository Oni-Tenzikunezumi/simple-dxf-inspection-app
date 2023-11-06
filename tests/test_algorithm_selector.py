# -*- coding: utf-8 -*-
"""algorithm_selectorのテスト.

Created on Thu Nov  2 16:20:45 2023.
@author: Yuta Kuronuma
"""

import tkinter as tk
import tkinter.ttk as ttk
from pprint import pprint as pprint

from frames.algorithm_selector import AlgorithmSelector
from tests.inspector_test.test_class import TestBase
from tests.inspector_test.test_subclass import TestBase


if __name__ == '__main__':
    print('aa')

    a = TestBase.__subclasses__()
    pprint(a)
    for c in a:
        print(c.inspect_name)
        c.inspect_doc()


    # root = tk.Tk()
    # root.geometry('220x200')
    # root.title('AlgorithmSelector test')

    # index = tk.IntVar()
    # algo = AlgorithmSelector(TestBase, root)
    # algo.pulldown.bind('<<ComboboxSelected>>',
    #                    lambda e: index.set(algo.pulldown.current()))
    # algo.pack()

    # button = tk.Button(root, text='読み取り', command=lambda:
    #                    print(algo.get(index.get())))
    # button.pack()

    # root.mainloop()
