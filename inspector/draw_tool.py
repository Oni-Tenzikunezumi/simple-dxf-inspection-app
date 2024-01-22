# -*- coding: utf-8 -*-
"""
Created on Fri Dec  8 17:27:49 2023

@author: Shingo Nakamura

ezdxf の doc に描画するための Toolクラス
"""

import ezdxf
import math
from math import sin, cos
import io
from ezdxf.document import Drawing
from ezdxf.entities import MText, Text

class DrawTool:
    
    DefaultLayer = "inspection"
    
    @staticmethod
    def Rectangle( doc: Drawing, p1, p2, color, width=1, layer=None):
        '''
        四角形を描画
        中は塗りつぶさない
        '''
        # 画層
        if layer is None:
            layer = DrawTool.DefaultLayer
        
        # 座標
        xmin = min( p1[0], p2[0] )
        xmax = max( p1[0], p2[0] )
        ymin = min( p1[1], p2[1] )
        ymax = max( p1[1], p2[1] )
        points = [ (xmin, ymax), (xmax, ymax), (xmax, ymin), (xmin, ymin)]
        
        msp = doc.modelspace()
        att = {'layer': layer, 'color' : color, 'linetype' : 'Continuous','const_width' : width}
        msp.add_lwpolyline( points, format='xy', close=True, dxfattribs= att)
        
    @staticmethod        
    def Line( doc: Drawing, p1, p2, color, width=1, layer=None):
        '''
        直線を描画
        '''
        # 画層
        if layer is None:
            layer = DrawTool.DefaultLayer
            
            
        msp = doc.modelspace()
        att = {'layer': layer, 'color' : color, 'linetype' : 'Continuous','const_width' : width}
        msp.add_lwpolyline( (p1, p2), format='xy', close=False, dxfattribs=att)
            
        
    @staticmethod
    def Arrow( doc: Drawing, head, tail, color, head_size=5, line_width=1, layer=None):
        '''
        矢印を描画
        '''
        
        # 画層
        if layer is None:
            layer = DrawTool.DefaultLayer

        # 線の角度を求める
        dx = tail[0] - head[0]
        dy = tail[1] - head[1]
        angle = math.atan2(dy, dx)
        
        # ヘッドの座標
        y = math.sin(math.pi * 20/180) # sin(20deg)
        points = [ (0,0), ( head_size, head_size*y), ( head_size, -head_size*y) ]
        
        # ヘッド座標変換
        sina = math.sin(angle)
        cosa = math.cos(angle)
        trans = lambda p : (p[0]*cosa-p[1]*sina + head[0], p[0]*sina+p[1]*cosa + head[1])
        points = list( map( trans, points ) )
        
        # ヘッド部分の描画
        msp = doc.modelspace()
        hatch = msp.add_hatch(color=color)
        hatch.paths.add_polyline_path( points, is_closed=True)
        
        # 線部分の描画
        p = ( (points[1][0]+points[2][0])/2, (points[1][1]+points[2][1])/2 )
        DrawTool.Line(doc, p, tail, color=color, width=line_width, layer=layer)
        
    @staticmethod
    def Circle( doc: Drawing, cent, radius, color, width=1, layer=None ):
        '''
        円を描画
        '''
        
        # 画層
        if layer is None:
            layer = DrawTool.DefaultLayer
        
        # LWPolyLineで描く（ add_circle だと太さの変更が難しいため)
        n = 24
        pts = []
        for i in range(n):
            p = ( cent[0]+radius * cos(2*math.pi*i/n), cent[1]+radius * sin(2*math.pi*i/n) )
            pts.append(p)
            
        
        msp = doc.modelspace()
        att = {'layer': layer, 'color' : color, 'linetype' : 'Continuous','const_width' : width}
        msp.add_lwpolyline( pts, format='xy', close=True, dxfattribs=att)
        
    def Arc( doc: Drawing, cent, radius, stdeg, eddeg, color, width=1, layer=None ):
        '''
        円弧を描画
        '''
        
        # 画層
        if layer is None:
            layer = DrawTool.DefaultLayer
        
        # degree -> rad
        if eddeg < stdeg:
            eddeg += 360
        st = stdeg * math.pi / 180
        ed = eddeg * math.pi / 180
        ag = ed - st
        
        # LWPolyLine
        n = int(ag / math.pi * 12) + 1  # 180度で12辺程度
        pts = []
        for i in range(n+1):
            theta = st+i*ag/n
            p = ( cent[0]+radius*cos(theta), cent[1]+radius*sin(theta))
            pts.append(p)
            
        msp = doc.modelspace()
        att = {'layer': layer, 'color' : color, 'linetype' : 'Continuous','const_width' : width}
        msp.add_lwpolyline( pts, format='xy', close=False, dxfattribs=att)

    @staticmethod
    def Text( doc: Drawing, txt, pos, color, height=15, layer=None ):
        '''
        テキストを描画 
        '''
        
        # 画層
        if layer is None:
            layer = DrawTool.DefaultLayer

        # matplotlib で表示させるために、ms-gothic 追加
        doc.styles.add("MS Gothic", font="msgothic.ttc")

        msp = doc.modelspace()
        att = {'layer': layer, 'style': 'MS Gothic','height':height, 'color':color }
        msp.add_text( txt, dxfattribs=att ).set_placement(pos)

        
    @staticmethod
    def CopyDoc( doc: Drawing ) -> Drawing:
        '''
        製図ドキュメントのコピーを作成
        '''
        stream = io.StringIO()
        doc.write( stream )
        stream.seek(0)
        newdoc = ezdxf.read( stream )
        stream.close()
        return newdoc
    
    @staticmethod
    def ResolveFont( doc : Drawing ) -> Drawing:
        '''
        matplotlib で表示できないフォントを表示できるものに変更する
        '''
        # style 中の iso.shx フォント
        for s in doc.styles:
            s.dxf.font = s.dxf.font.replace( 'iso.shx', 'isocp')
            
        # MS PGothic
        for e in doc.entities:
            if type(e) is MText or type(e) is Text:
                e.text = e.text.replace( 'MS PGothic', 'MS Gothic' )
                
        return doc
        
        
# テスト
if __name__ == '__main__':
    from ezdxf.addons.drawing import RenderContext, Frontend
    import matplotlib.pyplot as plt
    from ezdxf.addons.drawing.matplotlib import MatplotlibBackend
    from pprint import pprint
    ezdxf.addons.drawing.properties.MODEL_SPACE_BG_COLOR = "#222222"


    doc = ezdxf.new("R2018", setup=True)
    
    DrawTool.Rectangle(doc, (0,0), (400,300), color= 2, width=1)
    DrawTool.Line(doc, (0,0), (200, 100), color=3, width=4 )
    DrawTool.Text(doc, "テスト", (0,0), color=1, height=14 )
    DrawTool.Arrow(doc, (0,300), (200, 250), color=4, head_size=10, line_width=1 )
    DrawTool.Circle(doc, ( 150, 150 ), 20, color=1, width=0.5 )

    aaa = DrawTool.CopyDoc(doc)
    msp = doc.modelspace()
    
    fig = plt.figure()
    ax = fig.add_axes([0,0,20,20])
    ctx = RenderContext(doc)
    out = MatplotlibBackend(ax)
    Frontend(ctx, out).draw_layout(msp, finalize=True)
