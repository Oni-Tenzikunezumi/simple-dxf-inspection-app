# import tkinter as tk
import ezdxf
import math

from ezdxf.math import Vec3
from ezdxf.entities import Line, Circle, Arc
from typing import Union
from typing import Any
from ezdxf.document import Drawing
from inspector.check_base import CheckBase
from inspector.frame_extractor import Frame_extractor_result as FrameResult
from inspector.draw_tool import DrawTool
from inspector.check_result import CheckResult


class CheckOutlineConnectivity(CheckBase):
    """外形線の接続性チェッククラス"""

    inspect_name: str = '外形線の接続性確認'
    inspect_str: str = '枠線内に存在する外形線の接続性を確認します'

    @staticmethod
    def inspect_doc(doc: Drawing, draw_doc: Drawing, **Option: dict[str, Any]):
        """外形線の接続性を確認"""

        fresult: FrameResult = Option['frameresult']

        # 接続性が不足している直線を保存
        errline: dict[Line: list[Vec3]] = {}

        # 実線抽出
        continuousLines: list[ezdxf.entities] = ExtractContinuouslines.extract(doc)
        print(f'len(continuous): {continuousLines}')
        
        # 交点抽出
        intersections: Intersection = Intersection(continuousLines)
        print(intersections.outLines.values())
        
        number = 1
        color = 7
        results = []
        for entity, cntList in intersections.outLines.items():
            if not CheckOutlineConnectivity.isInFrame(entity, fresult):
                continue

            checkType = CheckOutlineConnectivity.inspect_name
            error = True
            pos = Vec3(0, 0, 0)
            caption = ''
            desc = ''

            if entity.dxftype() == 'LINE':
                

                pos = (entity.dxf.start + entity.dxf.end) / 2
                if cntList[0] == 1 or cntList[0] == 0 and cntList[1] >= 2:
                    caption = 'ループが途切れています'
                    desc = 'ループが切れた直線が輪郭線内に存在します'
                    res = CheckResult(
                        num = number,
                        checkType = checkType,
                        error = error,
                        pos = pos,
                        caption = caption,
                        desc = desc,
                        color = color
                    )
                    results.append(res)
                    number += 1
                elif cntList[0] == 0:
                    caption = '余計な線です'
                    desc = '余計な線が輪郭線内に存在します'
                    res = CheckResult(
                        num = number,
                        checkType = checkType,
                        error = error,
                        pos = pos,
                        caption = caption,
                        desc = desc,
                        color = color
                    )
                    results.append(res)
                    number += 1
            
            elif entity.dxftype() == 'ARC':
                pos = entity.start_point
                if cntList[0] == 1 or cntList[0] == 0 and cntList[1] >= 2:
                    caption = 'ループが途切れています'
                    desc = 'ループが切れた円弧が輪郭線内に存在します'
                    res = CheckResult(
                        num = number,
                        checkType = checkType,
                        error = error,
                        pos = pos,
                        caption = caption,
                        desc = desc,
                        color = color
                    )
                    results.append(res)
                    number += 1
                elif cntList[0] == 0:
                    caption = '余計な線です'
                    desc = '余計な円弧が輪郭線内に存在します'
                    res = CheckResult(
                        num = number,
                        checkType = checkType,
                        error = error,
                        pos = pos,
                        caption = caption,
                        desc = desc,
                        color = color
                    )
                    results.append(res)
                    number += 1

            elif entity.dxftype() == 'CORCLE':
                pos = entity.dxf.center + Vec3(entity.dxf.radius * math.cos(math.pi / 4), entity.dxf.radius * math.sin(math.pi / 4), 0)
                if cntList[1] < 2:
                    caption = 'ロープが途切れた円です'
                    desc = 'ループが切れた円が輪郭線内に存在します'
                    res = CheckResult(
                        num = number,
                        checkType = checkType,
                        error = error,
                        pos = pos,
                        caption = caption,
                        desc = desc,
                        color = color
                    )
                    results.append(res)
                    number += 1


        print(f'len(reuslts): {len(results)}')

        return draw_doc, results
    
    @staticmethod
    def isInFrame(entity, fresult):
        bottomleft = fresult.framePoint[0]
        topright = fresult.framePoint[1]

        if entity.dxftype() == 'LINE':
            pos = (entity.dxf.start + entity.dxf.end) / 2
            return bottomleft.x < pos.x < topright.x and bottomleft.y < pos.y < topright.y
        
        center = entity.dxf.center
        return bottomleft.x < center.x < topright.x and bottomleft.y < center.y < topright.y
            


class ExtractContinuouslines:
    """図面内の実線のみを抽出するクラス"""

    @staticmethod
    def extract(doc: ezdxf.document.Drawing):
        """実線を抽出"""
        # 実線のレイヤーを取得
        layers = doc.layers
        continuous_layer = []
        for layer in layers:
            if layer.dxf.linetype == "Continuous":
                continuous_layer.append(layer.dxf.name)

        # layerごとにentityをグループ分け
        group = doc.groupby('layer')

        # 外形線レイヤーを取得する
        outlineLayer = ""
        lenOutLine = 0
        for layerName, entities in group.items():
            if layerName not in continuous_layer: continue

            count = 0
            for entity in entities:
                # typeが直線、円、円弧のみを取得、そのほかはスルー
                dxftype = entity.dxftype()
                if dxftype == 'LINE' or dxftype == 'CIRCLE' or dxftype == 'ARC':
                    count += 1
            
            if count >= lenOutLine:
                outlineLayer = layerName
                lenOutLine = count

        # 外形線レイヤの上のエンティティを取得
        continuousLines = []
        for entity in group.get(outlineLayer):
            continuousLines.append(entity)

        return continuousLines



class Intersection:
    """図面内の外形線のみの交点を求めるクラス"""

    def __init__(self, continuousLines: list[ezdxf.entities]):
        #すべての交点をまとめるリスト
        self.points: set = set()

        # 外形線の持つ交点の数をそのエンティティと辞書型で保存
        self.outLines: dict[ezdxf.entities: list[int]] = {}

        # dexftypeごとに分ける
        self.dict: dict[str: list[ezdxf.entities]] = {}
        for entity in continuousLines:
            if not entity.dxftype() in self.dict.keys():
                entityList = [entity]
                self.dict[entity.dxftype()] = entityList
            else:
                self.dict[entity.dxftype()].append(entity)

        self.getInterLineAndLine()
        self.getInterCircleAndLine()
        self.getInterLineAndArc()
        self.getInterCircleAndCircle()
        self.getInterCircleAndArc()
        self.getInterArcAndArc()

    def countInter(self, A: Union[Line, Circle, Arc], B: Union[Line, Circle, Arc], pointSet: set):
        def isRange(endpoint, pointVec, v):
            return (endpoint - pointVec).magnitude <= v * 0.01
        
        if not A in self.outLines.keys():
            self.outLines[A] = [0, 0]
        if not B in self.outLines.keys():
            self.outLines[B] = [0, 0]

        pointList = list(pointSet)
        
        if len(pointList) != 0:
            if A.dxftype() == 'LINE' and B.dxftype() == 'LINE':
                self.outLines.get(A)[1] += 1
                self.outLines.get(B)[1] += 1

                va = A.dxf.end - A.dxf.start                
                vb = B.dxf.end - B.dxf.start
                lenv = max([va.magnitude, vb.magnitude])

                for endpoint in [A.dxf.start, A.dxf.end]:
                    if isRange(endpoint, pointList[0], lenv):
                        self.outLines.get(A)[0] += 1
                for endpoint in [B.dxf.start, B.dxf.end]:
                    if isRange(endpoint, pointList[0], lenv):
                        self.outLines.get(B)[0] += 1

            elif A.dxftype() == 'LINE' and B.dxftype() == 'CIRCLE':
                for point in pointList:
                    self.outLines.get(A)[1] += 1
                    self.outLines.get(B)[1] += 1
                    
                    va = A.dxf.end - A.dxf.start

                    for endpoint in [A.dxf.start, A.dxf.end]:
                        if isRange(endpoint, point, va.magnitude):
                            self.outLines.get(A)[0] += 1
                
            elif A.dxftype() == 'LINE' and B.dxftype() == 'ARC':
                for point in pointList:
                    self.outLines.get(A)[1] += 1
                    self.outLines.get(B)[1] += 1
                    
                    va = A.dxf.end - A.dxf.start

                    for endpoint in [A.dxf.start, A.dxf.end]:
                        if isRange(endpoint, point, va.magnitude):
                            self.outLines.get(A)[0] += 1
                    for endpoint in [B.start_point, B.end_point]:
                        if isRange(endpoint, point, va.magnitude):
                            self.outLines.get(B)[0] += 1

            elif A.dxftype() == 'CIRCLE' and B.dxftype() == 'CIRCLE':
                for point in pointList:
                    self.outLines.get(A)[1] += 1
                    self.outLines.get(B)[1] += 1
                    
            elif A.dxftype() == 'CIRCLE' and B.dxftype() == 'ARC':
                lenv = max([A.dxf.radius, B.dxf.radius])
                for point in pointList:
                    self.outLines.get(A)[1] += 1
                    self.outLines.get(B)[1] += 1
                    
                    for endpoint in [B.start_point, B.end_point]:
                        if isRange(endpoint, point, lenv):
                            self.outLines.get(B)[0] += 1

            elif A.dxftype() == 'ARC' and B.dxftype() == 'ARC':
                lenv = max([A.dxf.radius, B.dxf.radius])
                for point in pointList:
                    self.outLines.get(A)[1] += 1
                    self.outLines.get(B)[1] += 1    

                    for endpoint in [A.start_point, A.end_point]:
                        if isRange(endpoint, pointList[0], lenv):
                            self.outLines.get(A)[0] += 1
                    for endpoint in [B.start_point, B.end_point]:
                        if isRange(endpoint, pointList[0], lenv):
                            self.outLines.get(B)[0] += 1




    
    def getInterLineAndLine(self):
        """図面内の直線同士の交点を求める"""
        try:
            lines: list[Line] = self.dict.get('LINE')
            print(len(lines))
            for i in range(len(lines)):
                for j in range(i + 1, len(lines)):
                    pointSet = Calculator.calInterLineAndLine(lines[i], lines[j])
                    self.countInter(lines[i], lines[j], pointSet)
                    self.points.update(pointSet)
        except KeyError as e:
            print(f'{e}: 直線が存在しません')
        except IndexError as e:
            print(f'{e}: 直線が一本しかありません')
        
        
    def getInterCircleAndLine(self):
        """図面内の直線と円の交点を求める"""
        try:
            lines: list[Line] = self.dict.get('LINE')
            circles: list[Circle] = self.dict.get('CIRCLE')

            for line in lines:
                for circle in circles:
                    pointSet = Calculator.calInterCircleAndLine(line, circle)
                    self.countInter(line, circle, pointSet)
                    self.points.update(pointSet)
        except KeyError as e:
            print(f'{e}: 直線または円が存在しません')

    
    def getInterLineAndArc(self):
        """図面内の直線と円弧の交点を求める"""
        try:
            lines: list[Line] = self.dict.get('LINE')
            arcs: list[Arc] = self.dict.get('ARC')
        
            for line in lines:
                for arc in arcs:
                    pointSet = Calculator.calInterArcAndLine(line, arc)
                    self.countInter(line, arc, pointSet)
                    self.points.update(pointSet)
        except KeyError as e:
            print(f'{e}: 直線または円弧が存在しません')

    
    def getInterCircleAndCircle(self):
        """図面内の円同士の交点を求める"""
        try:
            circles: list[Circle] = self.dict.get('CIRCLE')

            for i in range(len(circles)):
                for j in range(i + 1, len(circles)):
                    pointSet = Calculator.calInterCircleAndCircle(circles[i], circles[j])
                    self.countInter(circles[i], circles[j], pointSet)
                    self.points.update(pointSet)
        except KeyError as e:
            print(f'{e}: 円が存在しません')
        except IndexError as e:
            print(f'{e}: 円が１つしかありません')


    def getInterCircleAndArc(self):
        """図面内の円と円弧の交点を求める"""
        try:
            circles: list[Circle] = self.dict.get('CIRCLE')
            arcs: list[Arc] = self.dict.get('ARC')

            for circle in circles:
                for arc in arcs:
                    pointSet = Calculator.calInterCircleAndArc(circle, arc)
                    self.countInter(circle, arc, pointSet)
                    self.points.update(pointSet)
        except KeyError as e:
            print(f'{e}: 円または円弧が存在しません')
            
    
    def getInterArcAndArc(self):
        """図面内の円弧同士の交点を求める"""
        try:
            arcs: list[Arc] = self.dict.get('ARC')

            for i in range(len(arcs)):
                for j in range(i + 1, len(arcs)):
                    pointSet = Calculator.calInterArcAndArc(arcs[i], arcs[j])
                    self.countInter(arcs[i], arcs[j], pointSet)
                    self.points.update(pointSet)
        except KeyError as e:
            print(f'{e}: 円弧が存在しません')
        except IndexError as e:
            print(f'{e}: 円弧が１つしかありません')
            



class DummyCircle:
    """ダミー円を作成するクラス"""
    def __init__(self, center: Vec3, radius: float):
        self.center: Vec3 = center
        self.radius: float = radius



class Calculator:
    """交点を求める計算処理クラス"""
    TOL = 0.01

    @staticmethod
    def isOnLine(pointVec: Vec3, line: Line) -> bool:
        """点が直線上にあるかどうか確認"""
        # 点と直線の距離
        distance: float = Calculator.calRangePointAndLine(pointVec, line)
        
        # pointVecが指定の範囲に入っているか
        isRangeX: bool = min(line.dxf.start.x, line.dxf.end.x) - Calculator.TOL <= pointVec.x and pointVec.x <= max(line.dxf.start.x, line.dxf.end.x) + Calculator.TOL
        isRangeY: bool = min(line.dxf.start.y, line.dxf.end.y) - Calculator.TOL <= pointVec.y and pointVec.y <= max(line.dxf.start.y, line.dxf.end.y) + Calculator.TOL

        return distance <= Calculator.TOL and isRangeX and isRangeY
    
    @staticmethod
    def calInterLineAndLine(lineA: Line, lineB: Line) -> set:
        """直線同士の交点を求める"""
        pointSet = set()
        
        va: Vec3 = lineA.dxf.end - lineA.dxf.start
        vb: Vec3 = lineB.dxf.end - lineB.dxf.start
        vab: Vec3 = lineB.dxf.start - lineA.dxf.start
        vba: Vec3 = -vab
        
        bxa: float = vb.cross(va).z

        if va.magnitude == 0 or vb.magnitude == 0: return pointSet
        
        if not va.is_parallel(vb, rel_tol=Calculator.TOL):
            ta: float = vba.cross(vb).z / bxa
            vt: Vec3 = ta * va + lineA.dxf.start

            if Calculator.isOnLine(vt, lineA) and Calculator.isOnLine(vt, lineB):
                pointSet.add(vt)

        return pointSet

                
    @staticmethod
    def calRangePointAndLine(pointVec: Vec3, line: Line) -> float:
        """pointVecと直線の距離を計算する"""
        va: Vec3 = line.dxf.end - line.dxf.start
        vAsP: Vec3 = pointVec - line.dxf.start

        d: float = va.cross(vAsP).z / va.magnitude
        
        return abs(d)
    

    @staticmethod
    def calInterCircleAndLine(line: Line, circle: Union[Circle, DummyCircle]) -> set:
        """円と直線の交点を計算する"""
        pointSet: set = set()
        center: Vec3 = circle.dxf.center if isinstance(circle, Circle) else circle.center
        radius: float = circle.dxf.radius if isinstance(circle, Circle) else circle.radius
        vL: Vec3 = line.dxf.end - line.dxf.start
        vLsC: Vec3 = center - line.dxf.start
        lenvL: float = vL.magnitude
        lenvLsC: float  = vLsC.magnitude

        # 二次方程式のパラメータ
        a = math.pow(lenvL, 2)
        b = -2 * vL.dot(vLsC)
        c = math.pow(lenvLsC, 2) - math.pow(radius, 2)
        # 判別式
        D = math.pow(b, 2) - 4 * a * c

        # 交点の計算
        tList = []

        # 長さが０の時交点としない
        if (line.dxf.end - line.dxf.start).magnitude == 0:
            return pointSet
        
        # 直線と円の中心の距離で交点の数を算出
        distance: float = Calculator.calRangePointAndLine(center, line)
        deltaR = distance - radius

        if abs(deltaR) < Calculator.TOL:
            # 重解
            tList.append(-b / (2 * a))
        elif D > 0:
            tList.append((-b + math.sqrt(D)) / (2 * a))
            tList.append((-b - math.sqrt(D)) / (2 * a))

        # 交点の位置を確認
        for ti in tList:
            vt: Vec3 = ti * vL + line.dxf.start

            if Calculator.isOnLine(vt, line):
                pointSet.add(vt)

        return pointSet
    

    @staticmethod
    def calInterCircleAndCircle(c1: Union[Circle, DummyCircle], c2: Union[Circle, DummyCircle]) -> set:
        """円と円の交点を計算する"""
        pointSet = set()

        if Calculator.areOverlapped(c1, c2):
            return pointSet

        # 中心同士を結ぶベクトル
        center1: Vec3 = c1.dxf.center if isinstance(c1, Circle) else c1.center
        center2: Vec3 = c2.dxf.center if isinstance(c2, Circle) else c2.center
        vC1C2: Vec3 = center2 - center1
        lenvC1C2: float = vC1C2.magnitude
        r1: float = c1.dxf.radius if isinstance(c1, Circle) else c1.radius
        r2: float = c2.dxf.radius if isinstance(c2, Circle) else c2.radius

        # 中心間の距離で場合分け
        deltaR: float = lenvC1C2 - (r1 + r2)
        deltaG: float = lenvC1C2 - abs(r1 - r2)
        if deltaR > 2 * Calculator.TOL or deltaG < 2 * Calculator.TOL:
            # 円同士が交わっていないとき
            return pointSet
        elif abs(deltaR) <=  2 * Calculator.TOL or abs(deltaG) <= 2 * Calculator.TOL:
            # 円同士が接しているとき
            inter = center1 + vC1C2 / lenvC1C2 * (r1 + Calculator.TOL)
            pointSet.add(inter)

            return pointSet
        else:
            # 円同士が２点で交わっているとき
            # 余弦定理
            costheta: float = (math.pow(r1, 2) + math.pow(lenvC1C2, 2) - math.pow(r2, 2)) / (2 * r1 * lenvC1C2)

            rc: float = r1 * costheta
            rs: float = math.sqrt(math.pow(r1, 2) - math.pow(rc,2))

            # 中心間のベクトル単位ベクトル
            e1: Vec3 = vC1C2 / lenvC1C2
            # e1を90°反時計回りに回転したベクトル
            e2: Vec3 = e1.rotate_deg(90)

            pointSet.add(center1 + rc * e1 + rs * e2)
            pointSet.add(center1 + rc * e1 - rs * e2)

            return pointSet


    @staticmethod
    def isOnArc(pointVec: Vec3, arc: Arc) -> bool:
        """点がARC上に存在するかどうか"""
        vcp: Vec3 = pointVec - arc.dxf.center
        avcp: float = vcp.angle_deg
        aS: float = arc.dxf.start_angle
        aE: float = arc.dxf.end_angle

        # pointVecと中心の距離が許容範囲内であるか
        if vcp.magnitude - arc.dxf.radius > Calculator.TOL:
            return False
        
        # 角度がマイナスの時プラスに変換
        if avcp < 0:
            avcp += 360
    
        # 円弧が360°をまたがっているとき
        if aS >= aE:
            return aS <= avcp and avcp <= 360 or 0 <= avcp and avcp <= aE
        
        return aS <= avcp and avcp <= aE
    

    @staticmethod
    def calInterArcAndLine(line: Line, arc: Arc) -> set:
        """円弧と直線の交点を計算する"""
        # 円弧を円として交点を計算
        c = DummyCircle(arc.dxf.center, arc.dxf.radius)
        circlePoint = Calculator.calInterCircleAndLine(line, c)

        pointset = set()
        for point in circlePoint:
            if Calculator.isOnArc(point, arc):
                pointset.add(point)

        return pointset
    

    @staticmethod
    def calInterCircleAndArc(circle: Circle, arc: Arc) -> set:
        """円と円弧の交点を計算する"""
        pointSet = set()

        if Calculator.areOverlapped(circle, arc):
            return pointSet
        
        # 円弧を円として計算
        c = DummyCircle(arc.dxf.center, arc.dxf.radius)
        circlePoint = Calculator.calInterCircleAndCircle(circle, c)

        for point in circlePoint:
            if Calculator.isOnArc(point, arc):
                pointSet.add(point)

        return pointSet
    

    @staticmethod
    def calInterArcAndArc(arc1: Arc, arc2: Arc) -> set:
        """円弧同士の交点を計算する"""
        pointSet = set()
        
        if Calculator.areOverlappedArcAndArc(arc1, arc2):
            return pointSet
        
        # 円弧を円として考える
        c1 = DummyCircle(arc1.dxf.center, arc1.dxf.radius)
        c2 = DummyCircle(arc2.dxf.center, arc2.dxf.radius)

        circlePoint = Calculator.calInterCircleAndCircle(c1, c2)

        for point in circlePoint:
            if Calculator.isOnArc(point, arc1) and Calculator.isOnArc(point, arc2):
                pointSet.add(point)

        return pointSet
    

    @staticmethod
    def areOverlapped(c1: Union[Circle, Arc, DummyCircle], c2: Union[Circle, Arc, DummyCircle]) -> bool:
        """円同士がまたは円と円弧同士が重複しているか返す"""
        center1: Vec3 = c1.dxf.center if isinstance(c1, Circle) or isinstance(c1, Arc) else c1.center
        center2: Vec3 = c2.dxf.center if isinstance(c2, Circle) or isinstance(c2, Arc) else c2.center 
        radius1: float = c1.dxf.radius if isinstance(c1, Circle) or isinstance(c1, Arc) else c1.radius
        radius2: float = c2.dxf.radius if isinstance(c2, Circle) or isinstance(c2, Arc) else c2.radius
        
        # 同一の中心
        isConcentricCircle: bool = (center1 - center2).magnitude <= Calculator.TOL
        # 同一の半径
        isOmetric: bool = abs(radius1 - radius2) <= Calculator.TOL

        return isConcentricCircle and isOmetric
    

    @staticmethod
    def areOverlappedArcAndArc(arc1: Arc, arc2: Arc) -> bool:
        """円弧同士が重複しているかどうか返す"""
        # 同一中心かつ同一半径
        if not Calculator.areOverlapped(arc1, arc2):
            return False
        
        startAngle: float = arc1.dxf.start_angle
        endAngle: float = arc1.dxf.end_angle

        # 片方の円弧の間にもう一方の開始角か終了角が入っていれば部分的にも重複している
        angleInS = startAngle <= arc2.dxf.start_angle and arc2.dxf.start_angle <= endAngle
        angleInE = startAngle <= arc2.dxf.end_angle and arc2.dxf.end_angle <= endAngle

        if startAngle > endAngle:
            angleInS = startAngle <= arc2.dxf.start_angle and arc2.dxf.start_angle <= 360 or 0 <= arc2.dxf.start_angle and arc2.dxf.start_angle <= endAngle
            angleInE = startAngle <= arc2.dxf.end_angle and arc2.dxf.end_angle <= 360 or 0 <= arc2.dxf.end_angle and arc2.dxf.end_angle <= endAngle

        return angleInS or angleInE
    

    @staticmethod
    def areOverlappedLineAndLine(line1: Line, line2: Line) -> bool:
        """直線同士が重複しているかどうか返す"""
        v1: Vec3 = line1.dxf.end - line1.dxf.start
        v2: Vec3 = line2.dxf.end - line2.dxf.start

        if v1.magnitude == 0 or v2.magnitude == 0:
            return True

        if not v1.is_parallel(v2, rel_tol=Calculator.TOL) and v1.distance(v2) <= Calculator.TOL:
            return False
        
        return Calculator.isOnLine(line2.dxf.start, line1) or Calculator.isOnLine(line2.dxf.end, line1) or Calculator.isOnLine(line1.dxf.start, line2) or Calculator.isOnLine(line1.dxf.end, line2)
            




def test():
    path = "D:\\2023_Satsuka\dxf練習\inputdata\\test01.dxf"
    doc = ezdxf.readfile(path)

    continuous = ExtractContinuouslines.extract(doc)
    
    intersections = Intersection(continuous)

    print(intersections.outLines)

    # intersections = Intersection(ExtractContinuouslines.extract(doc))
    # for point in intersections.points:
    #     msp.add_circle(point, 5, dxfattribs = None)

    # resultPath = path[:-4] + '_test.dxf'
    # doc.saveas(resultPath)

    # intersections = Intersection(ExtractContinuouslines.extract(doc))
    # print(intersections.points)

def main():
    test()

if __name__ == '__main__':
    main()