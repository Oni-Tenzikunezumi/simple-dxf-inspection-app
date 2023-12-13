# -*- coding: utf-8 -*-
"""
各チェックが返す結果のクラス

Created on Tue Dec 12 20:03:30 2023

@author: shingo
"""

class CheckResult:

    columns = ('検査項目', 'エラー', '位置', '見出し', '説明', '色')
    
    def __init__(self, checkType:str, error: bool, pos=None, caption:str = '', desc : str = '', color=7 ):
        '''
        チェックした結果クラスのコンストラクタ

        Parameters
        ----------
        checkType : str
            検査項目
        error : bool
            結果が失敗の内容か
        pos : TYPE
            結果に関する位置(x,y) ．指定しない場合は None． The default is None.
        caption : str
            描画に記述する弥陀s（descの簡易説明)
        desc : str
            結果の詳しい説明. The default is ''.
        color : TYPE
            描画する時の基本色. The default is 7 (black).
        '''
        self.checkType = checkType
        self.error = error
        self.pos = pos
        self.caption = caption
        self.desc = desc
        self.color = color
        
    def toColumnData(self):
        '''
        コラム内容の辞書を返す
        '''
        ret = {
            CheckResult.columns[0] : self.checkType,
            CheckResult.columns[1] : self.error,
            CheckResult.columns[2] : self.pos,
            CheckResult.columns[3] : self.caption,
            CheckResult.columns[4] : self.desc,
            CheckResult.columns[5] : self.color
        }
        return ret
        