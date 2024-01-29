import ezdxf

from typing import Any
from ezdxf.document import Drawing
from inspector.check_base import CheckBase
from inspector.frame_extractor import Frame_extractor_result as FrameResult
from inspector.check_result import CheckResult
from inspector.check_outer_object import CheckOuterObject
from inspector.check_frame import CheckFrame
from inspector.check_titleblock import CheckTitleBlock
from inspector.check_outline_connectivity import CheckOutlineConnectivity


class CheckTotal(CheckBase):
    """すべての検図結果をまとめる"""

    # 検図項目の名前
    inspect_name: str = 'すべての検図'

    # 処理内容の説明
    inspect_str: str = 'すべての検図結果をまとめて表示します.'

    @staticmethod
    def inspect_doc(doc: Drawing, draw_doc: Drawing, **Option: dict[str, Any]):
        """すべての検図."""
        inspector_list = [CheckFrame, CheckTitleBlock, CheckOuterObject, CheckOutlineConnectivity]
        frame = Option['frameresult']
        res = []

        for inspector in inspector_list:
            draw_doc, results = inspector.inspect_doc(doc, draw_doc, frameresult = frame)
            for result in results:
                res.append(result)

        for i, r in enumerate(res):
            r.num = i + 1

        return draw_doc, res