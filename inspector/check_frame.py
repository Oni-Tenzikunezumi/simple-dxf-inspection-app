import ezdxf
import tkinter as tk

from ezdxf.document import Drawing
from typing import Any
from .check_base import CheckBase
from .frame_extractor import Frame_extractor_result as FrameResult
from .check_result import CheckResult
from .draw_tool import DrawTool

class CheckFrame(CheckBase):
    """枠線表示クラス"""

    # 検図項目の名前
    inspect_name: str = "輪郭線表示"

    # 処理内容の説明
    inspect_str: str = "図面上の輪郭線を強調する."
    
    @staticmethod
    def inspect_doc(doc: Drawing, draw_doc: Drawing, **Option: tuple[Any]):
        """枠線表示"""

        fresult: FrameResult = Option["frameresult"]

        # 結果
        results = []
        color = 1
        num = 1

        # 枠線が存在しない場合
        if len(fresult.framePoint) == 0:
            res = CheckResult(
                num = num,
                checkType = CheckFrame.inspect_name,
                error=True,
                pos=None,
                caption='輪郭線なし',
                desc=fresult.message,
                color=color
            )
            results.append(res)

            return draw_doc, results

        # 枠線は存在するがレイヤーがおかしい場合
        elif fresult.message == "枠線の構成するレイヤーがおかしいです":
            DrawTool.Rectangle(draw_doc, fresult.framePoint[0], fresult.framePoint[1], color, 1.5)

            res = CheckResult(
                num = num,
                checkType = CheckFrame.inspect_name,
                error = True,
                pos = None,
                caption='輪郭線のレイヤーがおかしい',
                desc = '輪郭線を構成するレイヤーが一つではありません',
                color = color
            )
            results.append(res)

            return draw_doc, results

        # 枠線が存在する場合
        DrawTool.Rectangle(draw_doc, fresult.framePoint[0], fresult.framePoint[1], color, 1.5)
        res = CheckResult(
            num = num,
            checkType = CheckFrame.inspect_name,
            error = False,
            pos = None,
            caption = '輪郭線が存在しました',
            desc = '輪郭線が存在しました',
            color = color
        )
        results.append(res)

        return draw_doc, results
    

