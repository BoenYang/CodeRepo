import sys
from PIL import Image
import os
reload(sys)
sys.setdefaultencoding('utf-8')

sourceFile = 'icon_1024.png'

iosIconDir = '../frameworks/runtime-src/proj.ios_mac/ios/'
iosIconDir1 = '../frameworks/runtime-src/proj.ios_mac/MyJSGame-mobile/Images.xcassets/AppIcon.appiconset/'
androidDir1 = '../frameworks/runtime-src/proj.android/res/drawable-hdpi/'
androidDir2 = '../frameworks/runtime-src/proj.android/res/drawable-ldpi/'
androidDir3 = '../frameworks/runtime-src/proj.android/res/drawable-mdpi/'
androidDir4 = '../frameworks/runtime-src/proj.android/res/drawable-xhdpi/'
newIconImg = Image.open(sourceFile)

def list_icon_in_dir(path):
    files = []
    for f in os.listdir(path):
        file_path = os.path.join(path,f)
        if os.path.isfile(file_path) and os.path.splitext(f)[1] == '.png':
            files.append(file_path)
    return files

def generate_icon_in_dir(path):
    iconList = list_icon_in_dir(path)
    for icon in iconList:
        im = Image.open(icon)
        if im.width == im.height:
            bgImg = Image.new('RGBA',im.size,(255,255,255,0))
            new_photo = newIconImg.copy()
            new_photo.thumbnail((im.width,im.height),Image.ANTIALIAS)
            bgImg.paste(new_photo, (0, 0))
            bgImg.save(icon,'png')
            print 'replace %s' % (icon)

if __name__ == '__main__':
    #os.listdir(iosIconDir1)
    generate_icon_in_dir(iosIconDir)
    generate_icon_in_dir(iosIconDir1)
    generate_icon_in_dir(androidDir1)
    generate_icon_in_dir(androidDir2)
    generate_icon_in_dir(androidDir3)
    generate_icon_in_dir(androidDir4)
