# -*- coding: utf-8 -*-
"""help_windowのテストコード.

Created on Wed Nov  1 17:01:40 2023.
@author: Yuta Kuronuma
"""

import tkinter as tk

import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))
from frames.help_window import HelpWindow

root = tk.Tk()

root.title('Help Window Test')
root.geometry('{}x{}+200+200'.format(500, 500))

hw = HelpWindow(root)
hw.pack()

root.mainloop()
