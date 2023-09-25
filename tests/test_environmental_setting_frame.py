# -*- coding: utf-8 -*-
"""EnvironmentalSettingFrameのテスト.

Created on Tue Sep 19 15:00:57 2023.
@author: Yuta Kuronuma
"""

import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

import tkinter as tk

from frames.viewer_conf import ViewerConf
from frames.environmental_setting_frame import EnvironmentalSettingFrame


if __name__ == '__main__':

    root = tk.Tk()
    root.title('ESF Test')
    root.geometry('{}x{}+200+200'.format(500, 100))
    vc = ViewerConf(initialize_conf=True)

    esf = EnvironmentalSettingFrame(root, vc)
    esf.pack()

    root.mainloop()