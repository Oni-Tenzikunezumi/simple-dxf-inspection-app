# -*- coding: utf-8 -*-
"""円抽出テスト.

Created on Tue Nov  7 15:41:24 2023.
@author: Yuta Kuronuma
"""

from ezdxf.document import Drawing
from typing import Any
from .check_base import CheckBase
from .draw_tool import DrawTool
from .check_result import CheckResult


class CheckCircle(CheckBase):
    """円抽出テスト."""

    # 検図項目の名前
    inspect_name: str = '円抽出'

    # 処理内容の説明
    inspect_str: str = '図面上の全ての円を抽出し，表示します.\n'\
        '表示項目:handle, center, radius'

    @staticmethod
    def inspect_doc(doc: Drawing, draw_doc: Drawing, **Option: dict[str, Any]):
        """円抽出."""
        
        color = 1 # red
        
        # 図面の処理
        data = [ent.dxfattribs() for ent in doc.modelspace().query('CIRCLE')]

        # 図面描画
        for d in data:
            c = d['center']
            r = d['radius']
            DrawTool.Circle( draw_doc, c, r, color=color, width=1 )

        # 結果
        results = []
        num = 1
        rt2 = 1.41421 # root2
        for d in data:
            c = d['center']
            r = d['radius']
            res = CheckResult(
                num = num,
                checkType = CheckCircle.inspect_name,
                error=False,
                pos=(c[0]+r/rt2, c[1]+r/rt2),
                caption='円です',
                desc='center: {0}, radius: {1}'.format( c, r ),
                color = color
                )
            results.append(res)
            num += 1
            
        # 矢印なし結果
        for i in range(2):
            res = CheckResult(
                num = num,
                checkType = CheckCircle.inspect_name,
                error=False,
                pos=None,
                caption='円検出サンプル',
                desc='円検出サンプルの結果になります',
                color = color
                )
            results.append(res)
            num += 1

        return draw_doc, results
