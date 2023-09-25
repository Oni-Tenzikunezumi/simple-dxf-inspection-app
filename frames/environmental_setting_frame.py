# -*- coding: utf-8 -*-
"""環境設定用ウィンドウのモジュール.

Created on Fri Sep 15 16:36:15 2023.
@author: Yuta Kuronuma
"""

from ezdxf.addons import odafc as oda

from os import path
import tkinter as tk
import tkinter.ttk as ttk
from tkinter import filedialog

from frames.viewer_conf import ViewerConf


class EnvironmentalSettingFrame(tk.Frame):
    """環境設定を行うフレームのクラス."""

    def __init__(self, master, vconf: ViewerConf):
        """イニシャライザ.

        Parameters
        ----------
        vconf : ViewerConf
            環境設定変数.
        master : tk.Tk, optional
            表示先. The default is None.

        Returns
        -------
        None.

        """
        super().__init__(master)
        self.vconf = vconf

        self.master.geometry('{}x{}'.format(700, 300))
        oda_frame = ttk.Labelframe(self,
                                   text='ODA File Converter',
                                   borderwidth=10)

        # 説明
        oda_description = 'AutoCADファイルを直接読み込む設定をします.\n'\
            'ODA File Converterをインストールし，実行ファイル(.exe)のパスを指定してください．\n'\
            '通常は"C:\\Program Files\\ODA\\"にインストールされます．'
        description = ttk.Label(oda_frame, text=oda_description)

        # 設定状況の表示
        self.install_status = tk.StringVar()
        install_status_label = ttk.Label(oda_frame,
                                         textvariable=self.install_status,
                                         padding=[0, 10, 0, 0])

        # 読み込みエントリ
        read_frame = ttk.Frame(oda_frame)
        label = ttk.Label(read_frame, text='Path')
        self.oda_path = tk.StringVar()
        entry = ttk.Entry(read_frame, textvariable=self.oda_path, width=55)
        button1 = ttk.Button(read_frame,
                             text='参照',
                             command=self.ask_odapath,
                             width=-1)
        button2 = ttk.Button(read_frame,
                             text='設定',
                             command=self.check_odapath)
        label.pack(side=tk.LEFT)
        entry.pack(side=tk.LEFT)
        button1.pack(side=tk.LEFT)
        button2.pack(side=tk.LEFT)

        # 各変数の更新
        self.oda_path.set(self.vconf.get_odapath())
        self.check_odapath()
        self.set_odastatus()

        # 配置
        oda_frame.pack()

        description.pack()
        install_status_label.pack()
        read_frame.pack()

    def ask_odapath(self):
        """odaのファイルパスを検索する.

        exeファイルのみを指定させる
        指定がない場合はパスの変更を行わない.
        """
        idir = r"C:\\Program Files\\ODA\\"
        filetype = [('exeファイル', '*.exe')]
        file_path = filedialog.askopenfile(filetype=filetype,
                                           initialdir=idir)
        print(file_path)

        if file_path is not None:
            self.oda_path.set(file_path.name)

    def check_odapath(self):
        """ODAのパスか確認する.

        ODAのパスならばvconfを更新する.
        """
        oda_path = self.oda_path.get()

        # print('path:', oda.win_exec_path)
        # print(is_installed)

        if self.vconf.is_oda_path(oda_path):
            self.vconf.update_odapath(oda_path)
        self.set_odastatus()

    def set_odastatus(self):
        """ODAのインストール状況に関するメッセージを設定する."""
        text = '現在の設定: '
        if self.vconf. is_oda_installed:
            text += 'パスが指定されています．利用可能です．'
        else:
            text += '正しいパスが指定されていません．'
        self.install_status.set(text)
