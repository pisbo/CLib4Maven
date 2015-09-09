沿用MAVEN的项目pom.xml，并添加一些个性化节点（暂定为cpom.xml）。
1、工具上传LIB时，根据cpom.xml中groupid, artifactid, version三维坐标，并根据私有仓库配置url, repoid，生成MAVEN上传deploy的命令行system执行
2、工具下载LIB时，根据cpom.xml中的dependencies中配置的依赖项LIBS，分别连接MAVEN私有仓库的http服务器逐一获取tar包（上传时，packaging均以tar形式），解压后，并根据cpom.xml的local配置，将.h拷贝到include制定位置，将.c拷贝到lib制定位置

cpom.xml示意：
    MAVEN原有节点：
        <groupId>testDemo1</groupId>                    <-    三维坐标
        <artifactId>projectA</artifactId>               <-    三维坐标
        <version>1.0-SNAPSHOT</version>                 <-    三维坐标
        <packaging>tar</packaging>                      <-    类型（java默认为jar，我们默认为tar包）

        <dependencies>                                  <-    所有的依赖项LIB
        <dependency>                                    <-    依赖项 - 1
            <groupId>testgroup</groupId>                <-    三维坐标
            <artifactId>apache-maven</artifactId>       <-    三维坐标
            <version>1.0.1</version>                    <-    三维坐标
            <type>tar</type>                            <-    类型（java默认为jar，我们默认为tar包）
        </dependency>

        <dependency>                                    <-    依赖项 - 2
            <groupId>libzdogs</groupId>                 <-    三维坐标
            <artifactId>libzdogs4cSo</artifactId>       <-    三维坐标
            <version>1.0.1</version>                    <-    三维坐标
            <type>tar</type>                            <-    类型（java默认为jar，我们默认为tar包）
        </dependency>
      </dependencies>

    个性化节点（MAVEN私有仓库）
        <repo>
            <url>http://127.0.0.1:8081/artifactory/libs-release-local/</url>
            <id>bao-pc</id>
        </repo>

    个性化节点（上传使用）
        <file>c:\1.tar</file>                           <-    上传的tar包路径

    个性化节点（下载使用） - 下载后.h与.c文件存放位置
        <local>
            <default>                                   <-   默认配置, default是所有依赖均配置与此（若没有细分配置）
                #默认的设定
                <include>haha/include</include>
                <lib>heihei/lib</lib>
            </default>

            <apache-maven>                              <-   细分配置, artifactId=apache-maven的lib依赖库的特殊配置
                #特殊的设定
                <include>teststt/include</include>
                <lib>fdfdfad/lib</lib>
            </apache-maven>
        </local>