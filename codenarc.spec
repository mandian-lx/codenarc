%{?_javapackages_macros:%_javapackages_macros}
%global oname CodeNarc
Name:          codenarc
Version:       0.24.1
Release:       2%{?dist}
Summary:       Groovy library that provides static analysis features for Groovy code
Group:         Development/Java
License:       ASL 2.0
Url:           http://codenarc.sourceforge.net/
Source0:       https://github.com/CodeNarc/CodeNarc/archive/%{version}/%{name}-%{version}.tar.gz

BuildRequires: maven-local
BuildRequires: mvn(junit:junit)
BuildRequires: mvn(log4j:log4j:1.2.17)
BuildRequires: mvn(org.apache.ant:ant)
BuildRequires: mvn(org.codehaus.gmavenplus:gmavenplus-plugin)
BuildRequires: mvn(org.codehaus.groovy:groovy)
BuildRequires: mvn(org.codehaus.groovy:groovy-ant)
BuildRequires: mvn(org.codehaus.groovy:groovy-xml)
BuildRequires: mvn(org.gmetrics:GMetrics)
BuildRequires: mvn(org.sonatype.oss:oss-parent:pom:)

BuildArch:     noarch

%description
CodeNarc is a static analysis tool for Groovy source code,
enabling monitoring and enforcement of many coding standards
and best practices. CodeNarc applies a set of Rules
(predefined and/or custom) that are applied to each Groovy
file, and generates an HTML report of the results, including
a list of rules violated for each source file, and a count
of the number of violations per package and for the whole
project.

%package javadoc
Summary:       Javadoc for %{name}

%description javadoc
This package contains javadoc for %{name}.

%prep
%setup -q -n %{oname}-%{version}

find . -name "*.jar" -delete
find . -name "*.class" -delete
rm -rf docs/*

cp -p site-pom.xml pom.xml

mkdir -p src/main/java/org/codenarc/analyzer
cp -p src/main/groovy/org/codenarc/analyzer/SuppressionAnalyzer.java \
 src/main/java/org/codenarc/analyzer/

# Set encoding
%pom_xpath_inject pom:project/pom:properties '
  <antVersion>1.9.6</antVersion>
  <gmetricsVersion>0.7</gmetricsVersion>
  <junitVersion>4.12</junitVersion>
  <log4jVersion>1.2.17</log4jVersion>
  <project.build.sourceEncoding>UTF-8</project.build.sourceEncoding>
  <project.reporting.outputEncoding>UTF-8</project.reporting.outputEncoding>'

%pom_xpath_set pom:properties/pom:targetJdk 1.6
%pom_xpath_set pom:properties/pom:groovyVersion 2.4.5

%pom_add_plugin org.apache.maven.plugins:maven-compiler-plugin:3.5.1 . "
<configuration>
    <source>\${targetJdk}</source>
    <target>\${targetJdk}</target>
</configuration>"

%pom_add_plugin org.codehaus.gmavenplus:gmavenplus-plugin:1.5 . "
 <executions>
  <execution>
   <goals>
    <goal>generateStubs</goal>
    <!--goal>testCompile</goal-->
    <goal>testGenerateStubs</goal>
   </goals>
  </execution>
 </executions>"

%pom_add_dep org.apache.ant:ant:'${antVersion}' . "<optional>true</optional>"
%pom_add_dep org.codehaus.groovy:groovy:'${groovyVersion}'
%pom_add_dep org.codehaus.groovy:groovy-ant:'${groovyVersion}'
%pom_add_dep org.codehaus.groovy:groovy-xml:'${groovyVersion}'
%pom_add_dep org.gmetrics:GMetrics:'${gmetricsVersion}'
%pom_add_dep junit:junit:'${junitVersion}'
%pom_add_dep log4j:log4j:'${log4jVersion}'

# Convert from dos to unix line ending
for file in CHANGELOG.txt LICENSE.txt NOTICE.txt README.md ; do
 sed -i.orig 's|\r||g' $file
 touch -r $file.orig $file
 rm $file.orig
done

%mvn_file org.%{name}:%{oname} %{name} %{oname}

%build

%mvn_build

%install
%mvn_install

%files -f .mfiles
%doc CHANGELOG.txt README.md
%doc LICENSE.txt NOTICE.txt

%files javadoc -f .mfiles-javadoc
%doc LICENSE.txt NOTICE.txt

%changelog
* Fri Feb 10 2017 Fedora Release Engineering <releng@fedoraproject.org> - 0.24.1-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_26_Mass_Rebuild

* Tue Aug 16 2016 gil cattaneo <puntogil@libero.it> 0.24.1-1
- update to 0.24.1

* Wed Feb 03 2016 Fedora Release Engineering <releng@fedoraproject.org> - 0.17-15
- Rebuilt for https://fedoraproject.org/wiki/Fedora_24_Mass_Rebuild

* Tue Jun 23 2015 gil cattaneo <puntogil@libero.it> 0.17-14
- fix FTBFS
- use groovy 2

* Wed Jun 17 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.17-13
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Tue Mar 10 2015 gil cattaneo <puntogil@libero.it> 0.17-12
- remove cobertura

* Fri Jan 30 2015 gil cattaneo <puntogil@libero.it> 0.17-11
- re-base for use groovy 2

* Fri Jan 30 2015 gil cattaneo <puntogil@libero.it> 0.17-10
- introduce license macro

* Thu Nov 13 2014 gil cattaneo <puntogil@libero.it> 0.17-9
- fix log4j12 classpath/version
- remove (g)maven references

* Thu Nov 13 2014 Mikolaj Izdebski <mizdebsk@redhat.com> - 0.17-8
- Remove POM patch changing artifactId from groovy-all to groovy

* Sat Jun 07 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.17-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Fri Mar 28 2014 Michael Simacek <msimacek@redhat.com> - 0.17-6
- Use Requires: java-headless rebuild (#1067528)

* Thu Nov 14 2013 gil cattaneo <puntogil@libero.it> 0.17-5
- use objectweb-asm3

* Sat Aug 03 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.17-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Wed Feb 13 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.17-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Mon Aug 06 2012 gil cattaneo <puntogil@libero.it> 0.17-2
- fixed the permissions and encoding issues on *.txt files
- change with_gmaven to 0 (only for now)
- generate javadocs with ant support

* Thu Mar 29 2012 gil cattaneo <puntogil@libero.it> 0.17-1
- initial rpm
