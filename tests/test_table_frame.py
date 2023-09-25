# -*- coding: utf-8 -*-
"""TableFrameのテスト.

Created on Tue Sep 19 15:01:02 2023.
@author: Yuta Kuronuma
"""

import sys
import os
import time

import ezdxf
import tkinter as tk

sys.path.append(os.path.join(os.path.dirname(__file__), '..'))
from frames.table_frame import TableFrame

# テスト
if __name__ == '__main__':
    # DXF読み込み
    path = r'../dxf/700.dxf'

    doc = ezdxf.readfile(path)

    # データの挿入
    columns = ('handle', 'owner', 'layer')
    lists = [ent.dxfattribs() for ent in doc.query('LINE')]

    # ウィンドウ作成
    root = tk.Tk()
    root.geometry('{}x{}+200+200'.format(1500, 800))
    tableframe = TableFrame()

    # 表作成
    buttonframe = tk.Frame(root)
    button = tk.Button(buttonframe, text='create',
                       command=lambda:
                           tableframe.create_table(columns, lists))
    button.pack(side=tk.LEFT)

    button2 = tk.Button(buttonframe, text='time',
                        command=lambda:
                            tableframe.add_message(
                                '今の時間は:{}'.format(time.time())))
    button2.pack(side=tk.LEFT)

    # 配置
    tableframe.pack(fill=tk.BOTH, expand=True)
    buttonframe.pack()

    # 実行
    root.mainloop()
