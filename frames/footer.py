# -*- coding: utf-8 -*-
"""フッターのモジュール.

Created on Tue Sep 19 15:28:16 2023.
@author: Yuta Kuronuma
"""

import os

import tkinter as tk
import tkinter.ttk as ttk

from frames.viewer_conf import ViewerConf


class Footer(tk.Frame):
    """フッターのクラス."""

    def __init__(self, master: tk.Tk, vconf: ViewerConf):
        """イニシャライザ."""
        super().__init__(master)
        self.vconf = vconf

        # 各ラベルの作成
        self.odastate = tk.StringVar()
        odastate_label = ttk.Label(master=self,
                                   textvariable=self.odastate,
                                   padding=[10, 0])

        self.filename = tk.StringVar()
        self.filename.set('File Name: None')
        filename_label = ttk.Label(master=self,
                                   textvariable=self.filename,
                                   padding=[10, 0])

        self.algoname = tk.StringVar()
        algoname_label = ttk.Label(master=self,
                                   textvariable=self.algoname,
                                   padding=[10, 0])

        # ラベルの初期化
        self.update_footer()

        # 配置
        odastate_label.pack(side=tk.RIGHT)
        filename_label.pack(side=tk.RIGHT)
        algoname_label.pack(side=tk.RIGHT)

    def update_footer(self):
        """値の更新."""
        self.set_filename()
        self.set_algoname()
        self.set_oda_state()

    def set_filename(self, path: str = None):
        """表示するファイル名をパスから指定.

        指定がない場合は変更しない.
        """
        form = 'File Name: {}'
        basename = 'None'

        if path is not None and os.path.exists(path):
            basename = os.path.basename(path)
            self.filename.set(form.format(basename))

    def set_algoname(self, inspect_name: str = None):
        """実行した検図内容を表示.

        指定がない場合は変更しない.
        """
        form = '検図内容: {}'
        basename = '未実行' if inspect_name is None else inspect_name

        self.algoname.set(form.format(basename))


    def set_oda_state(self):
        """ODAのインストール状況を表示する."""
        form = 'ODA: {}'
        state = '未設定'

        if self.vconf.is_oda_installed:
            state = '設定済'
        self.odastate.set(form.format(state))
