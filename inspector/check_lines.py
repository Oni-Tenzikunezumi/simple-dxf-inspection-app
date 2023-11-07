# -*- coding: utf-8 -*-
"""直線抽出テスト.

Created on Tue Nov  7 15:44:49 2023.
@author: Yuta Kuronuma
"""

import ezdxf
from typing import Any
from .check_base import CheckBase


class CheckLines(CheckBase):
    """検図アルゴリズムのベースクラス."""

    # 検図項目の名前
    inspect_name: str = '直線抽出'

    # 処理内容の説明
    inspect_str: str = '図面上の全ての直線を抽出し，表示します.'

    @staticmethod
    def inspect_doc(doc: ezdxf.document.Drawing, Option: tuple[Any] = None):
        """直線抽出."""
        # 図面の処理
        data = [ent.dxfattribs() for ent in doc.query('LINE')]

        # 表示する図面
        docment = doc

        # 列名
        columns = ('handle', 'start', 'end')  # 列名の指定

        return docment, columns, data
