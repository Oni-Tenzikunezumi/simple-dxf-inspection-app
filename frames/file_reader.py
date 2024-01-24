# -*- coding: utf-8 -*-
"""DXFファイルを読み込むモジュール.

Created on Tue Sep 19 20:11:18 2023.
@author: Yuta Kuronuma
"""

import tkinter as tk
import tkinter.ttk as ttk
from tkinter import filedialog
import os.path

from ezdxf.addons import odafc as oda
from ezdxf.document import Drawing
import ezdxf

from frames.viewer_conf import ViewerConf


class FileReader(tk.Frame):
    """DXFファイルを読み込むクラス."""

    doc = None

    def __init__(self, master: tk.Tk, vconf: ViewerConf):
        """イニシャライザ."""
        super().__init__(master)
        self.vconf = vconf

        # 読み込み用フォームの作成
        self._filepath = tk.StringVar()
        path_entry = ttk.Entry(self, width=60,
                               textvariable=self._filepath)
        referring_button = ttk.Button(self, width=-1,
                                      text='参照',
                                      command=self.browse_path)
        # self.executing_button = ttk.Button(self,
        #                                    text='読み込み',
        #                                    command=self.read_file)

        # 配置
        path_entry.pack(side=tk.LEFT)
        referring_button.pack(side=tk.LEFT)
        # self.executing_button.pack(side=tk.LEFT)

    def browse_path(self):
        """パス指定."""
        filetype = [('DXFファイル', '*.dxf')]
        if self.vconf.is_oda_installed:
            filetype = [('図面ファイル', '*.dwg;*.dxf'), ('AutoCADファイル', '*.dwg'),
                        ('DXFファイル', '*.dxf')]
        file_path = filedialog.askopenfile(filetype=filetype)
        if file_path is not None:
            self._filepath.set(file_path.name)

    def read_file(self) -> tuple[Drawing, str]:
        """ファイルの読み込み."""
        filepath = self._filepath.get()
        text = ''

        # ファイル形式の確認
        if os.path.splitext(filepath)[1] == '.dxf':
            # dxfの場合読み込み
            text = 'dxfファイルを読み込みました.'
            self.doc = ezdxf.readfile(filepath)

        elif os.path.splitext(filepath)[1] == '.dwg':
            # dwgの場合,ODAが入っていれば読み込み
            if self.vconf.is_oda_installed:
                text = 'dwgファイルを読み込みました．'
                self.doc = oda.readfile(filepath)

            else:
                text = 'ODA File Converterが設定されていないため，\n'\
                    'dwgファイルを読み込むことはできません．'

        # パスの存在確認
        elif os.path.exists(filepath):
            print(os.path.splitext(filepath))
            text = 'このアプリケーションでは利用できないパスです．'

        else:
            text = '存在しないパスが指定されています．'

        # メッセージを返す.
        return self.doc, text

    @property
    def file_path(self):
        """ファイルパスを返す."""
        return self._filepath.get()
