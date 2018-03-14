# Generate devel rpm
%global with_devel 0
# Build with debug info rpm
%global with_debug 0

%if 0%{?with_debug}
%global _dwz_low_mem_die_limit 0
%else
%global debug_package   %{nil}
%endif

# this is just a monotonically increasing number to preceed the git hash, to get incremented on every git bump
%global git_bump         1
%global git_commit       f005e33859d423c545bd6d2360231dfe46751aa7
%global git_shortcommit  %(c=%{git_commit}; echo ${c:0:7})

%global provider        github
%global provider_tld    com
%global project         istio-proxy
%global repo            istio-proxy
# https://github.com/istio/proxy
%global provider_prefix %{provider}.%{provider_tld}/%{project}/%{repo}
%global import_path     proxy

Name:           istio-proxy
Version:        0.6.0
Release:        1%{?dist}
Summary:        The Istio Proxy is a microservice proxy that can be used on the client and server side, and forms a microservice mesh. The Proxy supports a large number of features.
License:        ASL 2.0
URL:            https://%{provider_prefix}
BuildRequires:  bazel
BuildRequires:  devtoolset-4-gcc
BuildRequires:  devtoolset-4-gcc-c++
BuildRequires:  devtoolset-4-libatomic-devel
BuildRequires:  devtoolset-4-libstdc++-devel
BuildRequires:  devtoolset-4-runtime
BuildRequires:  wget
BuildRequires:  git
BuildRequires:  cmake3
BuildRequires:  libtool
BuildRequires:  golang

#BuildRequires:  strace

# TODO: Change to a release version
Source0:        proxy-full.tar.xz


# e.g. el6 has ppc64 arch without gcc-go, so EA tag is required
#ExclusiveArch:  %{?go_arches:%{go_arches}}%{!?go_arches:%{ix86} x86_64 aarch64 %{arm}}
# If go_compiler is not set to 1, there is no virtual provide. Use golang instead.
#BuildRequires:  golang >= 1.9

%description
The Istio Proxy is a microservice proxy that can be used on the client and server side, and forms a microservice mesh. The Proxy supports a large number of features.

########### istio-proxy ###############
%package istio-proxy
Summary:  The istio envoy proxy
Requires: istio-proxy = %{version}-%{release}

%description istio-proxy
The Istio Proxy is a microservice proxy that can be used on the client and server side, and forms a microservice mesh. The Proxy supports a large number of features.

This package contains the envoy program.

istio-proxy is the proxy required by the Istio Pilot Agent that talks to Istio pilot

%prep
%setup -q -n %{name}

ME=$(whoami)
chown -R ${ME}:${ME} ${RPM_BUILD_DIR}/istio-proxy

rm -rf /usr/bin/cmake
ln -s /usr/bin/cmake3 /usr/bin/cmake
rm -rf /usr/bin/aclocal-1.15
ln -s /usr/bin/aclocal /usr/bin/aclocal-1.15
rm -rf /usr/bin/automake-1.15
ln -s /usr/bin/automake /usr/bin/automake-1.15

#if [[ ${PATH} != *"devtoolset"* ]]; then
#    source /opt/rh/devtoolset-4/enable
#fi

echo $PATH
which g++
g++ --version

%build

cd proxy

bazel --output_base=${RPM_BUILD_DIR}/istio-proxy/bazel/base --output_user_root=${RPM_BUILD_DIR}/istio-proxy/bazel/root --batch build --config=release "//..."
#bazel --output_base=${RPM_BUILD_DIR}/proxy/bazel/base --output_user_root=${RPM_BUILD_DIR}/proxy/bazel/root --batch build --config=release "//src/envoy -//external:android/crosstool -//external:android/sdk -//external:android/dx_jar_import -//external:android_sdk_for_testing -//external:android_ndk_for_testing -//external:has_androidsdk -//external:java_toolchain -//external:databinding_annotation_processor -//external:local_jdk -//external:jre-default -//external:jre -//external:jni_md_header-linux -//external:jni_md_header-freebsd -//external:jni_md_header-darwin -//external:jni_header -//external:jinja2 -//external:jdk-default -//external:jdk -//external:javac -//external:java_toolchain -//external:java -//external:jar -//external:go_sdk -//tools/deb:all -//:deb_version -//:darwin -//src/envoy:envoy_tar"
#bazel --output_base=${RPM_BUILD_DIR}/proxy/bazel/base --output_user_root=${RPM_BUILD_DIR}/proxy/bazel/root --batch version 

%install
rm -rf $RPM_BUILD_ROOT
mkdir -p $RPM_BUILD_ROOT%{_bindir}

cp -pav ${RPM_BUILD_DIR}/istio-proxy/proxy/bazel-bin/src/envoy/envoy $RPM_BUILD_ROOT%{_bindir}/

%files istio-proxy
%{_bindir}/envoy

%changelog
* Mon Mar 5 2018 Bill DeCoste <wdecoste@redhat.com>
- First package 
