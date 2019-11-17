from FileGrabber import filegrabber


if __name__ == '__main__':
    # Todo: file saving folder
    testurl = r'https://www.clien.net/service/board/park/14290602'
    testurl = input('URL: ').strip()
    filegrabber.do_grab(testurl, True)

