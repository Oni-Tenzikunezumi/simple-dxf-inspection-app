import ezdxf
import tkinter as tk

from typing import Any
from .check_base import CheckBase
from .frame_extractor import Frame_extractor_result as FrameResult
from .draw_tool import DrawTool

class CheckFrame(CheckBase):
    """枠線表示クラス"""

    # 検図項目の名前
    inspect_name: str = "枠線表示"

    # 処理内容の説明
    inspect_str: str = "図面上の枠線を強調する.\n"\
        "表示項目"
    
    @staticmethod
    def inspect_doc(doc: ezdxf.document.Drawing, **Option: tuple[Any]):
        """枠線表示"""

        fresult: FrameResult = Option["frameresult"]

        # 枠線が存在しない場合
        if len(fresult.framePoint) == 0:
            data = CheckFrame.__show_error(fresult)
            document = doc
            columns = ('error', 'reason')

            return document, columns, data
        
        # 枠線は存在するがレイヤーがおかしい場合
        elif fresult.message == "枠線の構成するレイヤーがおかしいです":
            DrawTool.Rectangle(doc, fresult.framePoint[0], fresult.framePoint[1], 1, 2)

            data = CheckFrame.__show_error(fresult)
            document = doc
            columns = ('error', 'reason')
            
            return document, columns, data


        DrawTool.Rectangle(doc, fresult.framePoint[0], fresult.framePoint[1], 1, 2)


        # 図面の処理
        data = []
        # 表示する図面
        document = doc

        # 列名
        columns = ('handle', 'center', 'radius')  # 列名の指定

        return document, columns, data
    

    @staticmethod
    def __show_error(fresult: FrameResult):
        """枠線が存在しなかった場合のエラーを表示"""
        datalabel: list[str] = ["error", "reason"]

        ddict = {}
        ddict[datalabel[0]] = "Not found frameline"
        ddict[datalabel[1]] = fresult.message

        return [ddict]


