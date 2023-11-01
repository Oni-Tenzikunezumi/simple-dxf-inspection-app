# -*- coding: utf-8 -*-
"""メニューバーのモジュール.

Created on Thu Sep 14 15:37:33 2023.
@author: Yuta Kuronuma
"""

import tkinter as tk

from frames.environmental_setting_frame import EnvironmentalSettingFrame
from frames.viewer_conf import ViewerConf
from frames.footer import Footer
from frames.help_window import HelpWindow


class SimpleViewMenu():
    """メニューバーを追加する."""

    def __init__(self, master: tk.Tk,
                 viewer_conf: ViewerConf,
                 footer: Footer = None):

        self.master = master
        self.viewer_conf = viewer_conf
        self.fot = footer

        # メニューバー
        self.menubar = tk.Menu()
        self.master.config(menu=self.menubar)

        # 設定メニューの作成
        setting = tk.Menu(self.menubar, tearoff=False)
        setting.add_command(label='環境設定', command=self.env_setting)
        setting.add_command(label='終了', command=self.quit_app)

        # 表示メニューの作成
        view = tk.Menu(self.menubar, tearoff=False)
        view.add_checkbutton(label='最前面表示', command=self.fix_front)
        view.add_command(label='ウィンドウ最大化', command=lambda:
                         self.master.state('zoomed'))

        # サイズメニューの作成
        self.size_menu = tk.Menu(view, tearoff=False)
        self.add_size_command()
        view.add_cascade(label='サイズ変更', menu=self.size_menu)

        # メニューバーへ追加
        self.menubar.add_cascade(label='設定', menu=setting)
        self.menubar.add_cascade(label='表示', menu=view)
        self.menubar.add_command(label='使用方法', command=self.display_help)

    def quit_app(self):
        """終了用関数."""
        self.master.quit()
        self.master.destroy()
        print('Quit')

    def fix_front(self):
        """最前面表示."""
        a = not self.master.attributes('-topmost')
        self.master.attributes('-topmost', a)

    def env_setting(self):
        """環境設定."""
        env_modal = tk.Toplevel(self.master)
        env_modal.title("環境設定")

        # モーダル設定
        env_modal.grab_set()        # モーダルにする(操作が終わるまで固定)
        env_modal.focus_set()       # フォーカスを新しいウィンドウをへ移す
        env_modal.transient(self.master)   # タスクバーに表示しない

        env_set = EnvironmentalSettingFrame(env_modal, self.viewer_conf)
        env_set.pack()

        # ダイアログが閉じられるまで待つ
        self.master.wait_window(env_modal)

        if self.fot is not None:
            self.fot.update_footer()
        print("環境設定終了．")

    def add_size_command(self):
        """サイズ変更用の選択肢を追加する."""
        size_opt = ['800x450', '960x540', '1280x720', '1600x900',
                    '1920x1080', '2560×1440', '3200x1800', '3840x2160']
        # w = self.master.winfo_screenwidth()
        # h = self.master.winfo_screenheight()
        # screen_size = '{}x{}'.format(w, h)

        for size in size_opt:
            self.size_menu.add_command(label=size, command=lambda s=size:
                                       self.set_winsize(s))

    def set_winsize(self, size):
        """ウィンドウサイズを変更する."""
        self.master.state('normal')
        self.master.geometry(size)
        self.master.update()

    def display_help(self):
        """ヘルプウィンドウの表示."""
        help_frame = tk.Toplevel(self.master, name='howto')
        help_frame.title("使用方法")
        geo_info = list(map(int, self.master.geometry().split('+')[1:3]))
        display_position = '+{}+{}'.format(geo_info[0]-20, geo_info[1]-20)
        help_frame.geometry(display_position)

        # モーダル設定
        help_frame.focus_set()       # フォーカスを新しいウィンドウをへ移す
        help_frame.transient(self.master)   # タスクバーに表示しない

        help_winow = HelpWindow(help_frame)
        help_winow.pack()

        # ダイアログが閉じられるまで待つ
        self.master.wait_window(help_winow)

        if self.fot is not None:
            self.fot.update_footer()
        print("使用方法終了.")
