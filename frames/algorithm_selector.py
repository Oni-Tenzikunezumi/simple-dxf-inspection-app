# -*- coding: utf-8 -*-
"""検図アルゴリズム入れ替え用モジュール.

Created on Thu Nov  2 13:14:22 2023.
@author: Yuta Kuronuma
"""

import ezdxf

import tkinter as tk
import tkinter.ttk as ttk



class AlgorithmSelector(tk.Frame):
    """検図アルゴリズムを選択するためのクラス."""

    def __init__(self, base_class, master: tk.Tk | None = None):
        """イニシャライザ."""
        super().__init__(master)

        # プルダウンメニュー
        self.v = tk.StringVar()
        self.values = self.setValues()
        self.pulldown = ttk.Combobox(self, values=self.values,
                                     textvariable=self.v)
        self.pulldown.set(self.values[0])
        self.pulldown.config(state="readonly")

        # 詳細用ラベル
        self.detail = tk.StringVar()
        self.detail.set('test')
        self.label = ttk.Label(self, textvariable=self.detail)

        self.pulldown.pack()
        self.label.pack()

    def get(self, index: int):
        """プルダウン内の値を返す."""
        return self.values[index]

    def setValues(self):
        """プルダウンメニューの内容を設定する."""
        vals = ('0個め', '一つ目', '二つ目', '三つ目', '四つ目', '五つ目', '六つ目', )
        return vals



