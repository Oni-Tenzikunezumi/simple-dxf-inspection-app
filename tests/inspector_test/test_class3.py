# -*- coding: utf-8 -*-
"""テスト用サブクラス.

Created on Mon Nov  6 02:24:36 2023.
@author: Yuta Kuronuma
"""

from inspector.check_base import CheckBase


class TestClass3(CheckBase):
    """3番目."""

    inspect_name: str = 'テスト3番'
    inspect_str: str = '3番目テストクラス'

    @staticmethod
    def inspect_doc():
        """テスト関数."""
        print('実行（3番目）')
