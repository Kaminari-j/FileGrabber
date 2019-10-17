import os
from FileGrabber.filegrabber import grabbers
from FileGrabber.handler import converter


def main(url):
    files = grabbers.grab_files(url)

    for f in files:
        f.print_file()
        if not os.path.exists(f.PATH):
            grabbers.download_file(f)
        if f.EXT == 'mp4':
            converter.convertFile(f.PATH, converter.TargetFormat.GIF)
            os.remove(f.PATH)


if __name__ == '__main__':
    url = 'https://www.clien.net/service/board/park/13670441?od=T31&po=0&category=&groupCd='
    main(url)
