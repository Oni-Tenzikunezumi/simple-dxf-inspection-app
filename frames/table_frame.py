# -*- coding: utf-8 -*-
"""表を作成するモジュール.

Created on Sun Sep 10 22:30:41 2023.
@author: Yuta Kuronuma
"""

import tkinter as tk
from tkinter import ttk
from tkinter import scrolledtext

from frames.frame_constants import Fontsize


class TableFrame(tk.Frame):
    """表を作成するフレーム."""

    def __init__(self, master: tk.Tk | None = None,) -> None:
        """イニシャライザ.

        Parameters
        ----------
        master : tk.Tk | None, optional
            配置先のウィンドウ. The default is None.

        Returns
        -------
        None
        """
        super().__init__(master)

        # 表用のフレーム
        self.treeview_frame = tk.Frame(self)
        # TreeViewの仮作成
        self.tableset = tk.Frame(master=self.treeview_frame)
        self.create_table()

        # 詳細表示用フレーム
        info_frame = tk.Frame(self)
        label = ttk.Label(master=info_frame, text='詳細情報',  # テキストボックス
                          font=('', Fontsize.HEAD), padding=(30, 0, 30, 0))
        self.text_box = scrolledtext.ScrolledText(master=info_frame,
                                                  state='disable',
                                                  padx=30,
                                                  font=('', Fontsize.CONTENT),
                                                  bd=2)
        label.pack(side=tk.TOP, fill=tk.BOTH)
        self.text_box.tag_config('error', foreground='red')
        self.text_box.pack(side=tk.TOP, fill=tk.BOTH)

        # 配置
        self.treeview_frame.place(x=0, rely=0, relwidth=1, relheight=0.7)
        info_frame.place(x=0, rely=0.7, relwidth=1, relheight=0.3)

        # バインド
        self.master.bind("<<TreeviewSelect>>", self.select_record)

    def create_table(self, columns: tuple[str] = ('', '', ''),
                     data: list[dict[str, any]] = None):
        """列名とデータから表を作成する."""
        self.tableset.destroy()
        self.tableset = tk.Frame(master=self.treeview_frame)
        self.tableset.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True)

        # 表の書式設定
        style = ttk.Style()
        style.configure('Treeview.Heading', font=('', Fontsize.HEAD, 'bold'), rowheight=30)
        style.configure('Treeview', font=('', Fontsize.CONTENT), rowheight=28)

        # 表用のフレーム
        # TreeView作成
        self.columns = columns
        self.table = ttk.Treeview(master=self.tableset,
                                  columns=self.columns,
                                  padding=(0, 0, 0, 0))
        # スクロールバー作成
        y_sb = ttk.Scrollbar(self.tableset,
                             orient=tk.VERTICAL,
                             command=self.table.yview)
        x_sb = ttk.Scrollbar(self.tableset,
                             orient=tk.HORIZONTAL,
                             command=self.table.xview)
        self.table.configure(yscrollcommand=y_sb.set, xscrollcommand=x_sb.set)
        # 配置
        x_sb.pack(side=tk.BOTTOM, fill=tk.BOTH)
        y_sb.pack(side=tk.RIGHT, fill=tk.BOTH)
        self.table.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True)

        if data is not None:
            self.update_table(data)

    def set_columns(self):
        """TreeViewの列設定を行う.

        Returns
        -------
        None.

        """
        self.table.tag_configure('head', background='gray70')
        self.table.column('#0', width=0, stretch='no')
        self.table.heading('#0', text='')

        self.table.column

        if self.columns == ('No', '見出し', '検査項目', '説明'):
            self.table.column('No', anchor='c', stretch=False, width=50)
            self.table.heading('No', text='No', anchor='center')
            self.table.column('見出し', anchor='c', stretch=False, width=150)
            self.table.heading('見出し', text='見出し', anchor='center')
            self.table.column('検査項目', anchor='c', stretch=False, width=150)
            self.table.heading('検査項目', text='検査項目', anchor='center')
            self.table.column('説明', anchor='w', width=200)
            self.table.heading('説明', text='説明', anchor='center')
        else:
            for col in self.columns:
                self.table.column(col, anchor='e', width=100)
                self.table.heading(col, text=col, anchor='center')

    def update_table(self,
                     data: list[dict[str, any]]) -> None:
        """データを読み込み表を作成する.

        Parameters
        ----------
        data : dict[str, any]
            表示するデータ.

        Returns
        -------
        None
        """
        self.data = data
        self.set_columns()

        # タグ設定
        tag = ['even', 'odd']
        self.table.tag_configure(tag[0], background='gray85')
        self.table.tag_configure(tag[1], background='gray70')

        # テーブルの初期化
        for ele in self.table.get_children():
            self.table.delete(ele)

        # データの挿入
        for i, val in enumerate(self.data):
            # 値の抽出
            values = [val[col] for col in self.columns]
            self.table.insert(parent='',
                              index='end',
                              iid=i,
                              values=values,
                              tags=tag[i % 2])  # レコードの色を縞にする

    def select_record(self, event):
        """レコード選択時に実行される関数.

        Parameters
        ----------
        event : TYPE
            選択時のイベント.

        Returns
        -------
        None.

        """
        record_id = int(self.table.focus())
        if record_id == '':
            return
        # text = 'Number: {}\n'.format(record_id+1)
        text = ''
        for key, val in self.data[record_id].items():
            text += "{}: {}\n".format(key, val)

        self.print_message(text)

    def print_message(self, message):
        """テキストボックス内を消してから文字列を表示する."""
        self.text_box.config(state='normal')
        self.text_box.delete('1.0', self.text_box.index(tk.END))
        self.text_box.insert(index='1.0', chars=message)
        self.text_box.config(state='disable')

    def add_message(self, message, error=False):
        """テキストボックス内に文字列を追加する."""
        self.text_box.config(state='normal')
        self.text_box.insert(index=tk.END, chars='\n')

        if error:
            self.text_box.insert(tk.END, message, 'error')
        else:
            self.text_box.insert(index=tk.END, chars=message)
        self.text_box.config(state='disable')
