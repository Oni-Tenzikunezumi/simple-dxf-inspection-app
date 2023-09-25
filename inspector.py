# -*- coding: utf-8 -*-
"""検図を行うモジュール.

Created on Fri Sep 22 12:46:56 2023.
@author: Yuta Kuronuma
"""

import ezdxf


def inspect_doc(doc: ezdxf.document.Drawing):
    """図面docを検図し，検図結果のlistと表にする際の列名を返す.

    Parameters
    ----------
    doc : ezdxf.document.Drawing
        検図を行う図面.

    Returns
    -------
        document : ezdxf.document.Drawing
            表示する図面のDrawing

        columns : list[str]
            表にする際の列名.
            列名は検図結果のdictに存在するkeyから選択する.
            表はlist内の順番で列が表示される.

        data : list[dict[str, any]]
            検図結果のリスト.
            key:value = 検図項目:内容

    """
    # 入力された図面からlineエンティティのみを表示するサンプル.

    # 図面の処理
    data = [ent.dxfattribs() for ent in doc.query('LINE')]

    # 表示する図面
    docment = doc

    # 列名
    columns = ('owner', 'handle')  # 列名の指定

    return docment, columns, data


if __name__ == '__main__':

    path = r'./dxf/700.dxf'

    doc = ezdxf.readfile(path)

    document, col, data = inspect_doc(doc)
    print(document)
    print(col)
    # print(data)
