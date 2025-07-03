# physical_examination
## 概要
本プログラムの目的は，動画データによりフレームごとに活動量に応じた活動量について算出し，動作の特徴について調査することである．
具体的には，主に2つのプログラムで 構成されている．
+ 特定のフレームの動画を切り抜く．
+ 入力した動画についてフレームごとに活動量を算出して出力する．
  
また，デモとして PC から動画を撮影し，ゲージとして可視化した活動量を動画として出力する機能も用意した．
## ファイル，ディレクトリ一覧
+ README.md
    + このファイル
+ detect.track.py
    + 動画データを入力することで，指定した評価値に従って活動量を算出し，表示するプログラム
+ show_cutout.py
    + 動画データを入力し，フレームを指定することで指定フレーム内の動画を表示するプログラム
+ demo.py
    + カメラから動画を撮影し，ゲージとして可視化した活動量を動画として送信するプログラム
+ input_video/
    + 読み込む動画データを格納する．入力データに指定がない場合，このディレクトリ直下の input_video.mp4 が指定される．
+ output_video/
    + 活動量を描画した動画データを出力する際に指定がない場合，このディレクトリに保存される．
+ output_csv/
    + 活動量を csv に出力する際に指定がない場合，このディレクトリに保存される．
+ model/
    + detect.track.py で用いる物体検出モデルを保存するディレクトリ．(使用するモデルに指定がない場合，このディレクトリの yolov8n.pt が使用される．)
+ requirements.txt
    + Docker を用いない場合に，環境構築で使用する．
+ Dockerfile
    + Docker を用いて環境構築を行う際に使用する．

## 使用方法
### show_cutout.py
python3 show_cutout.py [-h] [--start STARTFRAME] [--end ENDFRAME] [--save] --input INPUTDATA
+ optional arguments:
  + -h, --help
    + Show this help message and exit
  + --start STARTFRAME
    + Set start of frame (frame_number default: 0)
  + --end ENDFRAME
    + Set end of frame (frame_number default: end_of_input_data)
  + --save
    + Save showed data
  + --input INPUTDATA
    + Imput file (mp4_filename)

### detect_track.py
python3 detect_track.py [-h] [--fps FPS] [--framesize SIZE]  [--type DETECTTYPE] [--limit DETECTEDPEOPLE]
[--model MODEL] [--outlier VALIDATION] [--save_csv CSVFILE] [--save_mov OUTPUTDATA] --input INPUTDATA
+ optional arguments:
  + -h, --help
    + Show this help message and exit
  + --fps FPS
    + Set FPS (default: 20)
  + --framesize SIZE
    + Set width and heigh of framesize (default: '1920,1080')
  + --type DETECTTYPE
    + Set evaluation (default: 1)
  + --limit DETECTEDPEOPLE
    + Set numuber of detected people (default: 100000)
  + --model MODEL
    + Set model_data (default: 'model/yolov8n.pt')
  + --outlier VALIDATION
    + Set validation (default: 1000)
  + --save_csv CSVFILE
    + Save result to csv (dedault: 'output_csv/{datetime}.csv')
  + --save_mov OUTPUTDATA
    + Save result to mp4 (dedault: 'output_data/{datetime}.mp4')
  + --input INPUTDATA
    + Imput file (mp4_filename)


## 環境構築
### Dockerを使用する場合

```bash
docker build -t healthy-detection:demo .
xhost +
docker run --rm \
    -e DISPLAY -v /tmp/.X11-unix:/tmp/.X11-unix \
    --device /dev/video0:/dev/video0:rwm \
    healthy-detection:demo
```
### Dockerを使用しない場合
1. python3.11.3 のインストール
2. import のためのインストール
```pip3 install -r requirements.txt```

## 実行環境
+ 実行環境
    + Python 3.11.3
    + ライブラリ
      + cv2
      + mediapipe
      + csv
      + datetime
      + argparse
      + RawTextHelpFormatter
