import sys
import os
import subprocess
import getopt
import plistlib
from pbxproj import XcodeProject
from pbxproj.XcodeProject import *
reload(sys)
sys.setdefaultencoding('utf-8')


projectFile = 'MyJSGame-en.xcodeproj'
projectPath = 'frameworks/runtime-src/proj.ios_mac/'
cocos_root = None;
dependencies_lib = None
working_dir = None
dependencies_lib = ['build/cocos2d_libs.xcodeproj','cocos/scripting/js-bindings/proj.ios_mac/cocos2d_js_bindings.xcodeproj']
build_cmd = 'xcodebuild -project %s -scheme %s -configuration Release -parallelizeTargets -sdk iphoneos -archivePath build/archive archive build -allowProvisioningUpdates'
archive_cmd = 'xcodebuild -exportArchive -exportOptionsPlist %s -archivePath build/archive.xcarchive -exportPath publish/ios -allowProvisioningUpdates'
build_target_name = 'MyJSGame-mobile'
project = None

def run_cmd(command,cwd = None):
    sys.stdout.flush()
    print 'excude command %s' % command
    process = subprocess.Popen(command,shell = True, cwd = cwd,stdout=subprocess.PIPE)
    while True:
        output = process.stdout.readline()
        if output == '' and process.poll() is not None:
            break
        if output:
            print output.strip()
    rc = process.poll()
    return rc;

def setEnviroment():
    try:
        global cocos_root
        global working_dir
        print 'Start Set Environment'
        cocos_root = os.environ['COCOS_X_ROOT']
        print 'COCOS_X_ROOT =' + cocos_root
        working_dir = os.getcwd()
        print working_dir
        run_cmd('sh tools/linkEngine.sh')
    except KeyError ,e:
        print 'Please Set Enviroment COCOS_X_ROOT Point to Engine Directory'
        sys.exit(-1)

def remove_old_build_phase():
    build_phases = project.get_build_phases_by_name('PBXFrameworksBuildPhase')
    file_needRemove = []
    print 'remove old build_phase'
    for build_phase in build_phases:
        file_needRemove = []
        for f in build_phase.files:
            fileStr = '%s' % build_phase.get_parent()[f]
            if fileStr.find('libcocos2d') > 0 or fileStr.find('libjscocos2d') > 0:
                file_needRemove.append(build_phase.get_parent()[f])
        for i in range(len(file_needRemove)):
            fileStr = '%s' % file_needRemove[i]
            result = build_phase.remove_build_file(file_needRemove[i])
            print "remove %s %s" % (fileStr , result)

def remove_old_project_reference():
    print 'remove old project refrence'
    project_files = project.objects.get_objects_in_section(u'PBXFileReference')
    project_file_need_remove = []
    for file in project_files:
        if file.path.find('xcodeproj') > 0:
            project_file.remove(file)

    for file in project_file:
        if file.path.find('xcodeproj') > 0:
            print file

    project_obj = project.objects.get_objects_in_section(u'PBXProject')[0]
    project_references = project_obj.projectReferences
    print project_references

    project_need_remove = [];
    for i in range(len(project_references)):
        project_str = '%s' % project_references[i]
        if project_str.find('cocos2d') > 0:
            project_need_remove.append(project_references[i]);

    for i in range(len(project_need_remove)):
        project_str = '%s' % project_need_remove[i]
        project_references.remove(project_need_remove[i]);
    print 'remove project reference ' + project_str

def add_new_project_reference():
    print 'add new project refrence '
    print cocos_root

    for i in range(len(dependencies_lib)):
        print 'add project ' + (cocos_root + '/' + dependencies_lib[i])
        result = project.add_project(cocos_root + '/' + dependencies_lib[i],force=True)

def remove_not_used_buid_phase():
    print 'remove not used buid phase'
    build_phases = project.get_build_phases_by_name(u'PBXFrameworksBuildPhase')
    for build_phase in build_phases:
        file_needRemove = []
        for f in build_phase.files:
            fileStr = '%s' % build_phase.get_parent()[f]
            #print fileStr
            if fileStr.find('Mac.a') > 0 or fileStr.find('tvOS.a') > 0:
                file_needRemove.append(build_phase.get_parent()[f]);
        for i in range(len(file_needRemove)):
            fileStr = '%s' % file_needRemove[i]
            result = build_phase.remove_build_file(file_needRemove[i])
            print "remove %s %s" % (fileStr , result)

def generate_plist_file():
    plist = dict(
        compileBitcode=False,
        method='enterprise',
        signingStype='automatic',
        stripSwiftSymbols=True,
        teamId='FTCB4GFBRS',
        thinning='<none>'
    )
    plistlib.writePlist(plist,'exportOptions.plist')

def build_ipa():
    generate_plist_file()
    command = build_cmd % (projectPath + projectFile,build_target_name)
    ret = run_cmd(command)
    if ret != 0:
        return ret
    exportOptionsFile = 'exportOptions.plist'
    command = archive_cmd % (exportOptionsFile)
    ret = run_cmd(command)
    return ret
def build_apk():
    command = 'rm -rf frameworks/runtime-src/proj.android/assets'
    ret = run_cmd(command)
    if ret != 0:
        return ret
    command = 'mkdir frameworks/runtime-src/proj.android/assets'
    ret = run_cmd(command)
    if ret != 0:
        return ret
    ret = run_cmd('cocos compile -p android -m release')
    return ret

if __name__ == '__main__':
    setEnviroment()
    if len(sys.argv) <= 1:
        print 'please use command : build_package.py [android | ios]'
        sys.exit(0)

    ios = False
    android = False
    match = False
    args = sys.argv[1:]
    for a in args:
        if a == 'ios':
            ios = True
            match = True
            print 'build ios'
        if a == 'android':
            print 'build android'
            android = True
            match = True

    if match == False:
        print 'please use command : build_package.py [android | ios]'
        sys.exit(0)

    if ios:
        project = XcodeProject.load(projectPath + projectFile + '/project.pbxproj')
        remove_old_build_phase()
        #remove_old_project_reference()
        add_new_project_reference()
        remove_not_used_buid_phase()
        project.save()
        ret = build_ipa()
        if ret != 0:
            sys.exit(ret)
    if android:
        ret = build_apk()
        if ret != 0:
            sys.exit(ret)
    sys.exit(0)

