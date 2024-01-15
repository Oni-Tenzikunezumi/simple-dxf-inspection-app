# -*- coding: utf-8 -*-
"""
Created on Fri Dec 22 18:53:03 2023

結果を集約して描画する SummarizeDrawer クラス

@author: shingo
"""

from ezdxf.document import Drawing
from .check_result import CheckResult
from .bounding_box import BoundingBox
from .draw_tool import DrawTool
from .non_cross_lines import NonCrossLines


class SummarizeDrawer:
    
    PAPER_SIZE = (420.0, 297.0)  # A3 Size (w, h)
    BASE_FONT_SIZE = 6
    BASE_LINE_SPACE = 14
    BASE_LINE_WIDTH = 0.8

    @classmethod
    def summarize( cls, doc: Drawing, results: list[CheckResult] ):
        
        cls.__drawdoc = doc
        cls.__bb = BoundingBox.DrawingBB(doc)
        cls.__sf = cls.__scale_factor(cls.__bb)
        cls.__font_size = cls.BASE_FONT_SIZE * cls.__sf
        cls.__line_space= cls.BASE_LINE_SPACE * cls.__sf
        cls.__line_width = cls.BASE_LINE_WIDTH * cls.__sf
        
        # リストをUpperとRight領域に分割
        up_rslts, rt_rslts, non_rslts = cls.__split_to_upper_right_non(cls.__bb, results)

        # 上側描画
        cls.__draw_upper_area( cls.__drawdoc, up_rslts )
        
        # 右側描画
        cls.__draw_right_area( cls.__drawdoc, rt_rslts)
        
        # 下側描画
        cls.__draw_bottom_area( cls.__drawdoc, non_rslts)


    @staticmethod
    def __split_to_upper_right_non( draw_bb, results: list[CheckResult]):
        l, b, r, t = draw_bb  # left, bottom, right, top
        center_x = (l+r)/2
        center_y = (b+t)/2
        
        
        upper, right, non = [], [], []
        for r in results:
            if r.pos is None:
                non.append(r)
            elif r.pos[0] < center_x and r.pos[1] > center_y:
                upper.append(r)
            else:
                right.append(r)
                
        return upper, right, non
        

    @classmethod
    def __draw_upper_area( cls, doc: Drawing, results:list[CheckResult], maxCount=None ):
        
        # 描画する数
        if maxCount is None:
            maxCount = len(results)
        count = min( maxCount, len(results) )
        if count == 0: return
        
        # 行間
        ls = cls.__line_space
        
        # 矢印線を引く
        lft, btm, rgt, top = cls.__bb
        st_x = (2*lft+3*rgt)/5.0
        tails = [ (st_x, top+(i+1)*ls ) for i in range(count) ]
        heads = [ results[i].pos for i in range(count) ]

        # 接続関係を求める
        idx = NonCrossLines.analyze(heads, tails)
        
        # 矢印&キャプション描画
        for i in range(count):
            caption = str(results[i].num) + '.' + results[i].caption
            DrawTool.Text(cls.__drawdoc, caption, tails[idx[i]], results[i].color, height=cls.__font_size)    
            DrawTool.Arrow(cls.__drawdoc, heads[i], tails[idx[i]], results[i].color, line_width=cls.__line_width)
            lineend = (tails[idx[i]][0] + len(caption)*cls.__font_size, tails[idx[i]][1] )
            DrawTool.Line(cls.__drawdoc, tails[idx[i]], lineend, results[i].color, width=cls.__line_width)
        

    @classmethod
    def __draw_right_area( cls, doc: Drawing, results:list[CheckResult], maxCount=None ):

        # 描画する数
        if maxCount is None:
            maxCount = len(results)
        count = min( maxCount, len(results) )
        if count == 0: return
        
        # 行間
        ls = cls.__line_space
        
        # 矢印線を引く
        lft, btm, rgt, top = cls.__bb
        st_x = rgt + ls
        tails = [ (st_x, top-(i+1)*ls ) for i in range(count) ]
        heads = [ results[i].pos for i in range(count) ]

        # 接続関係を求める
        idx = NonCrossLines.analyze(heads, tails)
        
        for i in range(count):
            caption = str(results[i].num) + '.' + results[i].caption
            DrawTool.Text(cls.__drawdoc, caption, tails[idx[i]], results[i].color, height=cls.__font_size)    
            DrawTool.Arrow(cls.__drawdoc, heads[i], tails[idx[i]], results[i].color, line_width=cls.__line_width)
            lineend = (tails[idx[i]][0] + len(caption)*cls.__font_size, tails[idx[i]][1] )
            DrawTool.Line(cls.__drawdoc, tails[idx[i]], lineend, results[i].color, width=cls.__line_width)


    @classmethod
    def __draw_bottom_area( cls, doc: Drawing, results:list[CheckResult], maxCount=None):

        # 描画する数
        if maxCount is None:
            maxCount = len(results)
        count = min( maxCount, len(results) )
        if count == 0: return
        
        # 行間
        ls = cls.__line_space
        
        # 描画
        lft, btm, rgt, top = cls.__bb
        st_x = lft
        pts = [ (st_x, btm - (i+1)*ls) for i in range(count)]
        for i in range(count):
            caption = str(results[i].num) + '.' + results[i].caption
            DrawTool.Text(cls.__drawdoc, caption, pts[i], results[i].color, height=cls.__font_size)


    @staticmethod
    def __scale_factor( doc_bb ):

        '''
        図面の矩形領域からスケールファクターを計算
        '''
        
        # 図面の矩形領域
        if doc_bb is None:
            return 1.0
        
        # スケールファクター計算
        lft, btm, rgt, top = doc_bb
        w, h = rgt - lft, top - btm
        paper_w, paper_h = SummarizeDrawer.PAPER_SIZE
        scale_factor = max( w/paper_w, h/paper_h )
        
        return scale_factor
    
