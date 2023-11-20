# -*- coding: utf-8 -*-
"""円弧抽出テスト.

Created on Tue Nov  7 15:42:23 2023.
@author: Yuta Kuronuma
"""

import ezdxf
from typing import Any
from .check_base import CheckBase


class CheckArc(CheckBase):
    """円弧抽出テスト."""

    # 検図項目の名前
    inspect_name: str = '円弧抽出'

    # 処理内容の説明
    inspect_str: str = '図面上の全ての円弧を抽出し，表示します.'

    @staticmethod
    def inspect_doc(doc: ezdxf.document.Drawing, **Option: dict[str, Any]):
        """円弧抽出."""
        # 図面の処理
        data = [ent.dxfattribs() for ent in doc.query('ARC')]

        # 表示する図面
        docment = doc

        # 列名
        columns = ('handle', 'center', 'radius', 'start_angle', 'end_angle')  # 列名の指定

        return docment, columns, data
