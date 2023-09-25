# -*- coding: utf-8 -*-
"""DxfPlotFrameのテスト.

Created on Tue Sep 19 15:01:00 2023.
@author: Yuta Kuronuma
"""

import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

import ezdxf
from ezdxf.addons.drawing.properties import LayoutProperties

import tkinter as tk

from frames.dxfplot_frame import DxfPlotFrame


def set_max(root: tk.Tk):
    """最大化."""
    print(root.geometry())
    print(root.wm_resizable())


def quit():
    """終了用関数."""
    root.quit()
    root.destroy()
    print('Quit')


if __name__ == '__main__':
    # DXF読み込み

    path = r'../dxf/700.dxf'
    doc = ezdxf.readfile(path)
    msp = doc.modelspace()

    msp_properties = LayoutProperties.from_layout(msp)

    # ウィンドウ作成
    root = tk.Tk()
    root.geometry('{}x{}+200+200'.format(1500, 800))
    root.protocol('WM_DELETE_WINDOW', quit)

    # フレーム作成----------------------------------------
    # 描画フレーム
    dpframe = DxfPlotFrame(master=root)

    frame = tk.Frame(master=root)
    # 図面の読み込み
    button = tk.Button(frame, text='実行',
                       command=lambda: dpframe.update_plot(doc))

    button2 = tk.Button(frame, text='Set Max',
                        command=lambda: set_max(root))
    button.pack(side=tk.LEFT)
    button2.pack(side=tk.LEFT)

    # 配置---------------------------------------------
    frame.pack()
    dpframe.pack(fill=tk.BOTH, expand=True)

    # 実行
    root.mainloop()
# #212830
