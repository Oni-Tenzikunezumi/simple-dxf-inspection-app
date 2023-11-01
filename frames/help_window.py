# -*- coding: utf-8 -*-
"""ヘルプ表示ウィンドウのモジュール.

Created on Wed Nov  1 15:58:21 2023.
@author: Yuta Kuronuma
"""

import tkinter as tk
import tkinter.ttk as ttk
from tkinter import scrolledtext

class HelpWindow(tk.Frame):
    """ヘルプ表示用ウィンドウクラス."""

    # 取扱説明書
    help_str = '取扱説明書\n'\
               '今後作成予定\n'\
               '詳細情報\n'

    def __init__(self, master: tk.Tk | None = None):
        """イニシャライザ.

        Parameters
        ----------
        master : tk.Tk | None, optional
            配置先のウィンドウ. The default is None.

        Returns
        -------
        None.

        """
        super().__init__(master)

        # 情報表示用フレーム
        info_frame = tk.Frame(self)
        text_box = scrolledtext.ScrolledText(master=info_frame,
                                             font=('', 20),
                                             bd=2)
        text_box.insert(index=tk.END, chars=self.help_str)
        text_box.config(state='disable')
        text_box.pack(side=tk.TOP, fill=tk.BOTH)
        info_frame.pack()
