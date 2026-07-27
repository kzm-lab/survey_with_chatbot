# survey_with_chatbot
論文のサーベイのためにChatBotを使うためのツール群
今のところ、指定フォルダ内の全pdfからテキストを抽出し、まとめるツールsurvey_with_chatbotのみ。

# 使い方
1. 以下のコマンドを実行する

git clone https://github.com/kzm-lab/survey_with_chatbot.git

Windowsなら、コマンドプロンプトかPowerShellを起動し、適当なディレクトリに移動して、cloneするとそこに「survey_with_chatbot」というディレクトリとファイルができるはずです。そのディレクトリに移動します

2. OneDriveの木島の「輪講_研究室」ディレクトリをマウント

URLはDiscordの「研究室員への通知」に、最近だと7/21の投稿にあります。
・機構アカウントでログインしている必要があります
・Web上でアクセスしてからマウントするようです。方法は検索してください

3. 以下のコマンドを実行する

python pdf2txt_dir_tar_zip.py 処理するフォルダのフルパス

多分、フォルダをドラッグしてコマンドプロンプトかPowerShellのウィンドウにドラッグするとフルパスが出てくるはず。

4.  ChatGPTなどにall_text_files.tar.gzを食わせて質問

指定したフォルダにall_text_files.tar.gzができているので、これをChatBotのウィンドウにドラッグ＆ドロップする。
例えば、「これらの論文のテキストファイルから、VR酔いに関連し、眼球運動や血圧、心拍変動などの生理指標を利用しているもののタイトルをあげてください。」などのプロンプトを与える。
（回答例）１分弱かかりました
| 論文タイトル                                                                                                                      | 使用している主な生理指標                |
| --------------------------------------------------------------------------------------------------------------------------- | --------------------------- |
| **Impact of Visually Induced Motion Sickness from VR Depending on Viewing Patterns, View Movement and Background Motion**   | ECG、心拍R–R間隔、LF/HF、呼吸        |
| **A Physiological Approach of Presence and VR Sickness in Simulated Teleoperated Social Tasks**                             | EEG、皮膚コンダクタンス反応（SCR）、心拍、皮膚温 |
| **Assessment and Quantification of Virtual Reality Induced Sickness in Relation to Age and Gender: A Multi-Modal Approach** | 心拍変動（HRV）、皮膚電気活動（EDA）       |
| **Real-Time Prediction of Simulator Sickness in Virtual Reality Games**                                                     | アイトラッキング、瞬目時間、注視時間などの眼球運動   |
| **Reducing VR Sickness by Directing User Gaze to Motion Singularity Point Region as Effective Rest Frame**                  | アイトラッキング、視線位置・注視パターン        |
| **Assessment of Virtual Reality Motion Sickness Severity Based on EEG via LSTM/BiLSTM**                                     | EEG                         |
| **An EEG-based Experiment on VR Sickness and Postural Instability While Walking in Virtual Environments**                   | EEG、全身モーションキャプチャによる姿勢・歩行指標  |
| **Resting-state EEG in the Vestibular Region Can Predict Motion Sickness Induced by a Motion-Simulated in-car VR Platform** | 安静時EEG、瞳孔計測、前額部PPG、心拍       |
| **Virtual Reality Sickness Reduces Attention During Immersive Experiences**                                                 | EEG／事象関連電位（P3b）             |
| **Exploring Neural Biomarkers in Young Adults Resistant to VR Motion Sickness: A Pilot Study of EEG**                       | EEG（EOGは眼球運動ノイズ除去用）         |


# テスト環境

手元でのテスト環境は以下の通り
Python 3.14.6
追加したモジュール
pip install fitz
pip install PyMuPDF
