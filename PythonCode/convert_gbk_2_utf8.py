import sys
import os
import chardet
import codecs
reload(sys)
sys.setdefaultencoding('utf-8')

dir1 = "../frameworks/runtime-src/proj.android-studio/app/src/"
   

def convert_gbk_2_utf8(dir):
    for f in os.listdir(dir):
        file_path = os.path.join(dir,f)
        if os.path.isdir(file_path):
            convert_gbk_2_utf8(file_path)
        elif os.path.splitext(f)[1] == '.java':
            f = open(file_path,'r+')
            content = f.read()
            f.close()
            source_encoding = chardet.detect(content)['encoding']
            print source_encoding , file_path
            if source_encoding != 'utf-8':
                content = content.decode(source_encoding, 'ignore') #.encode(source_encoding)
                codecs.open(file_path, 'w', encoding='UTF-8').write(content)
            

if __name__ == '__main__':
    convert_gbk_2_utf8(dir1)
