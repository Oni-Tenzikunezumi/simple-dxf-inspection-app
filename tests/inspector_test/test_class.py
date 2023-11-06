# -*- coding: utf-8 -*-
"""テスト用検図クラス.

Created on Mon Nov  6 02:19:26 2023.
@author: Yuta Kuronuma
"""


class TestBase:
    """テスト用クラス."""

    inspect_name: str = 'テストベース'
    inspect_str: str = 'テストのベース'

    @staticmethod
    def inspect_doc():
        """テスト関数."""
        print('実行（テスト用クラス）')
