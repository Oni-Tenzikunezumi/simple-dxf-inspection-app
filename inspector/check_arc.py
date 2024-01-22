# -*- coding: utf-8 -*-
"""円弧抽出テスト.

Created on Tue Nov  7 15:42:23 2023.
@author: Yuta Kuronuma
"""
import math
from math import sin, cos
from ezdxf.document import Drawing
from typing import Any
from .check_base import CheckBase
from .draw_tool import DrawTool
from .check_result import CheckResult


class CheckArc(CheckBase):
    """円弧抽出テスト."""

    # 検図項目の名前
    inspect_name: str = '円弧抽出'

    # 処理内容の説明
    inspect_str: str = '図面上の全ての円弧を抽出し，表示します.'

    @staticmethod
    def inspect_doc(doc: Drawing, draw_doc: Drawing, **Option: dict[str, Any]):
        """円弧抽出."""
        
        color = 84 # 濃いめの緑
        
        
        # 図面の処理
        data = [ent.dxfattribs() for ent in doc.modelspace().query('ARC')]

        # 図面描画
        for d in data:
            c = d['center']
            r = d['radius']
            st = d['start_angle']
            ed = d['end_angle']
            DrawTool.Arc( draw_doc, c, r, st, ed, color=color, width=1 )
            
        # 結果
        results = []
        num = 1
        for d in data:
            c = d['center']
            r = d['radius']
            st = d['start_angle']
            ed = d['end_angle']
            mid = (st+ed)/2 if st<ed else (st+ed+360)/2
            mid *= math.pi/180
            res = CheckResult(
                num = num,
                checkType = CheckArc.inspect_name,
                error=False,
                pos=(c[0]+r*cos(mid), c[1]+r*sin(mid)),
                caption='円弧です',
                desc='center: {0}, radius: {1}'.format( c, r ),
                color = color
                )
            results.append(res)
            num+=1
            
        # 矢印なし結果
        for i in range(2):
            res = CheckResult(
                num = num,
                checkType = CheckArc.inspect_name,
                error=False,
                pos=None,
                caption='円弧検出サンプル',
                desc='円弧検出サンプルの結果になります',
                color = color
                )
            results.append(res)
            num += 1

        return draw_doc, results
