import ezdxf
import math

from ezdxf.math import Vec3
from typing import Any
from .check_base import CheckBase
from .frame_extractor import Frame_extractor_result as FrameResult
from .draw_tool import DrawTool


class CheckOuterObject(CheckBase):
    """枠線外オブジェクト検出クラス"""

    # 検図項目の名前
    inspect_name: str = "枠線外オブジェクト検出"

    # 処理内容の説明
    inspect_str: str = "図面枠外に存在するオブジェクトを検出する.\n"\
        "表示項目"
    
    @staticmethod
    def inspect_doc(doc: ezdxf.document.Drawing, **Option: tuple[Any]):
        """枠線外オブジェクト検出"""

        fresult: FrameResult = Option["frameresult"]

        # 検出処理
        detect = Detect(doc, fresult.framePoint)
        print(detect.outerobject)

        # 図面の処理
        data = []

        # 表示する図面
        document = doc

        # 列名
        columns = ('handle', 'center', 'radius')  # 列名の指定

        return document, columns, data
    


class Detect:
    """枠線検出のアルゴリズムクラス"""

    def __init__(self, doc: ezdxf.document.Drawing, framePoint: list[Vec3]):
        self.doc = doc
        self.framePoint = framePoint
        self.count = 1

        self.outerobject: dict[int: str] = {}
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

        if self.count == 1:
            print("枠線外にオブジェクトが存在しませんでした")
    

    def pointOutOfRange(self, point):
        """ある点が枠線外に存在するか確認"""
        bottomLeft = self.framePoint[0]
        topRight = self.framePoint[1]

        if point.x < bottomLeft.x or topRight.x < point.x or point.y < bottomLeft.y or topRight.y < point.y:
            return True

        return False


    def detectPoint(self):
        """POINTを検出"""
        points = self.doc.query("POINT")

        if len(points) == 0:
            return
        
        for point in points:
            location = point.dxf.location
            if self.pointOutOfRange(location):
                self.show(location, 1, "POINT")


    def detectLines(self):
        """LINEを検出"""
        lines = self.doc.query("LINE")

        if len(lines) == 0: 
            return 

        for line in lines:
            start = line.dxf.start
            end = line.dxf.end
            middle = (start + end) / 2

            if self.pointOutOfRange(start) or self.pointOutOfRange(end):
                # self.doc.add_circle(middle, 20, dxfattribs = None)
                self.show(middle, 1, 'LINE')

   
    def detectCircles(self):
        """CIRCLEを検出"""
        circles = self.doc.query("CIRCLE")

        if len(circles) == 0: 
            return

        for circle in circles:
            center = circle.dxf.center
            r = circle.dxf.radius
            vRa = Vec3(0, 1, 0) * r
            hRa = Vec3(1, 0, 0) * r

            # 円の左右上下4点
            top = center + vRa
            left = center - hRa
            bottom = center - vRa
            right = center + hRa
            
            if self.pointOutOfRange(top) or self.pointOutOfRange(left) or self.pointOutOfRange(bottom) or self.pointOutOfRange(right):
                head = center + Vec3(r * math.cos(math.pi / 4), r * math.sin(math.pi / 4), 0)
                self.show(head, 1, 'CIRCLE')
                
    
    def detectArc(self):
        """ARCを検出"""
        arcs = self.doc.query("ARC")

        if len(arcs) == 0: 
            return
        
        for arc in arcs:
            if self.pointOutOfRange(arc.start_point) or self.pointOutOfRange(arc.end_point):
                center = arc.dxf.center
                r = arc.dxf.radius
                middle_angle = (arc.dxf.end_angle - arc.dxf.start_angle) / 2

                if arc.dxf.start_angle > arc.dxf.end_angle:
                    middle_angle = - middle_angle

                head = center + Vec3(r * math.cos(math.radians(middle_angle)), r * math.sin(math.radians(middle_angle)), 0)
                self.show(head, 1, 'ARC')


    def detectText(self):
        """TEXTを検出"""
        texts = self.doc.query("TEXT")

        if len(texts) == 0:
            return

        for text in texts:
            if self.pointOutOfRange(text.get_placement()[1]):
                self.show(text.get_placement()[1], 1, "TEXT")
    
    def detectDimension(self):
        """DIMENSIONを検出"""
        dimensions = self.doc.query("DIMENSION")
        
        if len(dimensions) == 0:
            return
        
        for dimension in dimensions:
            if self.pointOutOfRange(dimension.dxf.text_midpoint):
                self.show(dimension.dxf.text_midpoint, 1, 'DIMENSION')

    def show(self, head: Vec3, color: int, object: str, head_size=5, line_width = 1, layer=None):
        tail = head + Vec3(50, 50, 0)
        DrawTool.Arrow(self.doc, head, tail, color, head_size, line_width, layer)
        self.outerobject[self.count] = object
        self.count += 1