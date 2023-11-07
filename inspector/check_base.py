# -*- coding: utf-8 -*-
"""検図アルゴリズムのベースクラスモジュール.

Created on Tue Oct 31 14:44:32 2023.
@author: Yuta Kuronuma
"""

import ezdxf
from typing import Any


class CheckBase:
    """検図アルゴリズムのベースクラス."""

    # 検図項目の名前
    inspect_name: str = '動作テスト'

    # 処理内容の説明
    inspect_str: str = 'ベースクラスが表示されています.'

    @staticmethod
    def inspect_doc(doc: ezdxf.document.Drawing, Option: tuple[Any] = None):
        """図面docを検図し，検図結果のlistと表にする際の列名を返す.

        Parameters
        ----------
        doc : ezdxf.document.Drawing
            検図を行う図面.
        Option : tuple[Any]
            枠線等の追加情報.

        Returns
        -------
            document : ezdxf.document.Drawing
                表示する図面のDrawing

            columns : list[str]
                表にする際の列名.
                列名は検図結果のdictに存在するkeyから選択する.
                表はlist内の順番で列が表示される.

            data : list[dict[str, any]]
                検図結果のリスト.
                key:value = 検図項目:内容

        """
        # 図面の処理
        data = [ent.dxfattribs() for ent in doc.query('LINE')]

        # 表示する図面
        docment = doc

        # 列名
        columns = ('owner', 'handle')  # 列名の指定

        return docment, columns, data
