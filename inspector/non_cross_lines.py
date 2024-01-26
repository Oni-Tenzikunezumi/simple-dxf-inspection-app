# -*- coding: utf-8 -*-
"""
Created on Wed Dec 27 16:34:17 2023

@author: shingo

２次元上で、２つの点群の各点同士を交わらないように結ぶ組み合わせを求めるクラス
"""

class NonCrossLines :
    
    @classmethod
    def analyze( cls, ps1, ps2 ):
        '''
        点群ps1と点群ps2の点を交わらないように直線でつながる組み合わせを見つける
        ps1に対応するps2のインデックスのリストが返される
        全探索に近いことをしているため、点の数が１０を超えると遅くなる場合がる
        深さ探索で探索
        '''
        assert len(ps1) == len(ps2), '点群 ps1 と点群 ps2 の点の数が異なります'
        cnt = len(ps1)
        if cnt==0: return []
        baselist = lambda: list(range(cnt))
        
        x = [baselist()]
        depth = 0
        lines = []
        index = []
        while True:
            #print(x) # printするとアルゴリズムの動きがわかりやすい
            new_p_index = x[-1][0]
            new_line = (ps1[depth], ps2[new_p_index])
            
            check = True # 次の深さへ行けるかフラグ
            if depth != 0:
                # 前の線と交わるかチェック
                for l in lines:
                    if cls.is_cross( l, new_line ):
                        check = False
                        break

            if check:
                # 直線を追加できれば次の深さへ
                lines.append( new_line )
                index.append( new_p_index )
                next_list = baselist()
                for l in x:
                    next_list.remove(l[0])
                x.append(next_list)
                depth += 1
            
            else:
                # 直線を追加できなければ次の候補にする
                x[-1].pop(0)
                while depth >= 0 and len(x[-1])==0:
                    x.pop(-1)
                    lines.pop(-1)
                    index.pop(-1)
                    x[-1].pop(0)
                    depth -= 1
            
            if depth == cnt:
                # 交わらない組み合わせが見つかった
                return index

            if depth < 0:
                # 見つからなかった
                return None
        
        
    def is_cross( line1, line2 ):
        '''
        ２つの線分が交わるか確認する
        参考: https://qiita.com/zu_rin/items/e04fdec4e3dec6072104
        '''
        pa, pb = line1
        pc, pd = line2
        
        # 点 c, d が直線 a-b で分割される領域の同じ側か調べる -> 同じ側であれば交わらない
        s = (pb[0]-pa[0])*(pc[1]-pa[1]) - (pc[0]-pa[0])*(pb[1]-pa[1])
        t = (pb[0]-pa[0])*(pd[1]-pa[1]) - (pd[0]-pa[0])*(pb[1]-pa[1])
        if s*t >= 0:
            return False
        
        # 点 a, b が直線 c-d で分割される領域の同じ側か調べる -> 同じ側であれば交わらない
        s = (pd[0]-pc[0])*(pa[1]-pc[1]) - (pa[0]-pc[0])*(pd[1]-pc[1])
        t = (pd[0]-pc[0])*(pb[1]-pc[1]) - (pb[0]-pc[0])*(pd[1]-pc[1])
        if s*t >= 0:
            return False
        
        # 交差する
        return True


if __name__ == '__main__':
    import random
    import matplotlib.pyplot as plt
    
    cnt = 10
    rnd = lambda: random.uniform(-10, 10)
    
    # 適当な点群を２つ
    ps1, ps2 = [], []
    for _ in range(cnt):
        ps1.append( (rnd(), rnd()) )
        ps2.append( (rnd(), rnd()) )
    
    # 実行
    ret = NonCrossLines.analyze(ps1, ps2)
    
    # 結果描画
    for i in range(cnt):
        x = (ps1[i][0], ps2[ret[i]][0])
        y = (ps1[i][1], ps2[ret[i]][1])
        plt.plot(x,y)
    plt.show()
        
    