# -*- coding: utf-8 -*-
"""設定内容を.iniファイルとして保存するモジュール.

Created on Mon Sep 18 16:27:33 2023.
@author: Yuta Kuronuma
"""

import configparser as conf
import os

from ezdxf.addons import odafc as oda


class ViewerConf:
    """アプリの設定内容を保存するクラス."""

    dirpath = r'C:\ProgramFiles\SimpleInspector'
    confpath = dirpath + r'\conf.ini'
    oda_section = 'odapath'

    def __init__(self, confdir: str = None, initialize_conf: bool = False):
        """イニシャライザイ."""
        if confdir is not None:
            self.dirpath = confdir
        # 設定ファイルの存在確認
        if not os.path.isfile(self.confpath) or initialize_conf:
            # 存在しない場合初期設定のファイルを作成
            self.create_conf()

        # .iniの読み込み
        self.conf_file = conf.ConfigParser()
        self.conf_file.read(self.confpath, encoding='utf_8')

    def create_conf(self):
        """初期設定のconfファイルを作成する."""
        # configの作成
        config = conf.RawConfigParser()

        # 初期設定の入力
        config.add_section(self.oda_section)
        path = r'C:\Program Files\ODA\ODAFileConverter\ODAFileConverter.exe'
        config.set(self.oda_section, 'defa', path)

        # ファイル，ディレクトリの作成
        os.makedirs(self.dirpath, exist_ok=True)

        with open(self.confpath, 'w', encoding='utf_8') as file:
            config.write(file)

    def save_conf(self):
        """設定の保存."""
        with open(self.confpath, 'w', encoding='utf_8') as file:
            self.conf_file.write(file)

    def get_odapath(self) -> str:
        """最後に設定されたodapathを返す."""
        items = self.conf_file.items(self.oda_section)
        # print('len', len(items))
        if len(items) == 0:
            return ''
        else:
            path = items[-1][1]
            return path

    def update_odapath(self, path):
        """odapathを更新する."""
        # items = self.conf_file.items(self.oda_section)
        self.conf_file.set(self.oda_section,
                           'opt0',
                           path)
        self.save_conf()

    def is_oda_path(self, oda_path: str) -> bool:
        """odaconverterのパスか確認する."""
        oda.win_exec_path = oda_path
        is_installed = oda.is_installed()

        # print('path:', oda.win_exec_path)
        # print(is_installed)

        if is_installed:
            try:
                dxfpath = r"D:\pythontext\prac_ezdzf\prac11dxf_exe\fffffff.dxf"
                _ = oda.readfile(dxfpath)
                # print(doc)

            except Exception as e:
                # 読み込めなければ無関係のパス
                is_installed = False
                oda.win_exec_path = ''
                print(e)

        return is_installed

    @property
    def is_oda_installed(self):
        """odaがインストールされているかを返す."""
        odapath = self.get_odapath()
        return self.is_oda_path(odapath)
