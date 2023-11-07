# -*- coding: utf-8 -*-
"""DXFの図面と表のみを表示する.

Created on Mon Sep 11 10:55:52 2023.
@author: Yuta Kuronuma
"""

import tkinter as tk
import tkinter.ttk as ttk
import traceback

from frames.dxfplot_frame import DxfPlotFrame
from frames.table_frame import TableFrame
from frames.menubar import SimpleViewMenu
from frames.viewer_conf import ViewerConf
from frames.footer import Footer
from frames.file_reader import FileReader
from frames.algorithm_selector import AlgorithmSelector

from inspector.check_base import CheckBase
from inspector import *


class SimpleViewer():
    """表，図面のみ."""

    def __init__(self, master: tk.Tk):
        """イニシャライザ.

        Parameters
        ----------
        master : tk.Tk
            配置先のウィンドウ.

        Returns
        -------
        None
            DESCRIPTION.

        """
        self.master = master

        # 設定の読み込み
        self.vconf = ViewerConf()

        # フレームのインスタンス化
        self.plot_frame = DxfPlotFrame(master=self.master)
        self.table_frame = TableFrame(master=self.master)
        self.footer = Footer(self.master, self.vconf)
        self.readpath_frame = FileReader(self.master, self.vconf)
        self.selector = AlgorithmSelector(CheckBase, self.master)

        # 実行ボタンの作成
        self.execution_button = ttk.Button(
            self.master, text='検図',
            command=lambda: self.process_doc(error_to_console=True))

        # メニューバー
        _ = SimpleViewMenu(master=self.master,
                           viewer_conf=self.vconf,
                           footer=self.footer)

        # 配置
        self.readpath_frame.pack(side=tk.TOP)
        self.selector.pack(side=tk.TOP)
        self.execution_button.pack()

        self.footer.pack(side=tk.BOTTOM, fill=tk.X)

        self.plot_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        self.table_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        # バインド
        self.master.protocol('WM_DELETE_WINDOW', self.quit)

    def process_doc(self, error_to_console=True):
        """図面の読み込みと処理を行う."""
        message = self.readpath_frame.read_file()
        doc = self.readpath_frame.doc

        self.table_frame.print_message(message)
        if doc is not None:
            self.footer.set_filename(self.readpath_frame.file_path)
            inspector = self.selector.get_val()

            try:
                document, cols, data = inspector.inspect_doc(doc)

                # 図面表示
                self.plot_frame.update_plot(doc=doc)

                # 表の作成
                self.table_frame.create_table(columns=cols, data=data)

            except Exception as e:
                if error_to_console:
                    print(traceback.format_exc())
                else:
                    self.table_frame.add_message(e)

    def quit(self):
        """終了用関数."""
        root.quit()
        root.destroy()
        print('Quit')


# テスト
if __name__ == '__main__':

    # ウィンドウ作成
    root = tk.Tk()
    root.title('Simple Viewer')
    root.geometry('{}x{}+200+200'.format(1600, 900))

    # フレーム作成
    viewer = SimpleViewer(master=root)

    # 実行
    root.mainloop()
