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

（別の日の回答）
| 論文タイトル                                                                                                                            | 使用している指標                                | 用途・測定方法                                                                            |
| --------------------------------------------------------------------------------------------------------------------------------- | --------------------------------------- | ---------------------------------------------------------------------------------- |
| **Virtual reality sickness detection: an approach based on physiological signals and machine learning**                           | 心拍数、心拍変動（HRV）、発汗関連指標（EDA／皮膚コンダクタンス）、BVP | Shimmer GSR+でPPGによる血液容積脈波とEDAを連続測定し、VR酔いを機械学習で推定                                   |
| **Motion Sickness in Virtual Reality: An Empirical Evaluation**                                                                   | 血圧、心拍数、血糖値                              | VR体験の前後に血圧・心拍数・血糖値を測定し、VR環境の種類や主観的酔いとの関係を評価                                        |
| **Evaluation of Eardrum Temperature and Autonomic Nervous Activity by VR Motion Sickness in Amusement Parks VR Attraction**       | 心拍数、心拍変動（RRI、LF、HF、LF/HF）、鼓膜温度、ECG      | ECGと鼓膜温度を測定し、自律神経活動およびVR酔いとの関係を評価                                                  |
| **Evaluation of Simulator Sickness for 360° Videos on an HMD Subject to Participants’ Experience with Virtual Reality**           | 眼球運動・視線、心拍数、GSR（皮膚電気反応）                 | Tobii内蔵アイトラッカー、Shimmer GSRセンサー、PPGセンサーを使用                                          |
| **Real-Time Detection of Simulator Sickness in Virtual Reality Games Based on Players’ Psychophysiological Data during Gameplay** | 眼球運動、EEG                                | HTC Vive Pro Eyeから13種類の眼球運動データを記録し、眼球加速度などを用いてリアルタイム検出。EEGも収集・解析したが、一貫した特徴は得られなかった |
| **The Effect of a Foveated Field-of-view Restrictor on VR Sickness**                                                              | 視線位置、視線分散                               | HTC Vive Pro Eyeの両眼アイトラッカー（120 Hz）で視線を測定。視線分散を眼球行動の指標として使用                         |
| **Estimating VR Sickness Caused by Camera Shake in VR Videography**                                                               | ECG、EEG                                 | 15名からVR映像視聴中のECGと14チャンネルEEGを収集し、VR酔い推定モデルの生理特徴として使用                                |
| **Using EEG and Deep Learning to Predict Motion Sickness**                                                                        | EEG                                     | NeuroSky MindWave Mobileで脳波を記録し、深層学習によってVR酔いを予測                                    |


# テスト環境

手元でのテスト環境は以下の通り

Python 3.14.6

追加したモジュール

pip install fitz

pip install PyMuPDF

# 背景

本当は、ネットワーク上のドライブの中のフォルダを直接指定して、ChatBotに質問をしたり、Exelにサマリーをまとめてもらったりしたい。試したところ、[大学が供給するMS Copilot-Chat, サブスクしているChatGPT Plus, 無料版のGemini flush]x[大学が供給するMS OneDrive for Business, 無料のgoogle drive]のいずれの場合も、ChatBotはネットワーク上のドライブを見ることができなかったため、一手間かけることにした。大学（機構）供給のものは、安全のためアクセス権限が複雑すぎてよくわからない（しかもドライブ側とChatBot側双方）し、無料版は機能制限があるからだろう。AIの提案によれば、APIを使えばできるとのこと。他に、difyという（太平洋工業の大橋氏が使っているといっていた）RAGツールも使えそうなんだが、多少の課金をどう考えるか。

やりたいのは論文の下読み、スクリーニング、exelにまとめること、前読んでも忘れているものをさっと取り出せること。
