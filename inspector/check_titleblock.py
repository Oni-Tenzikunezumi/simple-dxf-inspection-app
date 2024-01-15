# -*- coding: utf-8 -*-
"""
表題欄の検出/検図クラス.

Created on Fri Dec  7 15:44:13 2023.
@author: Shingo Nakamura

"""
from ezdxf.document import Drawing
from typing import Any
import types
from .check_base import CheckBase
from .draw_tool import DrawTool
from .check_result import CheckResult


class CheckTitleBlock(CheckBase):
    
    """ 表題欄の検出/検図 """
    
    # 検図項目の名前
    inspect_name: str = '表題欄の検出'

    # 処理内容の説明
    inspect_str: str = '表題欄が正しく書かれているか検図します'
    
    # 検査項目
    insepct_type: str = '表題欄'
    
    # 誤差しきい値
    __eps1 = 0.001  # この範囲内であれば接している
    __eps2 = 0.1    # この範囲内であれば接するつもりが接していない
    
    @staticmethod
    def inspect_doc(doc: Drawing, draw_doc, **Option: dict[str, Any]):
        
        cls = CheckTitleBlock
        color = 54
        results = []

        try:
            # 表題欄の領域を見つける. 
            frm = Option['frameresult'].framePoint
            tb_area = cls.__FindTitleBlockArea( doc, frm, cls.__eps1 )

            # 表題欄内の水平・垂直線を見つける．精度(eps)をゆるくした場合と違いがない確認．
            lines1 = cls.__ExtractLinesInTitleBlock(doc, tb_area, CheckTitleBlock.__eps1 )
            lines2 = cls.__ExtractLinesInTitleBlock(doc, tb_area, CheckTitleBlock.__eps2 )
            if len(lines1) < len(lines2) :
                error_lines = CheckTitleBlock.__ExtractErrorLines(lines1, lines2)
            else:
                error_lines = []
            
            # 表題欄位置の検出に成功
            raise SuccessTitleBlockDetection()
            
            
        # 表題欄位置の検出に成功した場合
        except SuccessTitleBlockDetection:
        
            # 表題欄を塗る
            cls.__DrawTitleBlock(draw_doc, tb_area, lines1, error_lines, color=color)
            
            # 検出成功結果登録
            checkType = cls.insepct_type
            error = False
            cap = '検出した表題欄'
            desc = '表題欄が検出されました'
            pos = (tb_area.right, (tb_area.top + tb_area.bottom) / 2 )
            results.append( CheckResult( len(results)+1, checkType, error, pos, cap, desc, color) )
            
            # 間違い線の結果登録
            for el in error_lines:
                error = True
                cap = '表題欄の罫線に誤りあり'
                desc = '罫線が正しく接続されていない'
                pos = CheckTitleBlock.MiddlePoint(el)
                results.append( CheckResult(len(results)+1, checkType, error, pos, cap, desc, color=1) )
            
            
        # 表題欄位置の検出に失敗した場合
        except (HorizontalLineNotFoundError,
                VerticalLineNotFoundError,
                TitleBlockNotFoundError ) as e :
            print( type(e).__name__,':', e )

            results = []            
            try:
                # 条件をゆるくしてもう一度表題欄を
                tb_area2 = cls.__FindTitleBlockArea( doc, frm, CheckTitleBlock.__eps2 )
                
                # 誤った表題欄の描画
                cls.__DrawTitleBlock(draw_doc, tb_area2, lines=[], error_lines=[], color=1, hatch=False)
                
                # 誤った表題欄の結果登録
                checkType = cls.inspect_type
                error = True
                cap = '表題欄に誤りあり'
                desc = '表題欄の枠が正しく描かれていない可能性があります．接続に気をつけてください．'
                pos = (tb_area2.right, (tb_area2.top+tb_area2.bottom)/2 )
                results.append( CheckResult(len(results)+1, checkType, error, pos, cap, desc, color=1 ) )

            # 条件をゆるくして表題欄検出しても失敗
            except Exception as e:
                print( type(e).__name__, ':', e )
                
                # 失敗の結果登録
                checkType = cls.insepct_type
                error = True
                cap = '表題欄なし'
                desc = '厳密な表題欄が見つかりませんでした．表題欄を確認してください．'
                pos = None
                results.append( CheckResult(len(results)+1, checkType, error, pos, cap, desc, color=1 ) )
        
        # それ以外のよくわからない失敗
        except Exception as e:
            print( type(e).__name__,':', e )
            # 失敗の結果登録
            checkType = cls.insepct_type
            error = True
            desc = '表題欄がありません'
            pos = None
            results.append( CheckResult(len(results)+1, checkType, error, pos, desc, color=1 ) )

        # 終了
        return draw_doc, results
        
    
    @classmethod
    def __FindTitleBlockArea( cls, doc, framePoint, eps ):
        
        """
        表題欄の位置を見つける
        """
        # 枠の各座標取得
        frm = types.SimpleNamespace()
        frm.l = min( framePoint[0][0], framePoint[1][0] )
        frm.r = max( framePoint[0][0], framePoint[1][0] )
        frm.t = max( framePoint[0][1], framePoint[1][1] )
        frm.b = min( framePoint[0][1], framePoint[1][1] )
        
        # 直線抽出
        lines = [ent.dxfattribs() for ent in doc.modelspace().query('LINE')]
        
        # 枠の右に接する水平線抽出(ついでに左端が start に変更され、上から順になっている)
        h_lines = cls.__ExtractRightTouchHorizontalLine(frm, lines, eps)

        # 枠の下に接する垂直線抽出(ついでに上端が start に変更、)
        v_lines = cls.__ExtractBottomTouchVerticalLine(frm, lines, eps )

        # 表題欄の左上の座標を見つける
        try:
            x, y = cls.__FindTopLeftCorner(h_lines, v_lines, eps)
        except TopLeftCornerNotFoundError as e:
            print( e.__name__, ':',  e )
            msg = 'Title Block is not found'
            raise TitleBlockNotFoundError( msg )

        # 成功処理
        titleblock = types.SimpleNamespace()
        titleblock.top = y
        titleblock.left = x
        titleblock.bottom = frm.b
        titleblock.right = frm.r
        return titleblock
        
    
    @staticmethod
    def __ExtractRightTouchHorizontalLine( frm, lines, eps ):

        """
        線群から枠の右側に接している水平線を抽出する
        ついでに左端を start に統一し、
        連結できる水平線は連結し、
        上から順番に並び替える
        """
        # 枠内の水平線を抽出
        c1 = lambda l: abs(l['start'][1] - l['end'][1]) < eps  # 水平線
        c2 = lambda l: (l['start'][1] < frm.t and l['start'][1] > frm.b ) # 枠内
        c12 = lambda l: c1(l) and c2(l)
        lines = list( filter( c12, lines ) )
        if len(lines) == 0 :
            msg = 'Any horizontal line for title block is not found.'
            raise HorizontalLineNotFoundError( msg )

        # 水平線の左端点を start にする
        def make_left_start( hline ):
            if hline['start'][0] > hline['end'][0]:
                p = hline['start']
                hline['start'] = hline['end']
                hline['end'] = p
            return hline
        lines = list(map( make_left_start, lines ) )
        
        # 1：y 降順, 2：x昇順でソート
        lines = sorted( lines, key = lambda l : (-l['start'][1], l['start'][0]) )
        
        # 水平線が繋がっていたら１つにまとめる
        new_lines = []
        line = lines[0]
        i = 1
        
        while i < len(lines):
            y = line['start'][1]
            x = line['end'][0]
            
            # 繋がっていたら結合した水平線を作成
            if abs(lines[i]['start'][1]-y) < eps and lines[i]['start'][0] < x+eps :
                st = line['start']
                ed = (max( line['end'][0], lines[i]['end'][0]), y )
                line = { 'start' :st, 'end' : ed }
            # 繋がっていなければ次へ
            else:
                new_lines.append(line)
                line = lines[i]
            i+=1
            
        else:
            new_lines.append(line)
            
        # 枠の右に接しているものを抽出
        c3 = lambda l: abs(l['end'][0] - frm.r ) < eps # 右接地
        touch_lines = list(filter( c3, new_lines ))
        if len(touch_lines) == 0 :
            msg = 'Any horizontal line touching to frame right for title block is not found.'
            raise HorizontalLineNotFoundError( msg )
        
        # 枠の右側に接している水平線
        return touch_lines
        

    @staticmethod
    def __ExtractBottomTouchVerticalLine( frm, lines, eps ):
        
        """
        線群から枠の下側に接している鉛直線を抽出する
        ついでに上端を start に統一
        """
        # 枠内の鉛直線を抽出
        c1 = lambda l: abs(l['start'][0] - l['end'][0]) < eps  # 鉛直線
        c2 = lambda l: (l['start'][0] < frm.r-eps and l['start'][0] > frm.l+eps) # 枠内
        c12 = lambda l: c1(l) and c2(l)
        lines = list( filter( c12, lines ) )
        if len(lines) == 0 :
            msg = 'Any vertical line for title block is not found.'
            raise VerticalLineNotFoundError( msg )

        # 鉛直線の上が start になるようにする
        def make_top_start( vline ):
            if vline['start'][1] < vline['end'][1]:
                p = vline['start']
                vline['start'] = vline['end']
                vline['end'] = p
            return vline
        lines = list(map( make_top_start, lines ) )
        
        # 1：x 降順, 2：y 降順でソート
        lines = sorted( lines, key = lambda l : (l['start'][0], -l['start'][1]) )

        # 鉛直線が繋がっていたら１つにまとめる
        new_lines = []
        line = lines[0]
        i = 1
        while i < len(lines):
            x = line['start'][0]
            y = line['end'][1]
            
            # 繋がっていたら結合した水平線を作成
            if abs(lines[i]['start'][0]-x) < eps and lines[i]['start'][1] > y-eps :
                st = line['start']
                ed = (x, min( line['end'][1], lines[i]['end'][1]) )
                line = { 'start' :st, 'end' : ed }
            # 繋がっていなければ次へ
            else:
                new_lines.append(line)
                line = lines[i]
            i+=1
            
        else:
            new_lines.append(line)

        # 枠の下に接している鉛直線を抽出
        c3 = lambda l: abs(l['end'][1] - frm.b ) < eps # 下に接地
        touch_lines = list(filter( c3, new_lines ))
        
        # 枠の下側に接している鉛直線
        return touch_lines

    @staticmethod
    def __ExtractLinesInTitleBlock( doc, titleblock_area, eps ):
        
        """
        表題欄内に含まれるすべての水平・垂直線を見つける
        """
        # 表題欄の領域
        top = titleblock_area.top
        btm = titleblock_area.bottom
        rgt = titleblock_area.right
        lft = titleblock_area.left

        # 水平、垂直で枠内の直線を抽出
        c1 = lambda l: abs(l['start'][1] - l['end'][1]) < eps  # 水平線
        c2 = lambda l: abs(l['start'][0] - l['end'][0]) < eps  # 垂直線
        c3 = lambda l: abs(lft-eps < l['start'][0] < rgt+eps ) # 開始点の x 座標
        c4 = lambda l: abs(btm-eps < l['start'][1] < top+eps ) # 開始点の y 座標
        c5 = lambda l: abs(lft-eps < l['end'][0] < rgt+eps )   # 終了点の x 座標
        c6 = lambda l: abs(btm-eps < l['end'][1] < top+eps )   # 終了点の y 座標
        cond = lambda l: (c1(l) or c2(l)) and (c3(l) and c4(l) and c5(l) and c6(l) )
        lines = [ent.dxfattribs() for ent in doc.modelspace().query('LINE')]
        lines = list(filter( cond, lines ))
        
        # 表題欄枠に繋がっている線だけを抽出（主に第三角法の中の直線を排除するため）
        lines = CheckTitleBlock.__ExtractTitleBlockLines( titleblock_area, lines, eps)
        
        # 終了
        return lines
    
    
    @classmethod
    def __ExtractTitleBlockLines( cls, titleblock_area, lines, eps ):
        
        """
        表題欄の罫線の候補から、表題欄の罫線だけを取り出す
        具体的には表題欄の外枠に接続する線だけ抽出する
        
        bt_lines の直線に接する lines の直線を bt_lines に移していく
        """

        # 表題欄の領域
        top = titleblock_area.top
        btm = titleblock_area.bottom
        rgt = titleblock_area.right
        lft = titleblock_area.left

        # 表題欄罫線
        bt_lines = [{'start':(lft,top), 'end':(rgt,top)}, # top line
                    {'start':(rgt,top), 'end':(rgt,btm)}, # right line
                    {'start':(rgt,btm), 'end':(lft,btm)}, # bottom line
                    {'start':(lft,btm), 'end':(lft,top)}, # left line
                    ]
        
        # 線の移動がなくなるまで続ける
        lines1 = lines    # 最初の比較線1
        lines2 = bt_lines # 最初の比較線2
        
        while True:
            
            nxt_lines1 = []   # 次の比較線1
            nxt_lines2 = []   # 次の比較線2
            for l1 in lines1:
                for l2 in lines2:
                    if cls.__IsContact( l1, l2, eps ):
                        nxt_lines2.append(l1)
                        break
                else:
                    nxt_lines1.append(l1)
                        
            # 次に比較する候補がなくなったら終了            
            if len(nxt_lines2) == 0:
                break
            
            # 新しい罫線を追加
            bt_lines.extend(nxt_lines2)
 
            # 次のループの準備
            lines1 = nxt_lines1
            lines2 = nxt_lines2
            
            
        # 見つかった罫線を返す．最初の４つ（枠線）は除く．
        return bt_lines[4:]
    
    
    @staticmethod
    def __IsContact( l1, l2, eps ):

        """
        ２つの直線が接する関係か返す( T, L の関係)
        交わる場合は該当しない( + は該当しない)
        """
        lines = ( l1, l2 )
        ls = []
        for l in lines:
            _l = types.SimpleNamespace()
            _l.xmin = min( l['start'][0], l['end'][0])
            _l.xmax = max( l['start'][0], l['end'][0])
            _l.ymin = min( l['start'][1], l['end'][1])
            _l.ymax = max( l['start'][1], l['end'][1])
            _l.dx = _l.xmax - _l.xmin
            _l.dy = _l.ymax - _l.ymin
            ls.append( _l )
        

        # 垂直関係かチェック
        if abs( ls[0].dx*ls[1].dx + ls[0].dy*ls[1].dy ) > eps:
            return False
        
        # 水平線と鉛直線の見定め
        if abs(ls[0].dx) < eps:
            vline, hline = ls[0], ls[1]
        else:
            hline, vline = ls[0], ls[1]
            
        # 鉛直線上に水平線の端点が付いている
        if (abs(hline.xmin-vline.xmax) < eps or abs(hline.xmax-vline.xmax) < eps) \
            and ( vline.ymin-eps < hline.ymin < vline.ymax+eps ):
                return True
        
        # 水平線上に鉛直線の端点が付いている
        elif (abs(vline.ymin-hline.ymin) < eps or abs(vline.ymax-hline.ymin) < eps) \
            and ( hline.xmin-eps < vline.xmin < hline.xmax+eps ):
                return True
            
        # そのほか
        else:
            return False
        
    @classmethod
    def __FindTopLeftCorner( cls, hlines, vlines, eps ):
        
        '''
        水平線群と鉛直線群から、左上角をなす２直線をもとめ、その座標を返す
        失敗した場合は、
        '''
        
        # 角をなす二直線を見つける
        i, j = 0, 0
        while True:
            hline, vline = hlines[i], vlines[j]

            # 正しく見つかった
            if cls.__IsSamePoint(hline['start'], vline['start'], eps ):
                x = hline['start'][0]
                y = hline['start'][1]
                return (x, y)
            
            # 水平線が上に離れている
            elif hline['start'][1] > vline['start'][1]:
                i+=1

            # 鉛直線が左に離れている
            elif vline['start'][0] < hline['start'][0]:
                j+=1
            
            # 鉛直線と水平線がクロスしている
            else:
                i+=1; j+=1
            
            # 角が見つからない
            if i >= len(hlines) or j >= len(vlines):
                msg = "The top-left corner of title-block was not found!"
                raise TopLeftCornerNotFoundError(msg)
            
            
            
    @staticmethod
    def __IsSamePoint( p1, p2, eps ):
        """
        点p1と点p2が同じ座標かチェックする
        """
        if abs(p1[0]-p2[0]) < eps and abs(p1[1]-p2[1]) < eps:
            return True
        else:
            return False

    @classmethod
    def __ExtractErrorLines( cls, lines1, lines2 ):
        
        '''
        lines2 にあって lines1 にない線を返す
        '''
        
        eps = cls.__eps1
        
        error_lines = []
        for l2 in lines2:
            for l1 in lines1:
                if cls.__IsSamePoint(l1['start'], l2['start'], eps) \
                    and cls.__IsSamePoint(l1['end'], l2['end'], eps) \
                    or  cls.__IsSamePoint(l1['start'], l2['end'], eps) \
                    and  cls.__IsSamePoint(l1['end'], l2['start'], eps) :
                        break
            else:
                error_lines.append(l2)
                
        return error_lines
        
        
    
    @staticmethod
    def __DrawTitleBlock( doc, titleblock_area, lines, error_lines, color=1, error_color=1, width=1.2, hatch=True ):
        
        """
        表題欄の位置を強調して doc に描く
        （罫線を太く、領域にハッチング）
        """

        # 表題欄の領域
        top = titleblock_area.top
        btm = titleblock_area.bottom
        rgt = titleblock_area.right
        lft = titleblock_area.left
        
        # 表題欄の罫線
        for l in lines:
            x1 = l['start'][0]
            y1 = l['start'][1]
            x2 = l['end'][0]
            y2 = l['end'][1]
            DrawTool.Line( doc, (x1, y1), (x2,y2), color=color, width=width )

        # 表題欄の枠線
        DrawTool.Rectangle(doc, (lft,btm), (rgt, top), color=color, width=width)
        
        # 間違い線
        for el in error_lines:
            x1 = el['start'][0]
            y1 = el['start'][1]
            x2 = el['end'][0]
            y2 = el['end'][1]
            DrawTool.Line( doc, (x1, y1), (x2,y2), color=error_color, width=width )
        
        # ハッチング
        if hatch:
            msp = doc.modelspace()
            h = msp.add_hatch()
            points= [(lft, top, 0), (rgt, top, 0), (rgt, btm, 0), (lft, btm, 0)]
            if abs(lft) < 1.0e09 :
                h.paths.add_polyline_path(points,is_closed=True)
                h.set_pattern_fill( "ANSI31", scale=2, color=color)
        
        
    def MiddlePoint( line ):
        '''
        直線の中点を返す
        '''
        x = ( line['start'][0] + line['end'][0] ) / 2
        y = ( line['start'][1] + line['end'][1] ) / 2
        return ( x, y )
        

""" 例外クラス """
class TopLeftCornerNotFoundError( Exception ):
    pass

class TitleBlockNotFoundError( Exception ):
    pass

class HorizontalLineNotFoundError( Exception ):
    pass

class VerticalLineNotFoundError( Exception ):
    pass

class SuccessTitleBlockDetection( Exception ):
    pass

