import sys
import os
import shutil
import re
import xml.dom.minidom as xmldom
reload(sys)
sys.setdefaultencoding('utf-8')

template_project_path = 'templates\\js-template-default\\frameworks\\runtime-src\\proj.android-studio'
cocos_root = None
working_dir = None
wokring_android_studio_dir = 'frameworks\\runtime-src\\proj.android-studio'
wokring_eclipse_dir = 'frameworks\\runtime-src\\proj.android'


def copy_android_studio_template():
    print 'copy_android_studio_template'
    srcDir = cocos_root + '\\' + template_project_path
    dstDir = working_dir + '\\' + wokring_android_studio_dir
    if(os.path.exists(dstDir)):
        shutil.rmtree(dstDir)
    shutil.copytree(srcDir,dstDir)


def copy_android_manifest():
    print 'copy_android_manifest'
    srcFile = working_dir +  '\\' + wokring_eclipse_dir + '\\AndroidManifest.xml'
    dstFile = working_dir + '\\' + wokring_android_studio_dir + '\\app\\AndroidManifest.xml'
    shutil.copy(srcFile,dstFile)


def copy_src():
    print 'copy_src'
    srcDir = working_dir + '\\' + wokring_eclipse_dir + '\\src'
    dstDir = working_dir + '\\' + wokring_android_studio_dir + '\\app\\src'
    shutil.rmtree(dstDir)
    shutil.copytree(srcDir,dstDir)


def copy_libs():
    print 'copy_libs'
    srcDir = working_dir + '\\' + wokring_eclipse_dir + '\\libs'
    dstDir = working_dir + '\\' + wokring_android_studio_dir + '\\app\\libs'
    if(os.path.exists(dstDir)):
        shutil.rmtree(dstDir)
    shutil.copytree(srcDir,dstDir)


def copy_jin():
    print 'copy_jin'
    srcDir = working_dir + '\\' + wokring_eclipse_dir + '\\jni'
    dstDir = working_dir + '\\' + wokring_android_studio_dir + '\\app\\jni'
    if(os.path.exists(dstDir)):
        shutil.rmtree(dstDir)
    shutil.copytree(srcDir,dstDir)


def copy_res():
    print 'copy_res'
    srcDir = working_dir + '\\' + wokring_eclipse_dir + '\\res'
    dstDir = working_dir + '\\' + wokring_android_studio_dir + '\\app\\res'
    shutil.rmtree(dstDir)
    shutil.copytree(srcDir,dstDir)


def copy_keystore():
    pass


def copy_gradle_properties():
    pass


def modify_gradle_project_name():
    print 'modify_gradle_project_name'
    project_name = get_project_name()
    settingGradlePath = working_dir + '\\' + wokring_android_studio_dir + '\\settings.gradle'
    f = open(settingGradlePath,'r+')
    content = f.read()
    newContent = re.sub('HelloJavascript',project_name,content)
    f.seek(0)
    f.truncate()
    f.write(newContent)
    f.flush()
    f.close()


def modify_gradle_version():
    print 'modify_gradle_version'
    gradlePropertiesPath = working_dir + '\\' + wokring_android_studio_dir + '\\gradle\\wrapper\\gradle-wrapper.properties'
    f = open(gradlePropertiesPath,'r+')
    content = f.read()
    newContent = re.sub('gradle-.*zip','gradle-3.3-all.zip',content)
    f.seek(0)
    f.truncate()
    f.write(newContent)
    f.flush()
    f.close()
    buildGradlePath = working_dir + '\\' + wokring_android_studio_dir + '\\build.gradle'
    f = open(buildGradlePath,'r+')
    content = f.read()
    newContent = re.sub('gradle:1\.3\.0','gradle:2.3.2',content)
    f.seek(0)
    f.truncate()
    f.write(newContent)
    f.flush()
    f.close()

def remove_libcocos2dx_dependence():
    print 'remove_libcocos2dx_dependence'
    settingGradlePath = working_dir + '\\' + wokring_android_studio_dir + '\\settings.gradle'
    f = open(settingGradlePath,'r+')
    content = ""
    for line in f:
        if line.find(':libcocos2dx') > 0:
            continue
        content += line
    f.seek(0)
    f.truncate()
    f.write(content)
    f.flush()
    f.close()

def modify_android_mk():
    print 'modify_android_mk'
    makeFilePath =  working_dir + '\\' + wokring_android_studio_dir + '\\app\\jni\\Android.mk'
    f = open(makeFilePath,'r+')
    content = f.read()
    newContent = re.sub('\.\.\/.\.\/','../../../',content)
    f.seek(0)
    f.write(newContent)
    f.flush()
    f.close()


def get_project_name():
    buid_xml_file_dir = working_dir + '\\' + wokring_eclipse_dir + '\\build.xml'
    build_xml = xmldom.parse(buid_xml_file_dir)
    elementObj = build_xml.documentElement
    project_name = elementObj.getAttribute('name')
    return project_name


def get_package_info():
    manifest_file_path = working_dir + '\\' + wokring_eclipse_dir + '\\AndroidManifest.xml'
    manifest_xml = xmldom.parse(manifest_file_path)
    elementObj = manifest_xml.documentElement
    package_name = elementObj.getAttribute('package')
    version_code = elementObj.getAttribute('android:versionCode')
    version_name = elementObj.getAttribute('android:versionName')
    return package_name,version_code,version_name


def modify_gradle_package_name():
    print 'modify_gradle_package_name'
    package_name,version_code,version_name = get_package_info()
    app_build_gradle_path = working_dir + '\\' + wokring_android_studio_dir + '\\app\\build.gradle'
    f = open(app_build_gradle_path,'r+')
    content = ""
    for line in f:
        if line.find('applicationId') > 0:
            line = line.replace('org.cocos2dx.hellojavascript',package_name)
        if line.find('versionCode') > 0:
            line = line.replace('1',version_code)
        if line.find('versionName') > 0:
            line = line.replace('1.0',version_name)
        if line.find(':libcocos2dx') > 0:
            continue
        content += line
    f.seek(0)
    f.truncate()
    f.write(content)
    f.flush()
    f.close()

def init_env():
    try:
        global cocos_root
        global working_dir
        print 'start init'
        cocos_root = os.environ['COCOS_X_ROOT']
        print 'COCOS_X_ROOT =' + cocos_root
        working_dir = os.getcwd()
        print 'working dir =' + working_dir
        print 'init complete'
    except KeyError ,e:
        print 'Please Set Enviroment COCOS_X_ROOT Point to Engine Directory'
        sys.exit(-1)


if __name__ == '__main__':
    init_env()
    copy_android_studio_template()
    copy_android_manifest()
    copy_src()
    copy_res()
    copy_libs()
    copy_jin()
    modify_android_mk()
    modify_gradle_project_name()
    modify_gradle_version()
    get_package_info()
    modify_gradle_package_name()
    remove_libcocos2dx_dependence()
