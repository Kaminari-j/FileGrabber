import os
from FileGrabber.grabber import FileGrabber
from FileGrabber import converter

if __name__ == '__main__':
    files = FileGrabber.grab_files('https://www.clien.net/service/board/park/13666299?od=T31&po=0&category=&groupCd=')

    for file in files:
        converter.convertFile(file.PATH, converter.TargetFormat.GIF)
        os.remove(file.PATH)
