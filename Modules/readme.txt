����MAVEN����Ŀpom.xml�������һЩ���Ի��ڵ㣨�ݶ�Ϊcpom.xml����
1�������ϴ�LIBʱ������cpom.xml��groupid, artifactid, version��ά���꣬������˽�вֿ�����url, repoid������MAVEN�ϴ�deploy��������systemִ��
2����������LIBʱ������cpom.xml�е�dependencies�����õ�������LIBS���ֱ�����MAVEN˽�вֿ��http��������һ��ȡtar�����ϴ�ʱ��packaging����tar��ʽ������ѹ�󣬲�����cpom.xml��local���ã���.h������include�ƶ�λ�ã���.c������lib�ƶ�λ��

cpom.xmlʾ�⣺
    MAVENԭ�нڵ㣺
        <groupId>testDemo1</groupId>                    <-    ��ά����
        <artifactId>projectA</artifactId>               <-    ��ά����
        <version>1.0-SNAPSHOT</version>                 <-    ��ά����
        <packaging>tar</packaging>                      <-    ���ͣ�javaĬ��Ϊjar������Ĭ��Ϊtar����

        <dependencies>                                  <-    ���е�������LIB
        <dependency>                                    <-    ������ - 1
            <groupId>testgroup</groupId>                <-    ��ά����
            <artifactId>apache-maven</artifactId>       <-    ��ά����
            <version>1.0.1</version>                    <-    ��ά����
            <type>tar</type>                            <-    ���ͣ�javaĬ��Ϊjar������Ĭ��Ϊtar����
        </dependency>

        <dependency>                                    <-    ������ - 2
            <groupId>libzdogs</groupId>                 <-    ��ά����
            <artifactId>libzdogs4cSo</artifactId>       <-    ��ά����
            <version>1.0.1</version>                    <-    ��ά����
            <type>tar</type>                            <-    ���ͣ�javaĬ��Ϊjar������Ĭ��Ϊtar����
        </dependency>
      </dependencies>

    ���Ի��ڵ㣨MAVEN˽�вֿ⣩
        <repo>
            <url>http://127.0.0.1:8081/artifactory/libs-release-local/</url>
            <id>bao-pc</id>
        </repo>

    ���Ի��ڵ㣨�ϴ�ʹ�ã�
        <file>c:\1.tar</file>                           <-    �ϴ���tar��·��

    ���Ի��ڵ㣨����ʹ�ã� - ���غ�.h��.c�ļ����λ��
        <local>
            <default>                                   <-   Ĭ������, default������������������ˣ���û��ϸ�����ã�
                #Ĭ�ϵ��趨
                <include>haha/include</include>
                <lib>heihei/lib</lib>
            </default>

            <apache-maven>                              <-   ϸ������, artifactId=apache-maven��lib���������������
                #������趨
                <include>teststt/include</include>
                <lib>fdfdfad/lib</lib>
            </apache-maven>
        </local>