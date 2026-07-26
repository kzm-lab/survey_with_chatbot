'''
pdfファイルからテキストを抽出する。
モジュールには、PyMuPDF、pikepdf、PyPDF2、pdfrw、pdfplumber/pdfminerなどがあるが、
PyMuPDFが多機能で流行ってるらしいので、これを使ってみる。
テキストブロックの順番がPDFの構造に依存するので、
抽出結果は必ずしも人間が読む順番になっているとは限らない。
要するに変な作り方をしたpdfでは、変な順番でテキストが抽出されるかもしれない。
この辺は、しばらく様子を見て、問題があれば他のモジュールを試すなり、
ブロックの配置を解析して順番を入れ替えるなりする必要があるかもしれない。
'''
import fitz  # PyMuPDF
import os

# テスト用のPDFファイルのパスを指定
pdf_path_test = "/Users/kijima/Library/CloudStorage/OneDrive-国立大学法人東海国立大学機構/輪講_研究室/2024_論文_VR_Sickness_Fujita_IEEE_VR/2023/Mitigation_of_VR_Sickness_During_Locomotion_With_a_Motion-Based_Dynamic_Vision_Modulator.pdf"

if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument("pdf")
    args = parser.parse_args()

    # PDFを開く
    doc = fitz.open(args.pdf)

    # 全ページからテキストを抽出して結合
    full_text = ""
    for page in doc:
        full_text += page.get_text()

    # 抽出結果の表示
    # print(full_text)

    # pdfファイルと同名のテキストファイルに保存
    body, sufx = os.path.splitext(args.pdf)
    fname_out = body+'.txt'
    with open(fname_out, "w", encoding="utf-8") as f:
        f.write(full_text)
