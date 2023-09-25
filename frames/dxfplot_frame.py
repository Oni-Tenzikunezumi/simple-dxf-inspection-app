# -*- coding: utf-8 -*-
"""MatplotlibでDXFを表示させるモジュール.

Created on Wed Sep  6 16:37:41 2023.
@author: Yuta Kuronuma
"""

import ezdxf

import re
import matplotlib.pyplot as plt
from ezdxf.addons.drawing import RenderContext, Frontend
from ezdxf.addons.drawing.matplotlib import MatplotlibBackend
from ezdxf.addons.drawing.properties import LayoutProperties

import tkinter as tk
import matplotlib.backends.backend_tkagg as tkplt


class DxfPlotFrame(tk.Frame):
    """DXFをmatplotlibで表示するフレーム."""

    def __init__(self,
                 master: tk.Tk | None = None,
                 doc: ezdxf.document.Drawing = ezdxf.new('R2018'),
                 color: str = "#eaeaea") -> None:
        """イニシャライザ.

        Parameters
        ----------
        master : tk.Tk | None, optional
            配置先のウィンドウ. The default is None.
        doc : ezdxf.document.Drawing, optional
            表示させるDXFファイルのドキュメント. The default is ezdxf.new('R2018').
        color : str, optional
            図面の背景色. The default is "#eaeaea".

        Returns
        -------
        None

        """
        # メンバの宣言
        super().__init__(master)
        self.doc = doc
        self.fig = plt.figure()
        self.color = color

        # plt用canvasの作成
        self.fig_canvas = tkplt.FigureCanvasTkAgg(self.fig, master=self)
        self.plt_toolbar = tkplt.NavigationToolbar2Tk(self.fig_canvas, self)
        self.fig_canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)
        self.fig_canvas.get_tk_widget().configure(bg=self.color)

        # 更新
        self.update_plot()

    def update_plot(self,
                    doc: ezdxf.document.Drawing | None = None) -> None:
        """self.docの図面をpltに書き出す.

        docを指定した場合,表示する図面を差し替える.

        Parameters
        ----------
        doc : ezdxf.document.Drawing | None, optional
            変更先の図面. The default is None.

        Returns
        -------
        None.

        """
        # モデルスペースの取得
        if doc is not None:
            self.doc = doc

        msp = self.doc.modelspace()
        msp_properties = LayoutProperties.from_layout(msp)

        msp_properties.set_colors(self.color)
        self.fig_canvas.get_tk_widget().configure(bg=self.color)

        ax = self.fig.add_axes([0, 0, 1, 1])
        ctx = RenderContext(self.doc)
        out = MatplotlibBackend(ax)
        Frontend(ctx, out).draw_layout(msp, finalize=True,
                                       layout_properties=msp_properties)
        self.fig_canvas.draw()

        self.refresh_plot()

    def refresh_plot(self):
        """更新したプロットを表示しなおす.

        Returns
        -------
        None.

        """
        # windowの更新
        self.master.update()

        # 現在状態の取得
        s = self.master.state()
        geo = self.master.geometry()
        w, h, x, y = list(map(int, re.split('[+x]', geo)))
        if s == 'zoomed':
            x, y = 0, 0

        # サイズを変更しキャンバスを表示
        self.master.state('normal')
        self.master.geometry('{}x{}+{}+{}'.format(w-1, h-1, x, y))
        self.master.update()

        # 元の状態に戻す
        self.master.geometry('{}x{}+{}+{}'.format(w, h, x, y))
        self.master.state(s)
