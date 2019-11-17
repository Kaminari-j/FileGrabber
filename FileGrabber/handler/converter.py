import imageio
import os
import sys


class TargetFormat(object):
    GIF = ".gif"
    MP4 = ".mp4"
    AVI = ".avi"


# Todo : reduce file size by adjust quality
def convertFile(inputpath, targetFormat, outputpath=None):
    """Reference: http://imageio.readthedocs.io/en/latest/examples.html#convert-a-movie"""
    outputpath = os.path.splitext(inputpath)[0] + targetFormat if outputpath is None else outputpath
    # print("converting\r\n\t{0}\r\nto\r\n\t{1}".format(inputpath, outputpath))
    print("converting {0} to {1}".format(inputpath, outputpath))

    reader = imageio.get_reader(inputpath)
    fps = reader.get_meta_data()['fps']

    writer = imageio.get_writer(outputpath, fps=fps)
    for i, im in enumerate(reader):
        sys.stdout.write("\rframe {0}".format(i))
        sys.stdout.flush()
        writer.append_data(im)
    print("\r\nFinalizing...")
    writer.close()
    print("Done.")


if __name__ == '__main__':
    # convertFile(r'C:\Users\Panasonic\Downloads\test.mp4', TargetFormat.GIF)
    convertFile(r'https://cdn.clien.net/web/api/file/F01/8476193/16920f49a7fe44.mp4', TargetFormat.GIF,
                r'C:\Users\Panasonic\Downloads\test2.gif')
