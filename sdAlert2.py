import time
import threading
from datetime import datetime
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
import pygame
import os

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
        # print(f"ファイル変更検知: {event.src_path}")  # デバッグ用
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
        # print("通常の通知音を再生します")  # デバッグ用メッセージ
        pygame.mixer.music.load("F:\\Documents\\VSCodeProjects\\pythonbat\\sdAlert\\sdAlert.mp3")  # 通常の通知音ファイル
        pygame.mixer.music.set_volume(1.0)  # 音量を50%に設定
        pygame.mixer.music.play()

    def play_inactivity_sound(self):
        # print("一定時間変化がないため、専用の通知音を再生します")  # デバッグ用メッセージ
        pygame.mixer.music.load(self.inactivity_sound)  # 無変化通知音ファイル
        pygame.mixer.music.set_volume(1.2)  # 無変化通知音の音量を70%に設定
        pygame.mixer.music.play()

# 現在の日付フォルダを監視
current_date = datetime.now().strftime("%Y-%m-%d")

# 監視するフォルダのパス
base_folder = "C:\\Users\\KS-Mk2\\Box\\00900 Kドライブ\\00912 KLドライブ（画像）\\StableDiffusion\\txt2img-images\\003 direct\\"
path_to_watch = os.path.join(base_folder, current_date)

# 無変化時間（例: 3600秒 = 1時間）
inactivity_duration = 180  # 秒単位

# 専用通知音ファイルのパス
inactivity_sound = "F:\\Documents\\VSCodeProjects\\pythonbat\\sdAlert\\sdAlert2.mp3"

# フォルダが存在するか確認
if not os.path.exists(path_to_watch):
    print(f"エラー：フォルダが存在しません: {path_to_watch}")
else:
    # 監視設定
    event_handler = ChangeHandler(inactivity_duration, inactivity_sound)
    observer = Observer()
    observer.schedule(event_handler, path=path_to_watch, recursive=False)

    # 監視開始
    observer.start()

    try:
        while True:
            time.sleep(10)
    except KeyboardInterrupt:
        observer.stop()

    observer.join()
