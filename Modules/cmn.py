#encoding=gbk

__author__ = 'bao'
import os
import urllib2
import tarfile
import shutil

def http_get(url, localfile):
    '''
    :param link: http link
    :param localfile: local file to write
    :return: True or False
    '''
    try:
        f = urllib2.urlopen(url)
        data = f.read()
        with open(localfile, "wb") as src:
            src.write(data)
        return True
    except BaseException, ex:
        print 'http_get ' + url + ' error: ', ex
        return False

def tar_compress(tarname, tgtdir):
    try:
        tar = tarfile.open(tarname, "w")
        for root, dir, files in os.walk(tgtdir):
            for file in files:
                fullpath = os.path.join(root, file)
                tar.add(fullpath)
        tar.close()
        return True
    except BaseException, ex:
        print 'tar_compress error: ', ex
        return False

def tar_uncompress(tarname, tgtdir):
    try:
        tar = tarfile.open(tarname)
        names = tar.getnames()
        for name in names:
            tar.extract(name, path=tgtdir)
        tar.close()
        tar.close()
        return True
    except BaseException, ex:
        print 'tar_uncompress error: ', ex
        return False

def move_file(src, dst):
    print 'find  file    :' + src
    print 'move file to  :' + dst
    if os.path.exists(dst):
        #如果目标端有同名文件，将文件改名
        print 'dst file exists, rename to '+ dst + '_bak'
        shutil.move(dst, dst + '_bak')
    shutil.move(src, dst)

if __name__ == '__main__':
    #httpGet('127.0.0.1:8081', '/', './111')
    tar_compress(r"C:\Users\bao\Desktop\CLib4Maven\Modules\apache-maven-3.3.3.tar", r"C:\Users\bao\Desktop\CLib4Maven\Modules\apache-maven-3.3.3")
    tar_uncompress(r"C:\Users\bao\Desktop\CLib4Maven\Modules\apache-maven-3.3.3.tar", r"C:\Users\bao\Desktop\CLib4Maven\Modules\tmp")
