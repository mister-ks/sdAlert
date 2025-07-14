import time
import threading
from datetime import datetime
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
import pygame
import os
import sys

class ChangeHandler(FileSystemEventHandler):
    def __init__(self, inactivity_duration, inactivity_sound):
        self.timer = None
        self.inactivity_timer = None
        self.delay = 2  # 通常の通知音までの待機時間
        self.inactivity_duration = inactivity_duration  # フォルダに変化がない場合の時間（秒単位）
        self.inactivity_sound = inactivity_sound  # 一定時間変化がない場合の通知音
        self.lock = threading.Lock()
        self.start_inactivity_timer()
        pygame.mixer.init()  # Pygameの音声ミキサーを初期化

    def on_any_event(self, event):
        if event.is_directory:
            return
        self.reset_timer()  # 通常の通知音のためのタイマーをリセット
        self.reset_inactivity_timer()  # フォルダの無変化監視タイマーもリセット

    def reset_timer(self):
        with self.lock:
            if self.timer is not None:
                self.timer.cancel()
            self.timer = threading.Timer(self.delay, self.play_sound)
            self.timer.start()

    def reset_inactivity_timer(self):
        with self.lock:
            if self.inactivity_timer is not None:
                self.inactivity_timer.cancel()
            self.start_inactivity_timer()

    def start_inactivity_timer(self):
        # フォルダに一定時間変化がない場合の通知音を鳴らすタイマー
        self.inactivity_timer = threading.Timer(self.inactivity_duration, self.play_inactivity_sound)
        self.inactivity_timer.start()

    def play_sound(self):
        pygame.mixer.music.load("F:\\Documents\\VSCodeProjects\\pythonbat\\sdAlert\\sdAlert.mp3")  # 通常の通知音ファイル
        pygame.mixer.music.set_volume(1.0)
        pygame.mixer.music.play()

    def play_inactivity_sound(self):
        pygame.mixer.music.load(self.inactivity_sound)  # 無変化通知音ファイル
        pygame.mixer.music.set_volume(1.0)
        pygame.mixer.music.play()

# 監視するフォルダのパス
current_date = datetime.now().strftime("%Y-%m-%d")
base_folder = "C:\\Users\\KS-Mk2\\Box\\00900 Kドライブ\\00912 KLドライブ（画像）\\StableDiffusion\\txt2img-images\\003 direct\\"
path_to_watch = os.path.join(base_folder, current_date)

# 無変化時間（例: 3600秒 = 1時間）
inactivity_duration = 80  # 秒単位
inactivity_sound = "F:\\Documents\\VSCodeProjects\\pythonbat\\sdAlert\\sdAlert2.mp3"

# フォルダが存在するか確認
if not os.path.exists(path_to_watch):
    print(f"エラー：フォルダが存在しません: {path_to_watch}")
    sys.exit()

# 監視の設定
event_handler = ChangeHandler(inactivity_duration, inactivity_sound)
observer = Observer()
observer.schedule(event_handler, path=path_to_watch, recursive=False)
observer.start()

# 指定の終了時刻を設定（例: 23:59）
end_time = datetime.now().replace(hour=23, minute=59, second=0, microsecond=0)
if datetime.now() >= end_time:
    end_time = end_time.replace(day=end_time.day + 1)

print(f"スクリプトは {end_time.strftime('%H:%M:%S')} に終了します。")

# メインループで監視と終了時刻のチェックを同時に行う
try:
    while True:
        # 現在時刻が終了時刻を超えたかどうかをチェック
        if datetime.now() >= end_time:
            print("指定した時刻になったのでスクリプトを終了します。")
            break  # ループを抜けて終了処理へ

        # メインの処理（例として10秒ごとに待機）
        time.sleep(10)
except KeyboardInterrupt:
    print("中断されました。")

# クリーンアップ
observer.stop()
observer.join()
pygame.mixer.quit()  # Pygameのミキサーを終了
