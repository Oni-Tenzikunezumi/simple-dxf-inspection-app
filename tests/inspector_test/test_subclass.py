# -*- coding: utf-8 -*-
"""テスト用サブクラス.

Created on Mon Nov  6 02:24:36 2023.
@author: Yuta Kuronuma
"""

from tests.inspector_test.test_class import TestBase


class TestClass1(TestBase):
    """1番目."""

    inspect_name: str = 'テスト1番'
    inspect_str: str = '1番目テストクラス'

    @staticmethod
    def inspect_doc():
        """テスト関数."""
        print('実行（1番目）')


class TestClass2(TestBase):
    """2番目."""

    inspect_name: str = 'テスト2番'
    inspect_str: str = '2番目テストクラス'

    @staticmethod
    def inspect_doc():
        """テスト関数."""
        print('実行（2番目）')


class TestClass3(TestBase):
    """3番目."""

    inspect_name: str = 'テスト3番'
    inspect_str: str = '3番目テストクラス'

    @staticmethod
    def inspect_doc():
        """テスト関数."""
        print('実行（3番目）')
