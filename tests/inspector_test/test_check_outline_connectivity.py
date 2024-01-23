
import ezdxf
from ezdxf.addons import odafc as oda
from ezdxf.document import Drawing
from ezdxf.addons.drawing import RenderContext, Frontend
from ezdxf.addons.drawing.matplotlib import MatplotlibBackend
from ezdxf.addons.drawing.properties import LayoutProperties

import matplotlib
import matplotlib.pyplot as plt
from pprint import pprint

import sys
import os.path as path
sys.path.append(path.join(path.dirname(__file__), '../..'))
from inspector.check_outline_connectivity import CheckOutlineConnectivity
from inspector.frame_extractor import Frame_extractor_result
from inspector.draw_tool import DrawTool
from inspector.summarize_drawer import SummarizeDrawer
import glob
import tkinter as tk
from simple_viewer import SimpleViewer


def main():
    # test1()
    # test2()
    test3()

def test1():
    
    '''
    特定のファイル 1 つを読み込み、処理をして結果をファイルに保存
    '''
    ezdxf.addons.drawing.properties.MODEL_SPACE_BG_COLOR = "#EEEEEE"
    oda.win_exec_path = "C:/Program Files/ODA/ODAFileConverter 24.11.0/ODAFileConverter.exe"
    
    # ファイル読み込み
    #filepath  = 'C:/Users/shingo/Desktop/0110_ねじ製図課題１検図後/AB22123_1_ねじ製図課題１.dwg'
    filepath  = 'C:/Users/shingo/Desktop/0110_ねじ製図課題２検図後/AB22010_1_Drawing8.dwg'
    #filepath  = 'C:/Users/shingo/Desktop/0110_ねじ製図課題１検図後/AB22155_1_Drawing12.dwg'
    doc = oda.readfile(filepath) # ODA あり
    #doc = ezdxf.readfile(file_path)
    
    # フレーム検出
    fr = Frame_extractor_result(doc)
    
    # 処理
    #CheckTitleBlock.inspect_doc( doc, frameresult = fr )
    
    # フレーム描画
    fp = fr.framePoint
    top = max(fp[0][1], fp[1][1])
    btm = min(fp[0][1], fp[1][1])
    lft = min(fp[0][0], fp[1][0])
    rgt = max(fp[0][0], fp[1][0])
    msp = doc.modelspace()
    points = ( (lft,top), (rgt,top), (rgt,btm), (lft,btm) )
    att = { 'color':1, 'const_width':2 }
    msp.add_lwpolyline(points,format='xy', close=True, dxfattribs=att)
    
    # matplotlib で描画    
    msp = doc.modelspace()
    fig = plt.figure(dpi=300 )
    ax = fig.add_axes([0,0,1,1])
    ctx = RenderContext(doc)
    msp_properties = LayoutProperties.from_layout(msp)
    #msp_properties.set_colors('#000000')
    ctx.set_current_layout(msp)
    out = MatplotlibBackend(ax)
    Frontend(ctx, out).draw_layout(msp, finalize=True, layout_properties=msp_properties)
    
    # png に保存
    #fig.savefig('C:/Users/shingo/Desktop/drawing.png', dpi=300)
    
def test2():
    
    '''
    特定のフォルダ内のdwgファイルを処理し、同じフォルダに画像(png)で保存
    '''
    # ODAの場所    
    oda.win_exec_path = "C:/Program Files/ODA/ODAFileConverter 24.11.0/ODAFileConverter.exe"

    # 描画の背景色
    ezdxf.addons.drawing.properties.MODEL_SPACE_BG_COLOR = "#EEEEEE"

    # フォルダ内の dwg ファイルを取得
    dir_path = 'D:/2023_Satsuka/cadData/1310_ねじ製図課題２/*.dwg'
    dwg_files = glob.glob(dir_path)

    # 保存のファイル名作成
    suffix = '_tb'
    png_files = []
    for f in dwg_files:
        name = path.splitext(f)[0] + suffix + '.png'
        png_files.append(name)
        
    # 実行
    for i, dwgfile in enumerate(dwg_files):
        
        # ファイル読み込み
        print( path.basename( dwgfile ) )
        doc = oda.readfile( dwgfile )
        
        # フレーム抽出
        fr = Frame_extractor_result(doc)
        
        # 検出処理
        draw_doc = DrawTool.CopyDoc(doc)
        draw_doc, results = CheckOutlineConnectivity.inspect_doc( doc, draw_doc, frameresult = fr )
        SummarizeDrawer.summarize(draw_doc, results)

        # matplotlib で描画    
        msp = draw_doc.modelspace()
        fig = plt.figure(dpi=300 )
        ax = fig.add_axes([0,0,1,1])
        ctx = RenderContext(draw_doc)
        msp_properties = LayoutProperties.from_layout(msp)
        ctx.set_current_layout(msp)
        out = MatplotlibBackend(ax)
        Frontend(ctx, out).draw_layout(msp, finalize=True, layout_properties=msp_properties)
        
        # png に保存
        fig.savefig( png_files[i], dpi=300)
        
        plt.close()

def test3():
    # ウィンドウ作成
    root = tk.Tk()
    root.title('Simple Viewer')
    root.geometry('{}x{}+200+200'.format(1600, 900))

    # フレーム作成
    viewer = SimpleViewer(master = root, error_to_console = True)
    
    # 実行
    root.mainloop()

if __name__ == '__main__':
    main()
 
 