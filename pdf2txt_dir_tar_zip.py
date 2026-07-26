'''
指定されたフォルダにあるすべてのpdfについて、pdf2txt_simple.pyを実行する
'''
import os
import subprocess

if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument("dir")
    args = parser.parse_args()

    # 指定されたディレクトリ内のすべてのPDFファイルを取得
    pdf_files = [f for f in os.listdir(args.dir) if f.endswith('.pdf')]

    # 各PDFファイルに対してpdf2txt_simple.pyを実行
    for pdf_file in pdf_files:
        pdf_full_path = os.path.join(args.dir, pdf_file)
        subprocess.run(["python", "pdf2txt_simple.py", pdf_full_path])

    # このディレクトリの全ての.txtファイルをtarで固める
    txt_files = [f for f in os.listdir(args.dir) if f.endswith('.txt')]
    if txt_files:
        tar_path = os.path.join(args.dir, "all_text_files.tar")
        subprocess.run(["tar", "-cvf", tar_path] + txt_files, cwd=args.dir)

    # tarballをgunzipで圧縮する
    if os.path.exists(tar_path):
        subprocess.run(["gzip", tar_path])
