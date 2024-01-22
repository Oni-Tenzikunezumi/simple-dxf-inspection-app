# -*- coding: utf-8 -*-
"""
Created on Fri Dec 22 19:05:49 2023

@author: shingo
"""

from ezdxf.entities import Arc, Circle, Dimension, Insert, Leader, Line, LWPolyline
from ezdxf.entities import MText, Point, Text
from ezdxf.entities.dxfgfx import DXFGraphic # Entity のベースクラス
from ezdxf.document import Drawing
from math import pi, sin, cos

class BoundingBox:
    
    EntityClasses = [Arc, Circle, Dimension, Insert, Leader, Line, LWPolyline, MText, Point, Text]
    __warning = False
    
    '''
    Entity からその矩形領域を計算するだけのクラス
    '''
    @classmethod
    def DrawingBB( cls, doc : Drawing ):
        '''
        Drawwing の矩形領域(Left, Bottom, Right, Top)を求める
        '''

        draw_bb = None
        mds = doc.modelspace()
        for ec in cls.EntityClasses:
            for entity in mds.query(ec.__name__ ):

                bb = cls.getBB(entity)
                if bb is None:
                    continue
                
                elif draw_bb is None:
                    draw_bb = [ v for v in bb ]
                    
                else:
                    draw_bb[0] = min( draw_bb[0], bb[0] ) # Left
                    draw_bb[1] = min( draw_bb[1], bb[1] ) # Bottom
                    draw_bb[2] = max( draw_bb[2], bb[2] ) # Right
                    draw_bb[3] = max( draw_bb[3], bb[3] ) # Top

        return draw_bb
                
        

    @classmethod
    def getBB( cls, entity : DXFGraphic ):
        '''
        Entity の矩形領域を求める
        '''
        class_name = entity.__class__.__name__
        
        if class_name == 'Arc':
            return cls.__getArcBB( entity )
        
        if class_name == 'Circle':
            return cls.__getCircleBB( entity )
        
        if class_name == 'Dimension':
            return cls.__getDimensionBB( entity )
        
        if class_name == 'Insert':
            return cls.__getInsertBB( entity )
        
        if class_name == 'Leader':
            return cls.__getLeaderBB( entity )
        
        if class_name == 'Line':
            return cls.__getLineBB( entity )
        
        if class_name == 'LWPolyline':
            return cls.__getLWPolylineBB( entity )
        
        if class_name == 'MText':
            return cls.__getMTextBB( entity )
        
        if class_name == 'Point':
            return cls.__getPointBB( entity )
        
        if class_name == 'Text':
            return cls.__getTextBB( entity )
        
        print( type(entity), '対応していないエンティティのため、矩形が計算できない')
        return None
            
    
    
    def __getArcBB( arc: Arc ):
        '''
        Arc(円弧)の矩形
        '''
        dxf = arc.dxf
        r = arc.dxf.radius;
        stA = dxf.start_angle * pi / 180.0
        edA = dxf.end_angle * pi / 180.0
        cx = dxf.center[0]
        cy = dxf.center[1]

        stP = (cx + r * cos(stA), cy + r * sin(stA))
        edP = (cx + r * cos(edA), cy + r * sin(edA))

        stAdeg = dxf.start_angle
        edAdeg = dxf.end_angle
        if stAdeg > edAdeg:
            edAdeg += 360.0
    
        lft = min(stP[0], edP[0])
        if stAdeg < 180.0 and 180.0 < edAdeg:
            lft = cx - r
            
        rgt = max(stP[0], edP[0])
        if stAdeg < 360.0 and 360.0 < edAdeg:
            rgt = cx + r;
        
        top = max(stP[1], edP[1]);
        if stAdeg < 90.0 and 90.0 < edAdeg:
            top = cy + r
            
        btm = min(stP[0], edP[0]);
        if stAdeg < 270.0 and 270.0 < edAdeg:
            btm = cy - r;
    
        return lft, btm, rgt, top
    
    
    def __getCircleBB( circle: Circle ):
        '''
        Circle(円)の矩形
        '''
        dxf = circle.dxf
        lft = dxf.center[0] - dxf.radius
        rgt = dxf.center[0] + dxf.radius
        btm = dxf.center[1] - dxf.radius
        top = dxf.center[1] + dxf.radius
        
        return lft, btm, rgt, top

    
    def __getDimensionBB( dimension: Dimension ):
        '''
        Dimension(寸法線)の矩形
        '''
        # TODO
        if BoundingBox.__warning:
            print( "Dimension の Bounding Box 取得は実装されていない")
        return None
    
    def __getInsertBB( insert: Insert ):
        '''
        Insert(ブロック挿入)の矩形
        '''
        #TODO
        if BoundingBox.__warning:
            print( "Insert の Bounding Box 取得は実装されていない")
        return None
        
    
    def __getLeaderBB( leader: Leader ):
        '''
        Leader(引出線)の矩形
        '''
        xmin = xmax = leader.dxf.vertices[0][0]
        ymin = ymax = leader.dxf.vertices[0][1]
        for v in leader.dxf.vertexes:
            xmin = min(xmin, v[0])
            xmax = max(xmax, v[0])
            ymin = min(ymin, v[1])
            ymax = max(ymax, v[1])
        
        # 注釈があれば考慮する
        # 以下は参考のC#のコード
        # if(leader.Annotation != null)
        # {
        #     IILSizeEntity ent = IILSizeEntity.Create(leader.Annotation);
        #     xmin = Math.Min(xmin, ent.BoundingBox.Left);
        #     xmax = Math.Max(xmax, ent.BoundingBox.Right);
        #     ymin = Math.Min(ymin, ent.BoundingBox.Bottom);
        #     ymax = Math.Max(ymax, ent.BoundingBox.Top);
        # }

        if BoundingBox.__warning:
            print( "Leader の Bounding Box 取得は「注釈」が考慮されていない")
        return xmin, ymin, xmax, ymax


    def __getLineBB( line: Line ):
        '''
        Line(直線)の矩形
        '''
        dxf = line.dxf
        lft = min( dxf.start[0], dxf.end[0] )
        rgt = max( dxf.start[0], dxf.end[0] )
        btm = min( dxf.start[1], dxf.end[1] )
        top = max( dxf.start[1], dxf.end[1] )
        
        return lft, btm, rgt, top
        
    
    def __getLWPolylineBB( lwpolyline: LWPolyline ):
        '''
        LWPolyline(ライトウェイトポリライン)の矩形
        '''
        lft = rgt = lwpolyline[0][0]
        btm = top = lwpolyline[0][1]
        for v in lwpolyline:
            lft = min(lft, v[0])
            rgt = max(rgt, v[0])
            btm = min(btm, v[1])
            top = max(top, v[1])

        return lft, btm, rgt, top
    
    def __getMTextBB( mtext: MText ):
        '''
        MLine(マルチライン)の矩形
        '''
        if BoundingBox.__warning:
            print( "Mline の Bounding Box 取得は実装されていない")
        return None
    
    
    def __getPointBB( point: Point ):
        '''
        Point(点)の矩形
        '''
        x = point.dxf.location[0]
        y = point.dxf.location[1]
        
        return x, y, x, y
    
    def __getTextBB( txt: Text ):
        '''
        Text(テキスト)の矩形
        '''
        if BoundingBox.__warning:
            print( "Text の Bounding Box 取得は実装されていない")
        return None
        
    
    
    

        