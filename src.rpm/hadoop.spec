%define hadoop_version 2.0.0+545
%define hadoop_patched_version 2.0.0-cdh4.1.1
%define hadoop_base_version 2.0.0
%define hadoop_release 1.cdh4.1.1.p0.22%{?dist}
# Licensed to the Apache Software Foundation (ASF) under one or more
# contributor license agreements.  See the NOTICE file distributed with
# this work for additional information regarding copyright ownership.
# The ASF licenses this file to You under the Apache License, Version 2.0
# (the "License"); you may not use this file except in compliance with
# the License.  You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#
# Hadoop RPM spec file
#

# FIXME: we need to disable a more strict checks on native files for now,
# since Hadoop build system makes it difficult to pass the kind of flags
# that would make newer RPM debuginfo generation scripts happy.
%undefine _missing_build_ids_terminate_build

%define hadoop_name hadoop
%define etc_hadoop /etc/%{name}
%define etc_yarn /etc/yarn
%define etc_httpfs /etc/%{name}-httpfs
%define config_hadoop %{etc_hadoop}/conf
%define config_yarn %{etc_yarn}/conf
%define config_httpfs %{etc_httpfs}/conf
%define lib_hadoop_dirname /usr/lib
%define lib_hadoop %{lib_hadoop_dirname}/%{name}
%define lib_httpfs %{lib_hadoop_dirname}/%{name}-httpfs
%define lib_hdfs %{lib_hadoop_dirname}/%{name}-hdfs
%define lib_yarn %{lib_hadoop_dirname}/%{name}-yarn
%define lib_mapreduce %{lib_hadoop_dirname}/%{name}-mapreduce
%define log_hadoop_dirname /var/log
%define log_hadoop %{log_hadoop_dirname}/%{name}
%define log_yarn %{log_hadoop_dirname}/%{name}-yarn
%define log_hdfs %{log_hadoop_dirname}/%{name}-hdfs
%define log_httpfs %{log_hadoop_dirname}/%{name}-httpfs
%define log_mapreduce %{log_hadoop_dirname}/%{name}-mapreduce
%define run_hadoop_dirname /var/run
%define run_hadoop %{run_hadoop_dirname}/hadoop
%define run_yarn %{run_hadoop_dirname}/%{name}-yarn
%define run_hdfs %{run_hadoop_dirname}/%{name}-hdfs
%define run_httpfs %{run_hadoop_dirname}/%{name}-httpfs
%define run_mapreduce %{run_hadoop_dirname}/%{name}-mapreduce
%define state_hadoop_dirname /var/lib
%define state_hadoop %{state_hadoop_dirname}/hadoop
%define state_yarn %{state_hadoop_dirname}/%{name}-yarn
%define state_hdfs %{state_hadoop_dirname}/%{name}-hdfs
%define state_mapreduce %{state_hadoop_dirname}/%{name}-mapreduce
%define bin_hadoop %{_bindir}
%define man_hadoop %{_mandir}
%define doc_hadoop %{_docdir}/%{name}-%{hadoop_version}
%define httpfs_services httpfs
%define mapreduce_services mapreduce-historyserver
%define hdfs_services hdfs-namenode hdfs-secondarynamenode hdfs-datanode hdfs-zkfc hdfs-journalnode
%define yarn_services yarn-resourcemanager yarn-nodemanager yarn-proxyserver
%define hadoop_services %{hdfs_services} %{mapreduce_services} %{yarn_services} %{httpfs_services}
# Hadoop outputs built binaries into %{hadoop_build}
%define hadoop_build_path build
%define static_images_dir src/webapps/static/images

%ifarch i386 i686
%global hadoop_arch Linux-i386-32
%global requires_lib_tag %{nil}
%endif
%ifarch amd64 x86_64
%global hadoop_arch Linux-amd64-64
%global requires_lib_tag ()(64bit)
%endif

# CentOS 5 does not have any dist macro
# So I will suppose anything that is not Mageia or a SUSE will be a RHEL/CentOS/Fedora
%if %{!?suse_version:1}0 && %{!?mgaversion:1}0

# FIXME: brp-repack-jars uses unzip to expand jar files
# Unfortunately aspectjtools-1.6.5.jar pulled by ivy contains some files and directories without any read permission
# and make whole process to fail.
# So for now brp-repack-jars is being deactivated until this is fixed.
# See BIGTOP-294
%define __os_install_post \
    /usr/lib/rpm/redhat/brp-compress ; \
    /usr/lib/rpm/redhat/brp-strip-static-archive %{__strip} ; \
    /usr/lib/rpm/redhat/brp-strip-comment-note %{__strip} %{__objdump} ; \
    /usr/lib/rpm/brp-python-bytecompile ; \
    %{nil}

%define netcat_package nc
%define libexecdir %{_libexecdir}
%define doc_hadoop %{_docdir}/%{name}-%{hadoop_version}
%define alternatives_cmd alternatives
%global initd_dir %{_sysconfdir}/rc.d/init.d
%endif


%if  %{?suse_version:1}0

# Only tested on openSUSE 11.4. le'ts update it for previous release when confirmed
%if 0%{suse_version} > 1130
%define suse_check \# Define an empty suse_check for compatibility with older sles
%endif

# Deactivating symlinks checks
%define __os_install_post \
    %{suse_check} ; \
    /usr/lib/rpm/brp-compress ; \
    %{nil}

%define netcat_package netcat-openbsd
%define libexecdir /usr/lib
%define doc_hadoop %{_docdir}/%{name}
%define alternatives_cmd update-alternatives
%global initd_dir %{_sysconfdir}/rc.d
%endif

%if  0%{?mgaversion}
%define netcat_package netcat-openbsd
%define libexecdir /usr/libexec/
%define doc_hadoop %{_docdir}/%{name}-%{hadoop_version}
%define alternatives_cmd update-alternatives
%global initd_dir %{_sysconfdir}/rc.d/init.d
%endif


# Even though we split the RPM into arch and noarch, it still will build and install
# the entirety of hadoop. Defining this tells RPM not to fail the build
# when it notices that we didn't package most of the installed files.
%define _unpackaged_files_terminate_build 0

# RPM searches perl files for dependancies and this breaks for non packaged perl lib
# like thrift so disable this
%define _use_internal_dependency_generator 0

Name: %{hadoop_name}
Version: %{hadoop_version}
Release: %{hadoop_release}
Summary: Hadoop is a software platform for processing vast amounts of data
License: Apache License v2.0
URL: http://hadoop.apache.org/core/
Group: Development/Libraries
Source0: %{name}-%{hadoop_patched_version}.tar.gz
Source1: do-component-build
Source2: install_%{name}.sh
Source3: hadoop.default
Source4: hadoop-fuse.default
Source5: httpfs.default
Source6: hadoop.1
Source7: hadoop-fuse-dfs.1
Source8: hdfs.conf
Source9: yarn.conf
Source10: mapreduce.conf
Source11: init.d.tmpl
Source12: hadoop-hdfs-namenode.svc
Source13: hadoop-hdfs-datanode.svc
Source14: hadoop-hdfs-secondarynamenode.svc
Source15: hadoop-mapreduce-historyserver.svc
Source16: hadoop-yarn-resourcemanager.svc
Source17: hadoop-yarn-nodemanager.svc
Source18: hadoop-httpfs.svc
Source19: mapreduce.default
Source20: hdfs.default
Source21: yarn.default
Source22: hadoop-layout.sh
Source23: hadoop-hdfs-zkfc.svc
Source24: hadoop-hdfs-journalnode.svc
Source25: %{name}-bigtop-packaging.tar.gz
Source26: hadoop-fuse.te

Patch0: mvn304.patch
Patch1: javafuse.patch
Patch2: libhdfs-soversion.patch
Patch3: libhdfs-soversion-install.patch
Patch4: fix_chown.patch
Patch5: pom.xml.patch
Patch6: 1184-extendable-client.patch
Patch7: HDFS-5341.004.patch
Patch8: 2006-HDFS-4997.patch


Buildroot: %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id} -u -n)
BuildRequires: python >= 2.4
BuildRequires: git
BuildRequires: fuse-devel
BuildRequires: fuse
BuildRequires: automake
BuildRequires: autoconf
%if 0%{?rhel} >= 7
BuildRequires: maven >= 3.0.0
%else
BuildRequires: maven3
%endif
BuildRequires: protobuf-compiler
BuildRequires: cmake
BuildRequires: java7-devel
BuildRequires: jpackage-utils
BuildRequires: /usr/lib/java-1.7.0

Requires: coreutils, /usr/sbin/useradd, /usr/sbin/usermod, /sbin/chkconfig, /sbin/service, bigtop-utils, zookeeper >= 3.4.0
Requires: psmisc, %{netcat_package}
Requires: java7
Requires: jpackage-utils
Requires: /usr/lib/java-1.7.0
Conflicts: hadoop-0.20
Provides: hadoop
Obsoletes: hadoop-0.20 <= 0.20.2+737

%if  %{?suse_version:1}0
BuildRequires: libfuse2, libopenssl-devel, gcc-c++, ant, ant-nodeps, ant-trax
# Required for init scripts
Requires: sh-utils, insserv
%endif

# CentOS 5 does not have any dist macro
# So I will suppose anything that is not Mageia or a SUSE will be a RHEL/CentOS/Fedora
%if %{!?suse_version:1}0 && %{!?mgaversion:1}0
BuildRequires: fuse-libs, libtool, redhat-rpm-config, lzo-devel, openssl-devel
# Required for init scripts
Requires: sh-utils, redhat-lsb
%endif

%if  0%{?mgaversion}
BuildRequires: libfuse-devel, libfuse2 , libopenssl-devel, gcc-c++, ant, libtool, automake, autoconf, liblzo-devel, zlib-devel
Requires: chkconfig, xinetd-simple-services, zlib, initscripts
%endif


%description
Hadoop is a software platform that lets one easily write and
run applications that process vast amounts of data.

Here's what makes Hadoop especially useful:
* Scalable: Hadoop can reliably store and process petabytes.
* Economical: It distributes the data and processing across clusters
              of commonly available computers. These clusters can number
              into the thousands of nodes.
* Efficient: By distributing the data, Hadoop can process it in parallel
             on the nodes where the data is located. This makes it
             extremely rapid.
* Reliable: Hadoop automatically maintains multiple copies of data and
            automatically redeploys computing tasks based on failures.

Hadoop implements MapReduce, using the Hadoop Distributed File System (HDFS).
MapReduce divides applications into many small blocks of work. HDFS creates
multiple replicas of data blocks for reliability, placing them on compute
nodes around the cluster. MapReduce can then process the data where it is
located.

%package hdfs
Summary: The Hadoop Distributed File System
Group: System/Daemons
Requires: %{name} = %{version}-%{release}, bigtop-jsvc
# Workaround for 4.0 to 4.X upgrade (CDH-7856) (upgrades from 4.1 onwards are fine)
Requires: libhadoop.so.1.0.0%{requires_lib_tag}

%description hdfs
Hadoop Distributed File System (HDFS) is the primary storage system used by
Hadoop applications. HDFS creates multiple replicas of data blocks and
distributes them on cluster hosts to enable reliable and extremely rapid
computations.

%package yarn
Summary: The Hadoop NextGen MapReduce (YARN)
Group: System/Daemons
Requires: %{name} = %{version}-%{release}
# Workaround for 4.0 to 4.X upgrade (CDH-7856) (upgrades from 4.1 onwards are fine)
Requires: libhadoop.so.1.0.0%{requires_lib_tag}

%description yarn
YARN (Hadoop NextGen MapReduce) is a general purpose data-computation framework.
YARN splits up the functionalities of JobTracker, resource management, 
job scheduling, and job monitoring into separate daemons called 
ResourceManager and NodeManager.

ResourceManager is the ultimate authority that arbitrates resources 
among all applications in the system. NodeManager is a per-host slave
that manages allocation of computational resources on a single host. 
Both daemons work in support of ApplicationMaster (AM).

ApplicationMaster is a framework-specific library that negotiates resources 
from ResourceManager and works with NodeManager(s) to execute and monitor 
the tasks.

%package mapreduce
Summary: The Hadoop MapReduce (MRv2)
Group: System/Daemons
Requires: %{name}-yarn = %{version}-%{release}

%description mapreduce
Hadoop MapReduce is a programming model and software framework for
writing applications that rapidly process vast amounts of data
in parallel on large clusters of hosts.


%package hdfs-namenode
Summary: The Hadoop namenode manages the block locations of HDFS files
Group: System/Daemons
Requires: %{name}-hdfs = %{version}-%{release}
Obsoletes: hadoop-0.20-namenode <= 0.20.2+737

%description hdfs-namenode
The Hadoop Distributed Filesystem (HDFS) requires one unique server, the
namenode, which manages the block locations of files on the filesystem.


%package hdfs-secondarynamenode
Summary: Hadoop Secondary namenode
Group: System/Daemons
Requires: %{name}-hdfs = %{version}-%{release}
Obsoletes: hadoop-0.20-secondarynamenode <= 0.20.2+737

%description hdfs-secondarynamenode
The Secondary Name Node periodically compacts the Name Node EditLog
into a checkpoint.  This compaction ensures that Name Node restarts
do not incur unnecessary downtime.

%package hdfs-zkfc
Summary: Hadoop HDFS failover controller
Group: System/Daemons
Requires: %{name}-hdfs = %{version}-%{release}
Requires(pre): %{name} = %{version}-%{release}

%description hdfs-zkfc
The Hadoop HDFS failover controller is a ZooKeeper client which also
monitors and manages the state of the NameNode. Each of the machines
which runs a NameNode also runs a ZKFC, and that ZKFC is responsible
for: Health monitoring, ZooKeeper session management, ZooKeeper-based
election.

%package hdfs-journalnode
Summary: Hadoop HDFS JournalNode
Group: System/Daemons
Requires: %{name}-hdfs = %{version}-%{release}
Requires(pre): %{name} = %{version}-%{release}

%description hdfs-journalnode
The HDFS JournalNode is responsible for persisting NameNode edit logs. 
In a typical deployment the JournalNode daemon runs on at least three 
separate machines in the cluster.

%package hdfs-datanode
Summary: Hadoop Data Node
Group: System/Daemons
Requires: %{name}-hdfs = %{version}-%{release}
Obsoletes: hadoop-0.20-datanode <= 0.20.2+737

%description hdfs-datanode
The Data Nodes in the Hadoop Cluster are responsible for serving up
blocks of data over the network to Hadoop Distributed Filesystem
(HDFS) clients.

%package httpfs
Summary: HTTPFS for Hadoop
Group: System/Daemons
Requires: %{name}-hdfs = %{version}-%{release}, bigtop-tomcat
Requires(pre): %{name} = %{version}-%{release}

%description httpfs
The server providing HTTP REST API support for the complete FileSystem/FileContext
interface in HDFS.

%package yarn-resourcemanager
Summary: Yarn Resource Manager
Group: System/Daemons
Requires: %{name}-yarn = %{version}-%{release}

%description yarn-resourcemanager
The resource manager manages the global assignment of compute resources to applications

%package yarn-nodemanager
Summary: Yarn Node Manager
Group: System/Daemons
Requires: %{name}-yarn = %{version}-%{release}

%description yarn-nodemanager
The NodeManager is the per-machine framework agent who is responsible for
containers, monitoring their resource usage (cpu, memory, disk, network) and
reporting the same to the ResourceManager/Scheduler.

#%package yarn-proxyserver
#Summary: Yarn Web Proxy
#Group: System/Daemons
#Requires: %{name}-yarn = %{version}-%{release}
#Requires(pre): %{name} = %{version}-%{release}

#%description yarn-proxyserver
#The web proxy server sits in front of the YARN application master web UI.

#%package mapreduce-historyserver
#Summary: MapReduce History Server
#Group: System/Daemons
#Requires: %{name}-mapreduce = %{version}-%{release}

#%description mapreduce-historyserver
#The History server keeps records of the different activities being performed on a Apache Hadoop cluster

%package client
Summary: Hadoop client side dependencies
Group: System/Daemons
Requires: %{name} = %{version}-%{release}
Requires: %{name}-hdfs = %{version}-%{release}
#disabling mapreduce in the client, we don't need it
#Requires: %{name}-yarn = %{version}-%{release}
#Requires: %{name}-mapreduce = %{version}-%{release}
#I have no idea why it requires this, disabling for now
#Requires: %{name}-0.20-mapreduce >= 0.20.2+1213
#Requires(pre): %{name}-0.20-mapreduce >= 0.20.2+1213

%description client
Installation of this package will provide you with all the dependencies for Hadoop clients.

%package conf-pseudo
Summary: Hadoop installation in pseudo-distributed mode
Group: System/Daemons
Requires: %{name} = %{version}-%{release}
Requires: %{name}-hdfs-namenode = %{version}-%{release}
Requires: %{name}-hdfs-datanode = %{version}-%{release}
Requires: %{name}-hdfs-secondarynamenode = %{version}-%{release}
Requires: %{name}-yarn-resourcemanager = %{version}-%{release}
Requires: %{name}-yarn-nodemanager = %{version}-%{release}
Requires: %{name}-mapreduce-historyserver = %{version}-%{release}

%description conf-pseudo
Installation of this RPM will setup your machine to run in pseudo-distributed mode
where each Hadoop daemon runs in a separate Java process.

%package doc
Summary: Hadoop Documentation
Group: Documentation
Obsoletes: %{name}-docs
%description doc
Documentation for Hadoop

%package libhdfs
Summary: Hadoop Filesystem Library
Group: Development/Libraries
Requires: %{name}-hdfs = %{version}-%{release}
Obsoletes: hadoop-0.20-libhdfs <= 0.20.2+737
# TODO: reconcile libjvm
AutoReq: no

%description libhdfs
Hadoop Filesystem Library


%package hdfs-fuse
Summary: Mountable HDFS
Group: Development/Libraries
Requires: %{name} = %{version}-%{release}
Requires: %{name}-libhdfs = %{version}-%{release}
Requires: %{name}-client = %{version}-%{release}
Requires: fuse
Requires: java7-devel
Obsoletes: hadoop-0.20-osg <= 0.20.2+737
Obsoletes: hadoop-0.20-fuse <= 0.20.2+737
AutoReq: no

%if %{?suse_version:1}0
Requires: libfuse2
%else
Requires: fuse-libs
%endif


%description hdfs-fuse
These projects (enumerated below) allow HDFS to be mounted (on most flavors of Unix) as a standard file system using


%define selinux_variants mls strict targeted
%global selinux_policyver %(%{__sed} -e 's,.*selinux-policy-\\([^/]*\\)/.*,\\1,' /usr/share/selinux/devel/policyhelp || echo 0.0.0)

%package hdfs-fuse-selinux
Summary: SELinux policy files for fuse mount
Group:          System Environment/Daemons
BuildRequires:  checkpolicy selinux-policy-devel hardlink selinux-policy-targeted
Requires: %{name} = %{version}-%{release}
Requires:       selinux-policy >= %{selinux_policyver}
Requires(post):         /usr/sbin/semodule /usr/sbin/semanage /sbin/fixfiles
Requires(preun):        /sbin/service /usr/sbin/semodule /usr/sbin/semanage /sbin/fixfiles
Requires(postun):       /usr/sbin/semodule
Obsoletes: hadoop-0.20-fuse-selinux <= 0.20.2+737

%description hdfs-fuse-selinux
selinux policy files for the Hadoop fuse hdfs mounts


%prep
%setup -n %{name}-%{hadoop_patched_version}
tar -C `dirname %{SOURCE25}` -xzf %{SOURCE25}
pushd `dirname %{SOURCE25}`
%if 0%{?rhel} <= 6
%patch0 -p1
%endif
%patch1 -p1
%patch3 -p1
popd
%patch2 -p0
%patch4 -p0
%patch5 -p0
%patch6 -p1
%patch7 -p1
%patch8 -p0

%build
# This assumes that you installed Java JDK 6 and set JAVA_HOME
# This assumes that you installed Java JDK 5 and set JAVA5_HOME
# This assumes that you installed Forrest and set FORREST_HOME

# Build the selinux policy file
mkdir SELinux
cp %{SOURCE26} SELinux/%{name}.te
pushd SELinux
for variant in %{selinux_variants}
do
    make NAME=${variant} -f %{_datadir}/selinux/devel/Makefile
    mv %{name}.pp %{name}.pp.${variant}
    make NAME=${variant} -f %{_datadir}/selinux/devel/Makefile clean
done
popd


export JAVA_HOME=%{java_home}
env FULL_VERSION=%{hadoop_patched_version} HADOOP_VERSION=%{hadoop_version} HADOOP_ARCH=%{hadoop_arch} bash %{SOURCE1}


%clean
%__rm -rf $RPM_BUILD_ROOT

#########################
#### INSTALL SECTION ####
#########################
%install
%__rm -rf $RPM_BUILD_ROOT

%__install -d -m 0755 $RPM_BUILD_ROOT/%{lib_hadoop}

bash %{SOURCE2} \
  --distro-dir=$RPM_SOURCE_DIR \
  --source-dir=$PWD/src \
  --build-dir=$PWD/src/build/%{name}-%{hadoop_patched_version} \
  --hadoop-version=%{hadoop_patched_version} \
  --httpfs-dir=$RPM_BUILD_ROOT%{lib_httpfs} \
  --system-include-dir=$RPM_BUILD_ROOT%{_includedir} \
  --system-lib-dir=$RPM_BUILD_ROOT%{_libdir} \
  --system-libexec-dir=$RPM_BUILD_ROOT%{lib_hadoop}/libexec \
  --hadoop-etc-dir=$RPM_BUILD_ROOT%{etc_hadoop} \
  --httpfs-etc-dir=$RPM_BUILD_ROOT%{etc_httpfs} \
  --prefix=$RPM_BUILD_ROOT \
  --doc-dir=$RPM_BUILD_ROOT%{doc_hadoop} \
  --example-dir=$RPM_BUILD_ROOT%{doc_hadoop}/examples \
  --native-build-string=%{hadoop_arch} \
  --installed-lib-dir=%{lib_hadoop} \
  --man-dir=$RPM_BUILD_ROOT%{man_hadoop} \

# Forcing Zookeeper dependency to be on the packaged jar
%__ln_s -f /usr/lib/zookeeper/zookeeper.jar $RPM_BUILD_ROOT/%{lib_hadoop}/lib/zookeeper*.jar
# Workaround for BIGTOP-583
%__rm -f $RPM_BUILD_ROOT/%{lib_hadoop}-*/lib/slf4j-log4j12-*.jar
%__ln_s -f /usr/lib/zookeeper/lib/`basename $RPM_BUILD_ROOT/%{lib_hadoop}/lib/slf4j-log4j12-*.jar` \
         $RPM_BUILD_ROOT/%{lib_hadoop}/lib/slf4j-log4j12-*.jar

# Init.d scripts
%__install -d -m 0755 $RPM_BUILD_ROOT/%{initd_dir}/

# Install top level /etc/default files
%__install -d -m 0755 $RPM_BUILD_ROOT/etc/default
%__cp $RPM_SOURCE_DIR/hadoop.default $RPM_BUILD_ROOT/etc/default/hadoop
# FIXME: BIGTOP-463
echo 'export JSVC_HOME=%{libexecdir}/bigtop-utils' >> $RPM_BUILD_ROOT/etc/default/hadoop
%__cp $RPM_SOURCE_DIR/%{name}-fuse.default $RPM_BUILD_ROOT/etc/default/%{name}-fuse

# Generate the init.d scripts
for service in %{hadoop_services}
do
       init_file=$RPM_BUILD_ROOT/%{initd_dir}/%{name}-${service}
       # On RedHat, SuSE and Mageia run-level 2 is networkless, hence excluding it
       env CHKCONFIG="- 85 15"       \
           INIT_DEFAULT_START=""  \
           INIT_DEFAULT_STOP="0 1 2 6" \
         bash $RPM_SOURCE_DIR/init.d.tmpl $RPM_SOURCE_DIR/%{name}-${service}.svc > $init_file
       chmod 755 $init_file
       cp $RPM_SOURCE_DIR/${service/-*/}.default $RPM_BUILD_ROOT/etc/default/%{name}-${service}
       chmod 644 $RPM_BUILD_ROOT/etc/default/%{name}-${service}
done

# Install security limits
%__install -d -m 0755 $RPM_BUILD_ROOT/etc/security/limits.d
%__install -m 0644 %{SOURCE8} $RPM_BUILD_ROOT/etc/security/limits.d/hdfs.conf
%__install -m 0644 %{SOURCE9} $RPM_BUILD_ROOT/etc/security/limits.d/yarn.conf
%__install -m 0644 %{SOURCE10} $RPM_BUILD_ROOT/etc/security/limits.d/mapreduce.conf

# Install fuse default file
%__install -d -m 0755 $RPM_BUILD_ROOT/etc/default
%__cp %{SOURCE4} $RPM_BUILD_ROOT/etc/default/hadoop-fuse

%ifarch noarch
%else

# Install selinux policies
pushd SELinux
for variant in %{selinux_variants}
do
    install -d $RPM_BUILD_ROOT%{_datadir}/selinux/${variant}
    install -p -m 644 %{name}.pp.${variant} \
           $RPM_BUILD_ROOT%{_datadir}/selinux/${variant}/%{name}.pp
done
popd
# Hardlink identical policy module packages together
/usr/sbin/hardlink -cv $RPM_BUILD_ROOT%{_datadir}/selinux
%endif

# /var/lib/*/cache
%__install -d -m 1777 $RPM_BUILD_ROOT/%{state_yarn}/cache
%__install -d -m 1777 $RPM_BUILD_ROOT/%{state_hdfs}/cache
%__install -d -m 1777 $RPM_BUILD_ROOT/%{state_mapreduce}/cache
# /var/log/*
%__install -d -m 0775 $RPM_BUILD_ROOT/%{log_yarn}
%__install -d -m 0775 $RPM_BUILD_ROOT/%{log_hdfs}
%__install -d -m 0775 $RPM_BUILD_ROOT/%{log_mapreduce}
%__install -d -m 0775 $RPM_BUILD_ROOT/%{log_httpfs}
# /var/run/*
%__install -d -m 0775 $RPM_BUILD_ROOT/%{run_yarn}
%__install -d -m 0775 $RPM_BUILD_ROOT/%{run_hdfs}
%__install -d -m 0775 $RPM_BUILD_ROOT/%{run_mapreduce}
%__install -d -m 0775 $RPM_BUILD_ROOT/%{run_httpfs}

%pre
getent group hadoop >/dev/null || groupadd -r hadoop
 alternatives --remove hadoop-default /usr/bin/hadoop-0.20 || true
 alternatives --remove hadoop-0.20-conf /etc/hadoop-0.20/conf.empty || true
 alternatives --remove hadoop-0.20-conf /etc/hadoop-0.20/conf.osg || true

%pre hdfs
getent group hdfs >/dev/null   || groupadd -r hdfs
getent passwd hdfs >/dev/null || /usr/sbin/useradd --comment "Hadoop HDFS" --shell /bin/bash -M -r -g hdfs --home %{state_hdfs} hdfs
 alternatives --remove hadoop-default /usr/bin/hadoop-0.20 || true
 alternatives --remove hadoop-0.20-conf /etc/hadoop-0.20/conf.empty || true
 alternatives --remove hadoop-0.20-conf /etc/hadoop-0.20/conf.osg || true

%pre client
 alternatives --remove hadoop-default /usr/bin/hadoop-0.20 || true
 alternatives --remove hadoop-0.20-conf /etc/hadoop-0.20/conf.empty || true
 alternatives --remove hadoop-0.20-conf /etc/hadoop-0.20/conf.osg || true

%pre libhdfs
 alternatives --remove hadoop-default /usr/bin/hadoop-0.20 || true
 alternatives --remove hadoop-0.20-conf /etc/hadoop-0.20/conf.empty || true
 alternatives --remove hadoop-0.20-conf /etc/hadoop-0.20/conf.osg || true

%pre httpfs
getent group httpfs >/dev/null   || groupadd -r httpfs
getent passwd httpfs >/dev/null || /usr/sbin/useradd --comment "Hadoop HTTPFS" --shell /bin/bash -M -r -g httpfs --home %{run_httpfs} httpfs

#%pre yarn
#getent group yarn >/dev/null   || groupadd -r yarn
#getent passwd yarn >/dev/null || /usr/sbin/useradd --comment "Hadoop Yarn" --shell /bin/bash -M -r -g yarn -G hadoop --home %{state_yarn} yarn

#%pre mapreduce
#getent group mapred >/dev/null   || groupadd -r mapred
#getent passwd mapred >/dev/null || /usr/sbin/useradd --comment "Hadoop MapReduce" --shell /bin/bash -M -r -g mapred -G hadoop --home %{state_mapreduce} mapred

%post
%{alternatives_cmd} --install %{config_hadoop} %{name}-conf %{etc_hadoop}/conf.empty 10

# Add "httpfs" user to the "hadoop" group. This is in %%post because it needs to
# be done after the "hadoop" group is created, i.e. after "hadoop"'s %%pre.
%post httpfs
getent group hadoop >/dev/null && /usr/sbin/usermod -G hadoop httpfs || true
%{alternatives_cmd} --install %{config_httpfs} %{name}-httpfs-conf %{etc_httpfs}/conf.empty 10
chkconfig --add %{name}-httpfs

# Add "hdfs" user to the "hadoop" group. This is in %%post because it needs to
# be done after the "hadoop" group is created, i.e. after "hadoop"'s %%pre.
%post hdfs
getent group hadoop >/dev/null && /usr/sbin/usermod -G hadoop hdfs || true

%preun
if [ "$1" = 0 ]; then
  # Stop any services that might be running
  for service in %{hadoop_services}
  do
     service hadoop-$service stop 1>/dev/null 2>/dev/null || :
  done
  %{alternatives_cmd} --remove %{name}-conf %{etc_hadoop}/conf.empty || :
fi

%preun httpfs
if [ $1 = 0 ]; then
  service %{name}-httpfs stop > /dev/null 2>&1
  chkconfig --del %{name}-httpfs
  %{alternatives_cmd} --remove %{name}-httpfs-conf %{etc_httpfs}/conf.empty || :
fi

%postun httpfs
if [ $1 -ge 1 ]; then
  service %{name}-httpfs condrestart >/dev/null 2>&1
fi

%post libhdfs
/sbin/ldconfig
# Force symlinks to be created if they are not
#   Otherwise shared linking can be broken from hadoop-0.20 to hadoop 2.0.0
if [ $1 -gt 0 ]; then
    for link in %{_libdir}/libhdfs.so.0 %{_libdir}/libhdfs.so.0.0; do
        [[ ! -e $link ]] && ln -s %{_libdir}/libhdfs.so.0.0.0 $link || :
    done
fi


%postun libhdfs
/sbin/ldconfig
if [ $1 -eq 0 ]; then
    # Now delete symlinks
    for link in %{_libdir}/libhdfs.so.0 %{_libdir}/libhdfs.so.0.0; do
        [[ -L $link ]] && rm -f $link || :
    done
fi


%post hdfs-fuse-selinux
# Install SELinux policy modules
for selinuxvariant in %{selinux_variants}
do
  /usr/sbin/semodule -s ${selinuxvariant} -i \
    %{_datadir}/selinux/${selinuxvariant}/%{name}.pp &> /dev/null || :
done

%preun hdfs-fuse-selinux
if [ "$1" -lt "1" ] ; then
    for variant in %{selinux_variants} ; do
        /usr/sbin/semodule -s ${variant} -r %{name} &> /dev/null || :
    done
fi

%postun hdfs-fuse-selinux
if [ "$1" -ge "1" ] ; then
    # Replace the module if it is already loaded. semodule -u also
    # checks the module version
    for variant in %{selinux_variants} ; do
        /usr/sbin/semodule -u %{_datadir}/selinux/${variant}/%{name}.pp || :
    done
fi


%files yarn
%defattr(-,root,root)
%config(noreplace) %{etc_hadoop}/conf.empty/yarn-env.sh
%config(noreplace) %{etc_hadoop}/conf.empty/yarn-site.xml
%config(noreplace) /etc/security/limits.d/yarn.conf
%{lib_hadoop}/libexec/yarn-config.sh
%{lib_yarn}
%attr(6050,root,yarn) %{lib_yarn}/bin/container-executor
%{bin_hadoop}/yarn
%attr(0775,yarn,hadoop) %{run_yarn}
%attr(0775,yarn,hadoop) %{log_yarn}
%attr(0775,yarn,hadoop) %{state_yarn}
%attr(1777,yarn,hadoop) %{state_yarn}/cache

%files hdfs
%defattr(-,root,root)
%config(noreplace) %{etc_hadoop}/conf.empty/hdfs-site.xml
%config(noreplace) /etc/default/hadoop-fuse
%config(noreplace) /etc/security/limits.d/hdfs.conf
%{lib_hdfs}
%{lib_hadoop}/libexec/hdfs-config.sh
%{bin_hadoop}/hdfs
%attr(0775,hdfs,hadoop) %{run_hdfs}
%attr(0775,hdfs,hadoop) %{log_hdfs}
%attr(0775,hdfs,hadoop) %{state_hdfs}
%attr(1777,hdfs,hadoop) %{state_hdfs}/cache

%files mapreduce
%defattr(-,root,root)
%config(noreplace) %{etc_hadoop}/conf.empty/mapred-site.xml
%config(noreplace) /etc/security/limits.d/mapreduce.conf
%{lib_mapreduce}
%{lib_hadoop}/libexec/mapred-config.sh
%{bin_hadoop}/mapred
%attr(0775,mapred,hadoop) %{run_mapreduce}
%attr(0775,mapred,hadoop) %{log_mapreduce}
%attr(0775,mapred,hadoop) %{state_mapreduce}
%attr(1777,mapred,hadoop) %{state_mapreduce}/cache


%files
%defattr(-,root,root)
%config(noreplace) %{etc_hadoop}/conf.empty/core-site.xml
%config(noreplace) %{etc_hadoop}/conf.empty/hadoop-metrics.properties
%config(noreplace) %{etc_hadoop}/conf.empty/hadoop-metrics2.properties
%config(noreplace) %{etc_hadoop}/conf.empty/log4j.properties
%config(noreplace) %{etc_hadoop}/conf.empty/slaves
%config(noreplace) %{etc_hadoop}/conf.empty/ssl-client.xml.example
%config(noreplace) %{etc_hadoop}/conf.empty/ssl-server.xml.example
%config(noreplace) /etc/default/hadoop
%{lib_hadoop}/*.jar
%{lib_hadoop}/lib
%{lib_hadoop}/sbin
%{lib_hadoop}/bin
%{lib_hadoop}/etc
%{lib_hadoop}/cloudera
%{lib_hadoop}/libexec/hadoop-config.sh
%{lib_hadoop}/libexec/hadoop-layout.sh
%{bin_hadoop}/hadoop
%{man_hadoop}/man1/hadoop.1.*

%files doc
%defattr(-,root,root)
%doc %{doc_hadoop}

%files httpfs
%defattr(-,root,root)
%config(noreplace) %{etc_httpfs}/conf.empty
%config(noreplace) /etc/default/%{name}-httpfs
%{lib_hadoop}/libexec/httpfs-config.sh
%{initd_dir}/%{name}-httpfs
%{lib_httpfs}
%attr(0775,httpfs,httpfs) %{run_httpfs}
%attr(0775,httpfs,httpfs) %{log_httpfs}

# Service file management RPMs
%define service_macro() \
%files %1 \
%defattr(-,root,root) \
%{initd_dir}/%{name}-%1 \
%config(noreplace) /etc/default/%{name}-%1 \
%post %1 \
chkconfig --add %{name}-%1 \
\
%preun %1 \
if [ $1 = 0 ]; then \
  service %{name}-%1 stop > /dev/null 2>&1 || :\
  chkconfig --del %{name}-%1 || :\
fi

%service_macro hdfs-namenode
%service_macro hdfs-secondarynamenode
%service_macro hdfs-zkfc
%service_macro hdfs-journalnode
%service_macro hdfs-datanode

#service_macro yarn-resourcemanager
#service_macro yarn-nodemanager
#service_macro yarn-proxyserver
#service_macro mapreduce-historyserver

# Pseudo-distributed Hadoop installation
%post conf-pseudo
%{alternatives_cmd} --install %{config_hadoop} %{name}-conf %{etc_hadoop}/conf.pseudo 30

%preun conf-pseudo
if [ "$1" = 0 ]; then
        %{alternatives_cmd} --remove %{name}-conf %{etc_hadoop}/conf.pseudo
        rm -f %{etc_hadoop}/conf
fi

%files conf-pseudo
%defattr(-,root,root)
%config(noreplace) %attr(755,root,root) %{etc_hadoop}/conf.pseudo

%files client
%defattr(-,root,root)
%{lib_hadoop}/client
%{lib_hadoop}/client-0.20

%files libhdfs
%defattr(-,root,root)
%{_libdir}/libhdfs*
%{_includedir}/hdfs.h
# -devel should be its own package
#%doc %{_docdir}/libhdfs-%{hadoop_version}

%files hdfs-fuse
%defattr(-,root,root)
%attr(0644,root,root) %config(noreplace) /etc/default/hadoop-fuse
%attr(0755,root,root) %{lib_hadoop}/bin/fuse_dfs
%attr(0755,root,root) %{bin_hadoop}/hadoop-fuse-dfs

%files hdfs-fuse-selinux
%defattr(-,root,root,-)
%doc SELinux/*.??
%{_datadir}/selinux/*/%{name}.pp




%changelog
* Sat Jan 16 2016 Carl Edquist <edquist@cs.wisc.edu> - 2.0.0+545-1.cdh4.1.1.p0.22
- Build for EL7 (SOFTWARE-2162)

* Thu Apr 10 2014 Edgar Fajardo <efajardo@physics.ucsd.edu> - 2.0.0+545-1.cdh4.1.1.p0.21
- Patch for error codes don't seem to be working HDFS-4997.patch SOFTWARE-2006

* Thu Apr 10 2014 Edgar Fajardo <efajardo@physics.ucsd.edu> - 2.0.0+545-1.cdh4.1.1.p0.20
- Adding a patch for large datanodes time out during block reports
- Credit to Erik Gough for providing the patch

* Tue Nov 12 2013 Matyas Selmeci <matyas@cs.wisc.edu> 2.0.0+545-1.cdh4.1.1.p0.19
- Build with Jeff Dost's extendable client patch (SOFTWARE-1184)

* Thu May 23 2013 Matyas Selmeci <matyas@cs.wisc.edu> - 2.0.0+545-1.cdh4.1.1.p0.18
- Fix creation of hdfs user in pre script
- Fix creation of httpfs user in pre script

* Tue May 21 2013 Matyas Selmeci <matyas@cs.wisc.edu> - 2.0.0+545-1.cdh4.1.1.p0.17
- Fix libhdfs postun script to not remove symlinks on upgrades
- Turn AutoReq back on

* Mon May 20 2013 Matyas Selmeci <matyas@cs.wisc.edu> - 2.0.0+545-1.cdh4.1.1.p0.16
- Add java7-devel dependency to hdfs-fuse subpackage -- needed for libjvm.so

* Thu May 16 2013 Matyas Selmeci <matyas@cs.wisc.edu> - 2.0.0+545-1.cdh4.1.1.p0.15
- Rebuild with java7

* Fri Dec 28 2012 Brian Bockelman <bbockelm@cse.unl.edu> - 2.0.0+545-1.cdh4.1.1.p0.14
- Fix chown implementation in FUSE.

* Mon Nov 26 2012 Doug Strain <dstrain@fnal.gov> - 2.0.0+545-1.cdh4.1.1.p0.13
- Fixing libhdfs obsoletes clauses

* Mon Nov 26 2012 Doug Strain <dstrain@fnal.gov> - 2.0.0+545-1.cdh4.1.1.p0.12
- Adding patches to fix libhdfs 
-- Credit to Brian Bockelman for providing the patches

* Wed Nov 21 2012 Doug Strain <dstrain@fnal.gov> - 2.0.0+545-1.cdh4.1.1.p0.11
- Forcing libhdfs symlinks to be created to fix linking on shared libs

* Thu Oct 18 2012 Doug Strain <dstrain@fnal.gov> - 2.0.0+545-1.cdh4.1.1.p0.10
- Adding ldconfig and requires java

* Thu Oct 18 2012 Doug Strain <dstrain@fnal.gov> - 2.0.0+545-1.cdh4.1.1.p0.6
- Repackaging for CDH4.1

* Thu Oct 4 2012 Doug Strain <dstrain@fnal.gov> - 2.0.0+88-1.cdh4.0.0.p0.39
- Got rid of postun script since it was failing.

* Tue Aug 7 2012 Doug Strain <dstrain@fnal.gov> - 2.0.0+88-1.cdh4.0.0.p0.33
- Changed hadoop-fuse default JAVA_HOME changes to a patch instead
- Added config path to classpath so fuse picks up default replication etc

* Wed Aug 1 2012 Doug Strain <dstrain@fnal.gov> - 2.0.0+88-1.cdh4.0.0.p0.31
- Changed hadoop init scripts to be off by default
- Added JAVA_HOME to hadoop-fuse default

* Tue Jul 17 2012 Doug Strain <dstrain@fnal.gov> - 2.0.0+88-1.cdh4.0.0.p0.30
- Initial packaging of Hadoop for OSG (based on Cloudera CDH4)
