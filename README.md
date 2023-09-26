## simple-dxf-inspection-app
 DXFファイルの表示，指定された検図処理を行います．
 python3.10以降での環境で動作します．

 ## インストールと実行方法
 1. Python3.10以降の環境を用意する．
 1. 以下のコードを実行してライブラリをインストールする．
 ```pip install -r requirements.txt```
 1. inspector.pyのinspect_doc関数に検図処理を記述する．
 1. simple_viewer.pyを実行する.

 ## UIの使用方法
 #### 図面の読み込み
 1. アプリ上部の[参照]をクリック.
 1. DXFファイルを選択し，[開く(O)]をクリック.
 1. エントリ内にパスが挿入されたことを確認し，[読み込み]をクリック.

 #### ODAの設定
 1. ODA File Converterをインストールし，インストール場所をメモしておく.
 1. アプリの[設定]>[環境設定]をクリック.
 1. 環境設定のODA File Converterの欄にある[参照]をクリック.
 1. インストール場所のODAFileConverter.exeを選択し，[開く(O)]をクリック.
 1. エントリ内にパスが挿入されたことを確認し，[読み込み]をクリック.
 1. エントリの上に「パスが指定されています．利用可能です．」と表示されれば完了．

 ## 使用ライブラリ
 * DXF処理
    * ezdxf  1.0.3

 * UI
    * tkinter
    * matplotlib
    * configparser

 * exe化
    * pyinstaller
    * nuitka
