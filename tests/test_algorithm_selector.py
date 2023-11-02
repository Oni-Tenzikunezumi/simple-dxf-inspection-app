# -*- coding: utf-8 -*-
"""algorithm_selectorのテスト.

Created on Thu Nov  2 16:20:45 2023.
@author: Yuta Kuronuma
"""

import tkinter as tk
import tkinter.ttk as ttk

from frames.algorithm_selector import AlgorithmSelector


class TestBase:
    """テスト用クラス"""
    inspect_name: str = 'テストベース'
    inspect_str: str = 'テストのベース'

    @staticmethod
    def inspect_doc():
        print('実行（テスト用クラス）')


class TestClass1(TestBase):
    """1番目"""
    inspect_name: str = 'テスト1番'
    inspect_str: str = '1番目テストクラス'

    @staticmethod
    def inspect_doc():
        print('実行（1番目）')


class TestClass2(TestBase):
    """2番目"""
    inspect_name: str = 'テスト2番'
    inspect_str: str = '2番目テストクラス'

    @staticmethod
    def inspect_doc():
        print('実行（2番目）')


class TestClass3(TestBase):
    """3番目"""
    inspect_name: str = 'テスト3番'
    inspect_str: str = '3番目テストクラス'

    @staticmethod
    def inspect_doc():
        print('実行（3番目）')


if __name__ == '__main__':
    print('aa')

    root = tk.Tk()
    root.geometry('220x200')
    root.title('AlgorithmSelector test')

    index = tk.IntVar()
    algo = AlgorithmSelector(TestBase, root)
    algo.pulldown.bind('<<ComboboxSelected>>',
                       lambda e: index.set(algo.pulldown.current()))
    algo.pack()

    button = tk.Button(root, text='読み取り', command=lambda:
                       print(algo.get(index.get())))
    button.pack()

    root.mainloop()
