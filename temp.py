import os
import sys
import tarfile
import PyPDF2
from pathlib import Path

# PDFファイルからテキストを抽出する


def extract_text_from_pdf(pdf_path):
    text = []
    try:
        with open(pdf_path, 'rb') as file:
            pdf_reader = PyPDF2.PdfReader(file)
            for page_num in range(len(pdf_reader.pages)):
                page = pdf_reader.pages[page_num]
                text.append(page.extract_text())
        # \nでページごとのテキストを結合して返す
        return '\n'.join(text)
    except Exception as e:
        # エラーが発生した場合はファイル名とえらー内容を表示して空文字を返す
        print(f"Error extracting text from {pdf_path}: {e}")
        return ""

# メイン処理


def main(folder_path):
    # 指定されたフォルダのパス文字列をPathオブジェクトに変換
    folder = Path(folder_path)

    # 指定されたフォルダが存在するか確認
    if not folder.exists():
        print(f"Error: Folder {folder_path} does not exist")
        sys.exit(1)

    # PDFファイルのリストを探す
    pdf_files = list(folder.glob("*.pdf"))

    # １つもPDFファイルが見つからなかった場合は終了
    if not pdf_files:
        print(f"No PDF files found in {folder_path}")
        return

    # 抽出したテキストを保存する.txtファイル名のリスト
    txt_files = []

    # 各PDFファイルからテキストを抽出して.txtファイルを作成
    for pdf_file in pdf_files:
        print(f"Processing {pdf_file.name}...")
        text = extract_text_from_pdf(pdf_file)

        # 同名の.txtファイルを作成
        txt_file = pdf_file.with_suffix('.txt')
        with open(txt_file, 'w', encoding='utf-8') as f:
            f.write(text)

        txt_files.append(txt_file)
        print(f"Created {txt_file.name}")

    # .txtファイルをtar.gzで圧縮
    # Pathオブジェクト特有の書き方でtar.gzファイルのパスを作成
    tar_gz_path = folder / "all.txt.tar.gz"
    print(f"\nCreating {tar_gz_path.name}...")

    with tarfile.open(tar_gz_path, "w:gz") as tar:
        for txt_file in txt_files:
            tar.add(txt_file, arcname=txt_file.name)

    print(f"Successfully created {tar_gz_path.name}")


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python temp.py <folder_path>")
        sys.exit(1)

    folder_path = sys.argv[1]
    main(folder_path)
