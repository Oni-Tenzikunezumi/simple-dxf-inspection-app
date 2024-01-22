import ezdxf
import math

from ezdxf.math import Vec3
from ezdxf.document import Drawing
from typing import Any
from .check_base import CheckBase
from .frame_extractor import Frame_extractor_result as FrameResult
from .check_result import CheckResult
from .draw_tool import DrawTool


class CheckOuterObject(CheckBase):
    """枠線外オブジェクト検出クラス"""

    # 検図項目の名前
    inspect_name: str = "輪郭線外オブジェクト検出"

    # 処理内容の説明
    inspect_str: str = "図面枠外に存在するオブジェクトを検出する."
    
    @staticmethod
    def inspect_doc(doc: Drawing, draw_doc: Drawing, **Option: tuple[Any]):
        """枠線外オブジェクト検出"""

        fresult: FrameResult = Option["frameresult"]

        # 検出処理
        detect = Detect(doc, draw_doc, fresult.framePoint)
        
        return draw_doc, detect.results

    


class Detect:
    """枠線検出のアルゴリズムクラス"""

    def __init__(self, doc: Drawing, draw_doc: Drawing, framePoint: list[Vec3]):
        self.doc = doc

        polyLines = self.doc.modelspace().query("LW POLYLINE")
        for polyLine in polyLines:
            polyLine.explode()

        self.framePoint = framePoint
        self.count = 0

        self.results = []
        self.detectOuterObject()


    def detectOuterObject(self):
        """枠外オブジェクトの検出"""

        if len(self.framePoint) != 2:
            print("枠線が存在しませんでした")
            return

        self.detectPoint()
        self.detectLines()
        self.detectCircles()
        self.detectArc()
        self.detectText()
        self.detectDimension()

        if self.count == 0:
            self.res(None, "輪郭線外にオブジェクトはありません", '輪郭線外にオブジェクトが存在しませんでした')
            print("枠線外にオブジェクトが存在しませんでした")
    

    def pointOutOfRange(self, point):
        """ある点が枠線外に存在するか確認"""
        tol = 5
        bottomLeft = self.framePoint[0]
        topRight = self.framePoint[1]

        if point.x < bottomLeft.x - tol or topRight.x + tol < point.x or point.y < bottomLeft.y - tol or topRight.y + tol < point.y:
            return True

        return False


    def detectPoint(self):
        """POINTを検出"""
        points = self.doc.modelspace().query("POINT")

        if len(points) == 0:
            return
        
        for point in points:
            location = point.dxf.location
            if self.pointOutOfRange(location):
                self.res(location, '点', "点が輪郭線外に存在します")


    def detectLines(self):
        """LINEを検出"""
        lines = self.doc.modelspace().query("LINE")

        if len(lines) == 0: 
            return 

        for line in lines:
            start = line.dxf.start
            end = line.dxf.end
            middle = (start + end) / 2

            if self.pointOutOfRange(middle):
                # self.doc.modelspace().add_circle(middle, 20, dxfattribs = None)
                self.res(middle, '直線', '直線が枠外に存在します')

   
    def detectCircles(self):
        """CIRCLEを検出"""
        circles = self.doc.modelspace().query("CIRCLE")

        if len(circles) == 0: 
            return

        for circle in circles:
            center = circle.dxf.center
            r = circle.dxf.radius
            
            if self.pointOutOfRange(center):
                head = center + Vec3(r * math.cos(math.pi / 4), r * math.sin(math.pi / 4), 0)
                self.res(head, '円', '円が枠外に存在します')
                
    
    def detectArc(self):
        """ARCを検出"""
        arcs = self.doc.modelspace().query("ARC")

        if len(arcs) == 0: 
            return
        
        for arc in arcs:
            center = arc.dxf.center
            r = arc.dxf.radius
            if self.pointOutOfRange(center):
                middle_angle = (arc.dxf.end_angle - arc.dxf.start_angle) / 2

                if arc.dxf.start_angle > arc.dxf.end_angle:
                    middle_angle = 0

                head = center + Vec3(r * math.cos(math.radians(middle_angle)), r * math.sin(math.radians(middle_angle)), 0)
                self.res(head, '円弧', '円弧が枠外に存在します')


    def detectText(self):
        """TEXTを検出"""
        texts = self.doc.modelspace().query("TEXT")

        if len(texts) == 0:
            return

        for text in texts:
            if self.pointOutOfRange(text.get_placement()[1]):
                self.res(text.get_placement()[1], '文字', "文字が枠外に存在します")
    
    def detectDimension(self):
        """DIMENSIONを検出"""
        dimensions = self.doc.modelspace().query("DIMENSION")
        
        if len(dimensions) == 0:
            return
        
        for dimension in dimensions:
            if self.pointOutOfRange(dimension.dxf.text_midpoint):
                self.res(dimension.dxf.text_midpoint, '寸法線', '寸法線が枠外に存在します')

    def res(self, pos: Vec3, caption: str, desc: str):
        self.count += 1
        
        res = CheckResult(
            num = self.count,
            checkType = CheckOuterObject.inspect_name,
            error = True,
            pos = pos,
            caption = caption,
            desc = desc,
            color = 3
        )

        self.results.append(res)
        