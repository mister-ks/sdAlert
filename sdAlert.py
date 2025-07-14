import time
import threading
from datetime import datetime
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
from playsound import playsound
import os

class ChangeHandler( FileSystemEventHandler ):
    def __init__( self ):
        self.timer = None
        self.delay = 2
        self.lock = threading.Lock()

    def on_any_event( self, event ):
        if event.is_directory:
            return
        self.reset_timer()

    def reset_timer( self ):
        with self.lock:
            if self.timer is not None:
                self.timer.cancel()
            self.timer = threading.Timer( self.delay, self.play_sound )
            self.timer.start()
    # def on_modified( self, event ):
    #    playsound("sdAlert.mp3")

    def play_sound( self ):
        playsound("F:\\Documents\\VSCodeProjects\\pythonbat\\sdAlert\\sdAlert.mp3")

    # def on_deleted( selef, event):
    #    playsound("sdAlert.mp3")

current_date = datetime.now().strftime("%Y-%m-%d")

base_folder = "C:\\Users\\KS-Mk2\\Box\\00900 Kドライブ\\00912 KLドライブ（画像）\\StableDiffusion\\txt2img-images\\003 direct\\"
path_to_watch = os.path.join( base_folder, current_date)

if not os.path.exists( path_to_watch ):
    print( f"エラー：フォルダが存在しません。：{ path_to_watch }" )
else:
    event_handler = ChangeHandler()
    observer = Observer()
    observer.schedule( event_handler, path=path_to_watch, recursive=False )
    
    observer.start()

    try:
        while True:
            time.sleep( 1 )
    except KeyboardInterrupt:
        observer.stop()

    observer.join()