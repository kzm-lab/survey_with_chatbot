# survey_with_chatbot
論文のサーベイのためにChatBotを使うためのツール群
今のところ、指定フォルダ内の全pdfからテキストを抽出し、まとめるツールsurvey_with_chatbotのみ。

# 使い方
1. 以下のコマンドを実行する

git clone https://github.com/kzm-lab/survey_with_chatbot.git

（Windowsなら、コマンドプロンプトかPowerShellを起動し、適当なディレクトリに移動して、cloneするとそこに「survey_with_chatbot」というディレクトリとファイルができるはずです。そのディレクトリに移動します）

2. OneDriveの木島の「輪講_研究室」ディレクトリをマウント

https://thersacjp-my.sharepoint.com/:f:/g/personal/ff_84d_1367_f_thers_ac_jp/IgBz8YkM7IPBSaln5j9VOFQKAXC2JqaY0Lzxgske6EyHqns?e=KQegYQ

（機構アカウントでログインしている必要があります）
（Web上でアクセスしてからマウントするようです。方法は検索してください）

3. 以下のコマンドを実行する

python pdf2txt_dir_tar_zip.py 処理するフォルダのフルパス

（多分、フォルダをドラッグしてコマンドプロンプトかPowerShellのウィンドウにドラッグするとフルパスが出てくるはず）