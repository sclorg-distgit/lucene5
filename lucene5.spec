%global pkg_name lucene5
%{?scl:%scl_package %{pkg_name}}
%{?java_common_find_provides_and_requires}

# Copyright (c) 2000-2005, JPackage Project
# All rights reserved.
#
# Redistribution and use in source and binary forms, with or without
# modification, are permitted provided that the following conditions
# are met:
#
# 1. Redistributions of source code must retain the above copyright
#    notice, this list of conditions and the following disclaimer.
# 2. Redistributions in binary form must reproduce the above copyright
#    notice, this list of conditions and the following disclaimer in the
#    documentation and/or other materials provided with the
#    distribution.
# 3. Neither the name of the JPackage Project nor the names of its
#    contributors may be used to endorse or promote products derived
#    from this software without specific prior written permission.
#
# THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS
# "AS IS" AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT
# LIMITED TO, THE IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR
# A PARTICULAR PURPOSE ARE DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT
# OWNER OR CONTRIBUTORS BE LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL,
# SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT
# LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES; LOSS OF USE,
# DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON ANY
# THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT
# (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE
# OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.
#

Summary:        High-performance, full-featured text search engine
Name:           %{?scl_prefix}%{pkg_name}
Version:        5.4.1
Release:        2.3%{?dist}
Epoch:          0
License:        ASL 2.0
URL:            http://lucene.apache.org/
Source0:        http://www.apache.org/dist/lucene/java/%{version}/lucene-%{version}-src.tgz
#svn export http://svn.apache.org/repos/asf/lucene/dev/tags/lucene_solr_5_4_1/dev-tools/
#tar caf dev-tools-5.4.1.tar.xz dev-tools/
Source1:        dev-tools-%{version}.tar.xz
Source2:        ivy-conf.xml

Patch0:         0001-disable-ivy-settings.patch
Patch1:         0001-dependency-generation.patch
Patch2:         ivy-local-fix.patch

BuildRequires:  %{?scl_prefix}ant
BuildRequires:  %{?scl_prefix}ivy-local
BuildRequires:  %{?scl_prefix}httpcomponents-client
BuildRequires:  %{?scl_prefix}jetty-continuation
BuildRequires:  %{?scl_prefix}jetty-http
BuildRequires:  %{?scl_prefix}jetty-io
BuildRequires:  %{?scl_prefix}jetty-server
BuildRequires:  %{?scl_prefix}jetty-servlet
BuildRequires:  %{?scl_prefix}jetty-util
BuildRequires:  %{?scl_prefix}nekohtml
BuildRequires:  %{?scl_prefix}xerces-j2
BuildRequires:  %{?scl_prefix}mvn(javax.servlet:servlet-api)
BuildRequires:  %{?scl_prefix}maven-local
BuildRequires:  %{?scl_prefix_maven}apache-parent

# test-framework deps
BuildRequires:  %{?scl_prefix}junit
#BuildRequires:  randomizedtesting-junit4-ant
#BuildRequires:  randomizedtesting-runner

# Workaround for bug in javapackages dependency generator (rhbz#1414716)
BuildRequires:  %{?scl_prefix}lucene-solr-grandparent

Provides:       %{name}-core = %{epoch}:%{version}-%{release}

BuildArch:      noarch

%description
Apache Lucene is a high-performance, full-featured text search
engine library written entirely in Java. It is a technology suitable
for nearly any application that requires full-text search, especially
cross-platform.

%package parent
Summary:      Parent POM for Lucene

%description parent
Parent POM for Lucene.

%package solr-grandparent
Summary:      Lucene Solr grandparent POM

%description solr-grandparent
Lucene Solr grandparent POM.

%package backward-codecs
Summary:      Lucene Backward Codecs Module

%description backward-codecs
Codecs for older versions of Lucene.

%package replicator
Summary:      Lucene Replicator Module

%description replicator
Lucene Replicator Module.

%package grouping
Summary:      Lucene Grouping Module

%description grouping
Lucene Grouping Module.

%package highlighter
Summary:      Lucene Highlighter Module

%description highlighter
Lucene Highlighter Module.

%package misc
Summary:      Miscellaneous Lucene extensions

%description misc
Miscellaneous Lucene extensions.

%package memory
Summary:      Lucene Memory Module

%description memory
High-performance single-document index to compare against Query.

%package classification
Summary:      Lucene Classification Module

%description classification
Lucene Classification Module.

%package join
Summary:      Lucene Join Module

%description join
Lucene Join Module.

%package suggest
Summary:      Lucene Suggest Module

%description suggest
Lucene Suggest Module.

%package facet
Summary:      Lucene Facets Module

%description facet
Package for Faceted Indexing and Search.

%package analysis
Summary:      Lucene Common Analyzers

%description analysis
Lucene Common Analyzers.

%package sandbox
Summary:      Lucene Sandbox Module

%description sandbox
Lucene Sandbox Module.

%package queries
Summary:      Lucene Queries Module

%description queries
Lucene Queries Module.

%package codecs
Summary:      Codecs and postings formats for Apache Lucene

%description codecs
Codecs and postings formats for Apache Lucene.

%package queryparser
Summary:      Lucene QueryParsers Module

%description queryparser
Lucene QueryParsers Module.

%package analyzers-smartcn
Summary:      Smart Chinese Analyzer

%description analyzers-smartcn
Lucene Smart Chinese Analyzer.

%package javadoc
Summary:        Javadoc for Lucene

%description javadoc
%{summary}.

%prep
%setup -q -n lucene-%{version}
%{?scl:scl enable %{scl_maven} %{scl} - <<"EOF"}
set -e -x
%patch0 -p1
%patch1 -p1
%patch2 -p1
# dependency generator expects that the directory name is just lucene
mkdir lucene
find -maxdepth 1 ! -name CHANGES.txt ! -name LICENSE.txt ! -name README.txt \
    ! -name NOTICE.txt ! -name MIGRATE.txt  ! -name ivy-settings.xml \
    ! -path lucene -exec mv \{} lucene/ \;

tar xf %{SOURCE1}
pushd dev-tools/maven
sed -i -e "s|/Export-Package>|/Export-Package><_nouses>true</_nouses>|g" pom.xml.template
popd

# remove all binary libs
find . -name "*.jar" -exec rm -f {} \;

%mvn_package ":lucene-analysis-modules-aggregator" lucene-analysis
%mvn_package ":lucene-analyzers-common" lucene-analysis
%mvn_package ":{*}-aggregator" @1

%mvn_compat_version : 5 5.4.1

# we don't need following modules
rm -Rf lucene/analysis/{icu,kuromoji,morfologik,phonetic,stempel,uima}
%{?scl:EOF}

%build
%{?scl:scl enable %{scl_maven} %{scl} - <<"EOF"}
set -e -x
pushd lucene
# generate dependencies
ant filter-pom-templates -Divy.settings.file=%{SOURCE2} -Dbuild.sysclasspath=first -Divy.mode=local -Dversion=%{version}

mkdir -p analysis/{icu,kuromoji,morfologik,phonetic,stempel,uima}

# fix source dir + move to expected place
for pom in `find build/poms/lucene -name pom.xml`; do
    sed 's/\${module-path}/${basedir}/g' "$pom" > "${pom##build/poms/lucene/}"
done
%pom_remove_plugin :forbiddenapis
for module in test-framework; do
    %pom_remove_plugin :forbiddenapis ${module}
done

%pom_disable_module src/test core
%pom_disable_module src/test codecs

# we don't need these
%pom_disable_module test-framework
%pom_disable_module spatial
%pom_disable_module spatial3d
%pom_disable_module demo
%pom_disable_module benchmark
%pom_disable_module expressions
%pom_disable_module icu analysis
%pom_disable_module kuromoji analysis
%pom_disable_module morfologik analysis
%pom_disable_module phonetic analysis
%pom_disable_module stempel analysis
%pom_disable_module uima analysis

popd

mv lucene/build/poms/pom.xml .

%pom_disable_module solr
%pom_remove_plugin :gmaven-plugin
%pom_remove_plugin :forbiddenapis
%pom_remove_plugin :maven-enforcer-plugin

# For some reason TestHtmlParser.testTurkish fails when building inside SCLs
%mvn_build -s -f
%{?scl:EOF}

%install
%{?scl:scl enable %{scl_maven} %{scl} - <<"EOF"}
set -e -x
# suggest provides spellchecker
%mvn_alias :lucene-suggest :lucene-spellchecker

# compatibility with existing packages
%mvn_alias :lucene-analyzers-common :lucene-analyzers

%mvn_install

# Use the same directory of the main package for subpackage licence and docs
%global _docdir_fmt %{pkg_name}
%{?scl:EOF}

%files -f .mfiles-lucene-core
%{!?_licensedir:%global license %%doc}
%dir %{_javadir}/%{pkg_name}
%dir %{_jnidir}/%{pkg_name}
%dir %{_mavenpomdir}/%{pkg_name}
%doc LICENSE.txt NOTICE.txt CHANGES.txt README.txt MIGRATE.txt

%files parent -f .mfiles-lucene-parent
%dir %{_mavenpomdir}/%{pkg_name}
%doc LICENSE.txt NOTICE.txt
%files solr-grandparent -f .mfiles-lucene-solr-grandparent
%dir %{_mavenpomdir}/%{pkg_name}
%doc LICENSE.txt NOTICE.txt
%files backward-codecs -f .mfiles-lucene-backward-codecs
%files replicator -f .mfiles-lucene-replicator
%files grouping -f .mfiles-lucene-grouping
%files highlighter -f .mfiles-lucene-highlighter
%files misc -f .mfiles-lucene-misc
%dir %{_jnidir}/%{pkg_name}
%files memory -f .mfiles-lucene-memory
%files classification -f .mfiles-lucene-classification
%files join -f .mfiles-lucene-join
%files suggest -f .mfiles-lucene-suggest
%files facet -f .mfiles-lucene-facet
%files analysis -f .mfiles-lucene-analysis
%files sandbox -f .mfiles-lucene-sandbox
%files queries -f .mfiles-lucene-queries
%files codecs -f .mfiles-lucene-codecs
%files queryparser -f .mfiles-lucene-queryparser
%files analyzers-smartcn -f .mfiles-lucene-analyzers-smartcn
%files javadoc -f .mfiles-javadoc
%doc LICENSE.txt NOTICE.txt

%changelog
* Thu Jan 19 2017 Mikolaj Izdebski <mizdebsk@redhat.com> - 0:5.4.1-2.3
- Add workaround for bug in javapackages dependency generator
- Resolves: rhbz#1414716

* Thu Mar 31 2016 Michal Srb <msrb@redhat.com> - 0:5.4.1-2.2
- Fix directory ownership (Resolves: rhbz#1319277)

* Tue Jan 26 2016 Michal Srb <msrb@redhat.com> - 0:5.4.1-2.1
- Prepare for SCL build

* Mon Jan 25 2016 Alexander Kurtakov <akurtako@redhat.com> 0:5.4.1-2
- Organize Sources numbering.
- Drop old jpackage header - package has nothing in common anymore.
- Drop 3+ years old provides/obsoletes.
- Move old changelog to separate file to ease working with the spec file.

* Mon Jan 25 2016 Alexander Kurtakov <akurtako@redhat.com> 0:5.4.1-1
- Update to upstream 5.4.1 release.

* Thu Jan 21 2016 Alexander Kurtakov <akurtako@redhat.com> 0:5.4.0-1
- Update to upstream 5.4.0 release.

* Tue Oct 6 2015 Alexander Kurtakov <akurtako@redhat.com> 0:5.3.1-1
- Update to upstream 5.3.1 release.

* Thu Aug 27 2015 Alexander Kurtakov <akurtako@redhat.com> 0:5.3.0-1
- Update to upstream 5.3.0 release.

* Wed Aug 26 2015 Mat Booth <mat.booth@redhat.com> - 0:5.2.1-4
- Remove forbidden SCL macros

* Wed Jun 24 2015 Alexander Kurtakov <akurtako@redhat.com> 0:5.2.1-3
- Disable generation of uses clauses in OSGi manifests.

* Wed Jun 24 2015 Alexander Kurtakov <akurtako@redhat.com> 0:5.2.1-2
- Drop old workarounds.

* Tue Jun 23 2015 Alexander Kurtakov <akurtako@redhat.com> 0:5.2.1-1
- Update to upstream 5.2.1.
