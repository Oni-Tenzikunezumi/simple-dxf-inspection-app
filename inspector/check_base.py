# -*- coding: utf-8 -*-
"""検図アルゴリズムのベースクラスモジュール.

Created on Tue Oct 31 14:44:32 2023.
@author: Yuta Kuronuma
"""

import ezdxf
from typing import Any
from ezdxf.document import Drawing
from .check_result import CheckResult
from .draw_tool import DrawTool


class CheckBase:
    """検図アルゴリズムのベースクラス."""

    # 検図項目の名前
    inspect_name: str = '動作テスト'

    # 処理内容の説明
    inspect_str: str = 'ベースクラスが表示されています.'
    
    @staticmethod
    def inspect_doc(doc: Drawing, draw_doc: Drawing, **Option: dict[str, Any]):
        """図面docを検図し，図面draw_docに検図結果を描画し，
        結果として draw_doc と CheckResult のリストを返す

        Parameters
        ----------
        doc : Drawing
            検図を行うオリジナル図面.
        draw_doc: Drawing
            結果を描画するための図面
        **Option: dict[str, Any]
            枠線等の追加情報.

        Returns
        -------
            描画した draw_doc
            検図結果の CheckResult のリスト

        """
        # 何か処理
        data = [ent.dxfattribs() for ent in doc.query('LINE')]

        # 図面描画
        if len(data) > 0:
            p1, p2 = data[0]['start'], data[0]['end']
            DrawTool.Arrow(draw_doc, head=p1, tail=p2, color=1)

        # 結果
        results = []
        if len(data) > 0:
            p1, p2 = data[0]['start'], data[0]['end']
            pos = ( (p1[0]+p2[0])/2, (p1[1]+p2[1])/2 )
            check_type = CheckBase.inspect_name
            res1 = CheckResult( check_type, error=True, pos=pos, caption='検査', desc='線です')
            results.append(res1)

        return draw_doc, results
