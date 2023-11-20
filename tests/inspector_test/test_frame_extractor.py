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
from inspector.frame_extractor import Frame_extractor_result as FrameResult


class FrameExtractorTestClass(CheckBase):
    """frame_extractorのテストクラス."""

    inspect_name: str = '枠線抽出テスト'
    inspect_str: str = '枠線を抽出し，パラメータを表示します．'

    @staticmethod
    def inspect_doc(doc: ezdxf.document.Drawing, **Option: dict[str, Any]):
        """枠線を抽出し，詳細を表示."""

        fresult: FrameResult = Option['frameresult']

        print(fresult.framePoint)
        print(fresult.message)

        # 図面の処理
        data = FrameExtractorTestClass.__make_datalist(fresult)

        # 表示する図面
        docment = doc

        # 列名
        columns = ('No.', 'X', 'Y')  # 列名の指定

        return docment, columns, data

    @staticmethod
    def __make_datalist(fresult: FrameResult):
        """dataを作成する関数."""
        datalabel: list[str] = ['No.', 'X', 'Y']

        data = []
        for i, point in enumerate(fresult.framePoint):
            ddict = {}
            ddict[datalabel[0]] = i+1
            ddict[datalabel[1]] = point[0]
            ddict[datalabel[2]] = point[1]

            data.append(ddict)

        return data


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
