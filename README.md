
# JBT extract

## これは何?
[日本語大シソーラス](http://www.taishukan.co.jp/item/nihongo_thesaurus/thesaurus.html)のCD-ROMに収録されている辞書形式から，計算機で処理しやすいTSV形式に変換するスクリプト

## 必要なもの
- 生テキストを抽出するためのWindows環境（Linux環境でもwineを用いれば可）
- 日本語大シソーラスのCD
- dessed
- DDwin
- python 2.X

## データ形式の変換
- 日本語大シソーラスをCD-ROMからインストール
- dessedでepwing形式に変換
- DDwinで生テキストへ書き出す
    - DDwinをインストール
    - 「全文検索」で、何も指定せずに検索を実行
    - 編集 -> エディタ起動 -> (出力する内容)該当項目すべて
    - ファイルを適当な場所に保存する
- できるファイルのmd5sumは``3c9782b0998ba0cb0d7ade551eef0231``です
- ``python ./jbt_extract.py body.txt out``のように，変換スクリプトを実行する
- できるファイルのmd5sumは以下のとおりです
```
be5f8549d1054b38f7f89ff3e16a7618  out.category.tsv
ad2bd20ffc0698ab4f2085c20d8bcea5  out.contents.tsv
```

## ファイルのフォーマット

- 公式サイトでは語群(以下では小分類とよぶ)を7分類している
    - I 抽象的関係
    - II 位相・空間
    - III 序と時間
    - IV 人間性
    - V 人間行動
    - VI 社会活動
    - VII 自然と環境
- 語群は小語群(以下では細分類とよぶ)をもつ

### out.category.tsv
```
大分類番号 [TAB] 中分類 [TAB] 小分類番号 [TAB] 小分類名 [TAB] 細分類番号 [TAB] 細分類名
```

### out.contents.tsv
```
小分類番号 [TAB] 細分類番号 [TAB] 項目
```

## TODO
- 細分類ごとに``【関連語】``や``【リスト】``等の付加情報が付いているのが，無視している
- 項目に``→``から始まる他の分類へのリンクがあるが，それを無視している

## License
- General Public License Version3
- Copyright (C) 2014- Yuta Hayashibe

