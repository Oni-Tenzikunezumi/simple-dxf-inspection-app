# -*- coding: utf-8 -*-
"""frame_extractorのテスト

Created on Sat Nov 18 16:47:30 2023.
@author: Yuta Kuronuma
"""


import tkinter as tk
import ezdxf
from typing import Any
from simple_viewer import SimpleViewer
from inspector.check_base import CheckBase


class FrameExtractorTestClass(CheckBase):
    """frame_extractorのテストクラス."""

    inspect_name: str = '枠線抽出テスト'
    inspect_str: str = '枠線を抽出し，詳細を表示します．'

    @staticmethod
    def inspect_doc(doc: ezdxf.document.Drawing, Option: tuple[Any] = None):
        """枠線を抽出し，詳細を表示."""

        frameresult = Option[0]

        print(frameresult.framePoint)
        print(frameresult.message)

        # 図面の処理
        data = [ent.dxfattribs() for ent in doc.query('LINE')]

        # 表示する図面
        docment = doc

        # 列名
        columns = ('owner', 'handle')  # 列名の指定

        return docment, columns, data


# テスト
if __name__ == '__main__':

    # ウィンドウ作成
    root = tk.Tk()
    root.title('Simple Viewer')
    root.geometry('{}x{}+200+200'.format(1600, 900))

    # フレーム作成
    viewer = SimpleViewer(master=root, error_to_console=True)

    # 実行
    root.mainloop()
