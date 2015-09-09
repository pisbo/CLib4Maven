#encoding=gbk
__author__ = 'bao'

import os
import shutil
from xml.dom.minidom import parse as xmlparse
from cmn import http_get, tar_uncompress, move_file


class CMavenArtifact(object):
    def __init__(self, groupid=None, artifactid=None, version=None, includepath=None, libpath=None, packaging='tar'):
        self.groupid = groupid
        self.artifactid = artifactid
        self.version = version
        self.packaging = packaging
        self.includepath = includepath
        self.libpath = libpath

    def show(self):
        print '*' * 20 + str(self.__class__.__name__).center(30) + '*' * 20
        for k, v in vars(self).items():
            print k.ljust(20) + ':', v


class CPom(CMavenArtifact):
    def __init__(self, xmlfile):
        self.xml = xmlfile
        self.dependencies = []
        self.file = None
        self.loadxml()

    def loadxml(self, xmlfile=None):
        localnotfound = False
        includepath = './include'
        libpath = './lib'
        packaging = 'tar'
        local = None
        tmpxml = self.xml
        if xmlfile:
            tmpxml = xmlfile

        dom = xmlparse(tmpxml)
        root = dom.documentElement
        try:
            # Ĭ��ȡ��һ��ȡ�õ�ֵ
            self.groupid = root.getElementsByTagName('groupId')[0].firstChild.data
            self.artifactid = root.getElementsByTagName('artifactId')[0].firstChild.data
            self.version = root.getElementsByTagName('version')[0].firstChild.data
            self.packaging = root.getElementsByTagName('packaging')[0].firstChild.data

            # �ϴ�Maven�⣬��Ҫfile��Դtar��
            files = root.getElementsByTagName('file')
            if files is not None and len(files) > 0:
                self.file = files[0].firstChild.data

            # ����Maven�⣬��Ҫdependices������
            dependencies = root.getElementsByTagName('dependencies')[0]
            locals = root.getElementsByTagName('local')

            if locals is None or len(locals) <= 0:
                localnotfound = True
            else:
                # ����default��local��ַ
                local = locals[0]
                defaultlocals = local.getElementsByTagName('default')
                if defaultlocals is None or len(defaultlocals) <= 0:
                    localnotfound = True
                else:
                    includepath = defaultlocals[0].getElementsByTagName('include')[0].firstChild.data
                    libpath = defaultlocals[0].getElementsByTagName('lib')[0].firstChild.data

            for depend in dependencies.getElementsByTagName('dependency'):
                try:
                    tmpinclude = includepath
                    tmplib = libpath
                    groupid = depend.getElementsByTagName('groupId')[0].firstChild.data
                    artifactid = depend.getElementsByTagName('artifactId')[0].firstChild.data
                    version = depend.getElementsByTagName('version')[0].firstChild.data
                    types = depend.getElementsByTagName('type')
                    if types and len(types) > 0:
                        # type�Ǳ��룬�����Ĭ��ֵtar
                        packaging = types[0].firstChild.data
                    if groupid is None or artifactid is None or version is None or \
                                    len(groupid) <= 0 or len(artifactid) <= 0 or len(version) <= 0:
                        continue
                    # Ѱ��path
                    if not localnotfound and local:
                        # ������Ƿ����ض�����
                        speclocals = local.getElementsByTagName(artifactid)
                        if speclocals and len(speclocals) > 0:
                            tmpinclude = speclocals[0].getElementsByTagName('include')[0].firstChild.data
                            tmplib = speclocals[0].getElementsByTagName('lib')[0].firstChild.data

                    arti = CMavenArtifact(groupid, artifactid, version, tmpinclude, tmplib, packaging)
                    self.dependencies.append(arti)
                except BaseException, ex:
                    print 'loadXml depend error : ', ex
                    continue
        except BaseException, ex:
            print 'loadXml error : ', ex

    def show(self):
        super(CPom, self).show()
        for d in self.dependencies:
            d.show()


class Repo(CMavenArtifact):
    def __init__(self, url=None, repoid=None, xml=None):
        if xml is None:
            self.url = url
            self.id = repoid
        else:
            self.loadxml(xml)

    def loadxml(self, xml):
        dom = xmlparse(xml)
        root = dom.documentElement
        try:
            # Ĭ��ȡ��һ��ȡ�õ�ֵ
            self.url = root.getElementsByTagName('url')[0].firstChild.data
            self.id = root.getElementsByTagName('id')[0].firstChild.data
        except BaseException, ex:
            print 'loadXml error : ', ex


class CMavenCtrl():
    '''
        Maven controller
        deploy and get 3rd libs
    '''

    def __init__(self, pomxml, url=None, repoid=None, repoxml=None):
        if repoxml is None and url is not None and repoid is not None:
            self.repo = Repo(url=url, repoid=repoid)
        elif repoxml is not None:
            self.repo = Repo(xml=repoxml)
        else:
            self.repo = Repo(xml=pomxml)
        self.pom = CPom(pomxml)

    def put(self):
        cmd = r'mvn deploy:deploy-file -DgroupId={0:s} -DartifactId={1:s} -Dversion={2:s} -Dpackaging={3:s} -Dfile={4:s} -Durl={5:s} -DrepositoryId={6:s}'.format(
            self.pom.groupid, self.pom.artifactid, self.pom.version, self.pom.packaging, self.pom.file,
            self.repo.url, self.repo.id
        )
        print 'cmd : ' + cmd
        os.system(cmd)

    def get(self):
        # ��ʱ����·�����ݶ�Ϊ��ǰĿ¼�µ�tmp_+������Ŀ��artifactid
        tmpdir = os.path.join('.', 'tmp_' + self.pom.artifactid)
        if os.path.exists(tmpdir):
            shutil.rmtree(tmpdir, True)
        os.makedirs(tmpdir)

        for d in self.pom.dependencies:
            target = '/'.join([d.groupid, d.artifactid, d.version, d.artifactid + '-' + d.version + '.' + d.packaging])
            #Ĭ�����ص�������ʱĿ¼��
            tarname = '/'.join([tmpdir, target.split('/')[-1]])
            print 'get file from   :', '/'.join([self.repo.url, target])
            print 'retrieve file to:', tarname
            http_get('/'.join([self.repo.url, target]), tarname)

            if os.path.exists(tarname):
                if d.packaging == 'tar':
                    if not os.path.exists(d.includepath):
                        os.makedirs(d.includepath)
                    if not os.path.exists(d.libpath):
                        os.makedirs(d.libpath)
                    # ���ڽ�֧��tar,��ѹ��������ʱĿ¼���ͬ���ļ�����
                    tmptardir = os.path.join(tmpdir, target.split('/')[-1].split('.')[0])
                    os.makedirs(tmptardir)
                    print 'start to uncompress ' + tarname
                    tar_uncompress(tarname, tmptardir)

                    # �������ý�include��lib�ֱ����ָ��λ��
                    for root, dir, files in os.walk(tmptardir):
                        for file in files:
                            fullpath = os.path.join(root, file)
                            if file.endswith('.h'):
                                move_file(fullpath, os.path.join(d.includepath, file))
                            elif file.endswith('.a') or file.endswith('.so'):
                                move_file(fullpath, os.path.join(d.libpath, file))

                else:
                    print 'get ', tarname, ' , it is not tar'


if __name__ == '__main__':
    cc = CMavenCtrl(r'C:\Users\bao\PycharmProjects\CLib4Maven\Modules\cpom.xml')
    cc.pom.show()
    cc.repo.show()
    cc.get()
    #cc.put()
