import os
from FileGrabber import FileGrabber
from InfoClass import FileInfo
import converter

if __name__ == '__main__':
    files = FileGrabber.grab_files('https://www.clien.net/service/board/park/13653872')

    for file in files:
        converter.convertFile(file.PATH, converter.TargetFormat.GIF)
        os.remove(file.PATH)
