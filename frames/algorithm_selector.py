# -*- coding: utf-8 -*-
"""検図アルゴリズム入れ替え用モジュール.

Created on Thu Nov  2 13:14:22 2023.
@author: Yuta Kuronuma
"""

import tkinter as tk
import tkinter.ttk as ttk


class AlgorithmSelector(tk.Frame):
    """検図アルゴリズムを選択するためのクラス."""

    __current_index = 0

    def __init__(self, baseclass, master: tk.Tk | None = None):
        """イニシャライザ."""
        super().__init__(master)

        # 各表示内容の初期化
        self.set_baseclass(baseclass)

        # プルダウンメニュー
        self.pulldown = ttk.Combobox(self, values=self.names)
        self.pulldown.current(self.__current_index)
        self.pulldown.config(state="readonly")
        self.pulldown.bind('<<ComboboxSelected>>',
                           lambda e: self.__update_display())

        # 詳細用ラベル
        self.detail = tk.StringVar()
        self.detail.set(self.details[self.__current_index])
        self.label = ttk.Label(self, textvariable=self.detail)

        self.pulldown.pack()
        self.label.pack()

    def __update_display(self):
        """index, detail,の更新を行う."""
        # print('update')
        self.__current_index = self.pulldown.current()
        self.detail.set(self.details[self.__current_index])

    def get_val(self):
        """選択されている値を返す."""
        return self.values[self.__current_index]

    def set_baseclass(self, baseclass):
        """指定されたベースクラスから情報を抽出する."""
        subclasses = baseclass.__subclasses__()
        if len(subclasses) == 0:
            subclasses.append(baseclass)
        self.names = [sub.inspect_name for sub in subclasses]
        self.details = [sub.inspect_str for sub in subclasses]
        self.values = subclasses
