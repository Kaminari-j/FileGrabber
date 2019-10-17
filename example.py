from FileGrabber import filegrabber


if __name__ == '__main__':
    # Todo: file saving folder
    testurl = r'https://www.clien.net/service/board/park/14155846?po=0&sk=title&sv=gif&groupCd=&pt=0'
    filegrabber.do_grab(testurl, False)
