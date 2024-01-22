import ezdxf
import math as Math
import glob

from ezdxf.math import Vec3


# layerごとに合成済みの水平線、垂直線のリストを取得する
class CombinedLine:
    def __init__(self, doc, layer):
        self.combinedLines = []
        self.getCombinedLines(doc, layer)

    def getCombinedLines(self, doc, layer):
        msp = doc.modelspace()

        linesInLay = msp.query(f'LINE[layer == "{layer.dxf.name}"]')
        if len(linesInLay) == 0: return
        # 水平線と垂直線をそれぞれ取得
        horizontal = []
        vertical = []
        rad = 5 * Math.pi / 180     # 許容する角度

        for line in linesInLay:
            vec = line.dxf.end - line.dxf.start

            if abs(Math.sin(vec.angle)) < Math.sin(rad):
                horizontal.append(line)
            if abs(Math.cos(vec.angle)) < Math.cos(Math.pi / 2 - rad):
                vertical.append(line)

        if len(horizontal) != 0:
            self.getCombinedHorizontalLine(msp, layer, horizontal)

        if len(vertical) != 0:
            self.getCombinedVerticalLine(msp, layer, vertical)




    # 重複している水平線を結合したリストを取得
    def getCombinedHorizontalLine(self, msp, layer, horizontalLines):
        # 水平線をy軸ごとに分類する　辞書で分類
        # 最も長い直線の傾き±1°を許容する誤差とする
        horizontalGroup = {}
        tol = 1

        for line in horizontalLines:
            if len(horizontalGroup) == 0:
                horizontalGroup[line.dxf.start.y] = [l for l in horizontalLines if line.dxf.start.y - tol <= l.dxf.start.y and l.dxf.start.y <= line.dxf.start.y + tol]

            flag = False
            for lineList in horizontalGroup.values():
                if line in lineList:
                    flag = True
                    break

            if not flag:
                horizontalGroup[line.dxf.start.y] = [l for l in horizontalLines if line.dxf.start.y - tol <= l.dxf.start.y and l.dxf.start.y <= line.dxf.start.y + tol]

        # 分類した直線をそれぞれ走査して重複している直線の座標を合成する
        combinedLinePositions = []
        judgeSet = set()
        for list in horizontalGroup.values():
            for i, baseLine in enumerate(list):
                if baseLine in judgeSet:
                    continue

                judgeSet.add(baseLine)
                basePosition = sorted([baseLine.dxf.start, baseLine.dxf.end], key = lambda x: x.x)

                for line in list[i:]:
                    position = sorted([line.dxf.start, line.dxf.end], key = lambda x: x.x)
                    if (basePosition[0].x <= position[0].x and position[0].x <= basePosition[1].x) or (basePosition[0].x <= position[1].x and position[1].x <= basePosition[1].x):
                        basePosition[0] = min([basePosition[0], position[0]], key = lambda pos: pos.x)
                        basePosition[1] = max([basePosition[1], position[1]], key = lambda pos: pos.x)
                        judgeSet.add(line)

                combinedLinePositions.append(basePosition)

        # 既存の水平線を削除
        for line in horizontalLines:
            msp.delete_entity(line)

        # 結合済みのラインをオブジェクトのリストとして取得
        # 結合済み水平線を書く
        for position in combinedLinePositions:
            self.combinedLines.append(msp.add_line(position[0], position[1], dxfattribs = {"layer": f"{layer.dxf.name}"}))



    # 重複している垂直線を結合したリストを取得
    def getCombinedVerticalLine(self, msp, layer, verticalLines):
        # 垂直線をｘ座標ごとに分類する
        # 最も長い直線の許容傾き誤差±1°座標を許容する
        verticalGroup = {}
        maxLengthLine = max(verticalLines, key = lambda line: (line.dxf.end - line.dxf.start).magnitude)
        tol = (maxLengthLine.dxf.end - maxLengthLine.dxf.start).magnitude * Math.cos(89 * Math.pi / 180)


        for line in verticalLines:
            if len(verticalGroup) == 0:
                verticalGroup[line.dxf.start.x] = [l for l in verticalLines if line.dxf.start.x - tol <= l.dxf.start.x and l.dxf.start.x <= line.dxf.start.x + tol]

            flag = False
            for lineList in verticalGroup.values():
                if line in lineList:
                    flag = True
                    break

            if not flag:
                verticalGroup[line.dxf.start.x] = [l for l in verticalLines if line.dxf.start.x - tol <= l.dxf.start.x and l.dxf.start.x <= line.dxf.start.x + tol]


        # 分類した直線をそれぞれ走査して重複している直線の座標を合成する
        combinedLinePositions = []
        judgeSet = set()
        for list in verticalGroup.values():
            for baseLine in list:
                if baseLine in judgeSet:
                    continue

                judgeSet.add(baseLine)
                basePosition = sorted([baseLine.dxf.start, baseLine.dxf.end], key = lambda y: y.y)

                for line in list[1:]:
                    position = sorted([line.dxf.start, line.dxf.end], key = lambda y: y.y)
                    if (basePosition[0].y <= position[0].y and position[0].y <= basePosition[1].y) or (basePosition[0].y <= position[1].y and position[1].y <= basePosition[1].y):
                        basePosition[0] = min([basePosition[0], position[0]], key = lambda pos: pos.y)
                        basePosition[1] = max([basePosition[1], position[1]], key = lambda pos: pos.y)
                        judgeSet.add(line)

                combinedLinePositions.append(basePosition)

        # 既存の水平線を削除
        for line in verticalLines:
            msp.delete_entity(line)

        # 結合済みのラインをオブジェクトのリストとして取得
        # 結合済み水平線を書く
        for position in combinedLinePositions:
            self.combinedLines.append(msp.add_line(position[0], position[1], dxfattribs = {"layer": f"{layer.dxf.name}"}))



# layer内の枠線検出クラス
class FrameField:
    # linesは合成済みの水平線と垂直線を合わせたリストを想定
    def __init__(self, lines):
        self.candidateLine = []
        self.frameLineList = []
        self.error_str = ""
        self.maxMinPoint = []
        self.hasFrame = self.detectCursoryFrame(lines)
        self.return_list = [self.maxMinPoint, self.error_str]


    # 直線の端点の座標をリストにして返す
    # 軸順にソートして返す
    def positionAboutX(self, line):
        res = [line.dxf.start, line.dxf.end]

        return sorted(res, key = lambda X: X.x)

    def positionAboutY(self, line):
        res = [line.dxf.start, line.dxf.end]

        return sorted(res, key = lambda Y: Y.y, reverse = True)


    # 点と点の距離が許容範囲内になっているか返す
    def isSurrounding(self, line, pointA, pointB):
        tol = (line.dxf.end - line.dxf.start).magnitude * 0.01
        target = (pointB - pointA).magnitude

        return target <= tol


    # 横線の候補2本と縦線の候補２本が大まかに四角形になっているかを返す
    def isCursoryFrame(self, horizontalLines, verticalLines):
        # 各枠線候補は２本ずつ
        if len(horizontalLines) != 2 or len(verticalLines) != 2:
            return False

        # x座標とy座標で並べ替え
        hLines = sorted(horizontalLines, key = lambda line: line.dxf.start.y, reverse = True)
        vLines = sorted(verticalLines, key = lambda line: line.dxf.start.x)

        # 座標の取得
        hPosition = [self.positionAboutX(line) for line in hLines]
        vPosition = [self.positionAboutY(line) for line in vLines]

        # 各水平線について，左右の端が垂直線の端に大まかにそろっているかを見る
        for i in range(len(hLines)):
            hline = hLines[i]
            isLeftConnected = self.isSurrounding(hline, hPosition[i][0], vPosition[0][i])    # 左との位置確認
            isRightConnected = self.isSurrounding(hline, hPosition[i][1], vPosition[1][i])   # 右との位置確認

            if not(isLeftConnected and isRightConnected): return False

        return True


    @staticmethod
    # n個の要素から2個の組み合わせのインデックスを返す
    def Combination2inN(n):
        comb = []
        for  i in range(n):
            for j in range(i + 1, n):
                ele = [i, j]
                comb.append(ele)

        return comb

    def detectCursoryFrame(self, lines):
        # linesの長さは1以上
        if len(lines) == 0:
            self.error_str = "直線が存在しません"
            return False

        # 輪郭線の候補を検索 昇順にソートして３つ選択
        horizontal = []
        vertical = []
        rad = 5 * Math.pi / 180     # 許容する角度

        for line in lines:
            vec = line.dxf.end -line.dxf.start

            if abs(Math.sin(vec.angle)) < Math.sin(rad):
                horizontal.append(line)
            if abs(Math.cos(vec.angle)) < Math.cos(Math.pi / 2 - rad):
                vertical.append(line)

        horizontal.sort(key = lambda x: (x.dxf.end - x.dxf.start).magnitude, reverse = True)
        vertical.sort(key = lambda x: (x.dxf.end - x.dxf.start).magnitude, reverse = True)

        # 水平線、垂直線それぞれ３本以上必要
        if len(horizontal) < 3 and len(vertical) < 3:
            self.error_str = '水平線と垂直線のどちらも候補線の数が足りません'
            return False
        elif len(horizontal) < 3:
            self.error_str = '水平線の候補線の数が足りません'
            return False
        elif len(vertical) < 3:
            self.error_str = '垂直線の候補線の数が足りません'
            return False
        
        ca_horizontal = horizontal[:3]
        ca_vertical = vertical[:3]

        # 候補となるlineのstartpoint, endpointを登録
        for line in ca_horizontal:
            self.candidateLine.append(line)
        for line in ca_vertical:
            self.candidateLine.append(line)


        # 組み合わせの生成
        comb = FrameField.Combination2inN(3)

        # 枠線の検出
        for e in comb:
            # 水平線候補
            hLines = [ca_horizontal[e[0]], ca_horizontal[e[1]]]

            for f in comb:
                # 垂直線候補
                vLines = [ca_vertical[f[0]], ca_vertical[f[1]]]

                # 大まかな枠線の判定
                isCursory = self.isCursoryFrame(hLines, vLines)

                if isCursory:
                    # 上辺から時計回りに登録
                    hLines.sort(key = lambda line: line.dxf.start.y, reverse = True)
                    vLines.sort(key = lambda line: line.dxf.start.x, reverse = True)

                    self.frameLineList.append(hLines[0])
                    self.frameLineList.append(vLines[0])
                    self.frameLineList.append(hLines[1])
                    self.frameLineList.append(vLines[1])

                    self.getframePoint()
                    self.error_str = "枠線が存在しました"

                    return True

        self.error_str = "枠線となる四角形が存在しませんでした"

        return False

    def getframePoint(self):
        topLine = self.frameLineList[0]
        rightLine = self.frameLineList[1]
        bottomLine = self.frameLineList[2]
        leftLine = self.frameLineList[3]

        self.maxMinPoint.append(self.calPoint(leftLine, bottomLine))
        self.maxMinPoint.append(self.calPoint(topLine, rightLine))

    def calPoint(self, lineA, lineB):
        """交点計算"""
        va: Vec3 = lineA.dxf.end - lineA.dxf.start
        vb: Vec3 = lineB.dxf.end - lineB.dxf.start
        vab: Vec3 = lineB.dxf.start - lineA.dxf.start
        vba: Vec3 = -vab
        
        bxa: float = vb.cross(va).z
 
        if not va.is_parallel(vb, rel_tol=0.0001):
            ta: float = vba.cross(vb).z / bxa
            vt: Vec3 = ta * va + lineA.dxf.start

        return vt

    def drawCandidateLine(self):
        doc = ezdxf.new()
        msp = doc.modelspace()

        for line in self.candidateLine:
            msp.add_line(line.dxf.start, line.dxf.end, dxfattribs = None)

        doc.saveas("candidate.dxf")



class Frame_extractor:
    def __init__(self, doc):
        self.doc = doc
        self.disassembly_Poly()
        self.pointAndMessage = self.detect_frame()

    # docの内部のpolylineを分解する
    def disassembly_Poly(self):
        msp = self.doc.modelspace()

        polyLines = msp.query("LW POLYLINE")
        for polyLine in polyLines:
            polyLine.explode()

    # 全体の枠線を検出するメソッド
    def detect_frame(self):
        layers = self.doc.layers

        # layerごとの結合済み水平線、垂直線のリスト
        linesInlayer = []
        # layerごとにFrameFeildクラスのリスト
        frameInLayers = []
        for layer in layers:
            lineList = CombinedLine(self.doc, layer)
            linesInlayer.append(lineList.combinedLines)
            frameInLayers.append(FrameField(lineList.combinedLines))

        # 全体の水平線、垂直線のリスト
        lineInAllLayer = []
        for lines in linesInlayer:
            lineInAllLayer.extend(lines)

        FrameInAll = FrameField(lineInAllLayer)

        # 全体の水平線、垂直線で枠線が得られなかった場合、枠線は存在しない
        if not FrameInAll.hasFrame:
            print("枠線は存在しませんでした")
            return FrameInAll.return_list

        # layerごとに枠線が存在するか確認する
        # 存在する場合その枠線を登録
        # 存在しない場合、枠線を作る直線の構成がおかしい
        for frame in frameInLayers:
            if frame.hasFrame:
                return frame.return_list

        # 枠線の構成がおかしい
        FrameInAll.return_list[1] = "枠線の構成するレイヤーがおかしいです"
        return FrameInAll.return_list


class Frame_extractor_result:
    def __init__(self, doc):
        frame_extractor = Frame_extractor(doc)
        self.framePoint = frame_extractor.pointAndMessage[0]
        self.message = frame_extractor.pointAndMessage[1]



if __name__ == "__main__":
    filePaths = glob.glob('D:\\2023_Satsuka\dxf練習\inputdata\*.dxf')
    for i, filePath in enumerate(filePaths):
        print(filePath)
        print(i + 1)
        doc = ezdxf.readfile(filePath)

        frame_extractor_result = Frame_extractor_result(doc)
        print(frame_extractor_result.framePoint)
        print(frame_extractor_result.message)

        print("-" * 30)


