# coding:utf-8

import requests
import os
import plistlib
import sys
import xml.dom.minidom as xmldom
import ConfigParser

reload(sys)
sys.setdefaultencoding('utf-8')

url = 'https://ios.supernano.com/game/upload_file.php'
apk_dir = 'publish/android/'
ipa_dir = 'publish/ios/'
plist_file_dir = 'frameworks/runtime-src/proj.ios_mac/ios/'
buid_xml_file_dir = 'frameworks/runtime-src/proj.android/'
ipa_name = 'MyJSGame-mobile.ipa'

if __name__ == '__main__':
    conf = None
    if os.path.exists('upload.conf'):
        conf = ConfigParser.ConfigParser()
        conf.read('upload.conf')
    else:
        print 'please create a upload.conf in project dir'
        print '[upload]'
        print 'project_en_name = your upload english name'
        print 'project_zh_name = your upload chinese name'
        sys.exit(-1)

    prject_en_name = conf.get('upload','project_en_name')
    prject_zh_name = conf.get('upload','project_zh_name')
    data = {'projname' : prject_en_name, 'projchname' : prject_zh_name}
    build_xml = xmldom.parse(buid_xml_file_dir + "build.xml")

    elementObj = build_xml.documentElement
    apk_name = elementObj.getAttribute('name') + '-release-signed.apk'
    apk_path = apk_dir + apk_name

    plist = None
    plist_file_path = None
    if os.path.exists(plist_file_dir + 'Info-en.plist'):
        plist_file_path = plist_file_dir + 'Info-en.plist'
    elif os.path.exists(plist_file_dir + 'Info.plist'):
        plist_file_path = plist_file_dir + 'Info.plist'
    else:
        print 'can not fount plist in ' + plist_file_dir
        sys.exit(-1)
    ios_package = None
    plist = plistlib.readPlist(plist_file_path)
    if  'CFBundleURLTypes' in plist.keys():
        CFBundleURLTypes = plist['CFBundleURLTypes']
        if len(CFBundleURLTypes) >= 2 and 'CFBundleURLName' in CFBundleURLTypes[1]:
            ios_package = CFBundleURLTypes[1]['CFBundleURLName']
        else:
            print 'can not found CFBundleURLName in ' + plist_file_path
            sys.exit(-1)
    else:
        print 'can not found key CFBundleURLTypes in ' + plist_file_path
        sys.exit(-1)

    ipa_path = ipa_dir + ipa_name
    files = {}
    if os.path.exists(apk_path):
        files['file1'] = (apk_name,open(apk_path,'rb'))
    if os.path.exists(ipa_path):
        files['file2'] = (ipa_name,open(ipa_path,'rb'))
        data['bundleid'] = ios_package
    print data
    r = requests.post(url,data,files = files)
    r.encoding = 'utf-8'
    print r.text
    


