# Generate devel rpm
%global with_devel 0
# Build with debug info rpm
%global with_debug 0

%if 0%{?with_debug}
%global _dwz_low_mem_die_limit 0
%else
%global debug_package   %{nil}
%endif

# https://github.com/istio/proxy
%global provider        github
%global provider_tld    com
%global project         istio
%global repo            proxy
%global provider_prefix %{provider}.%{provider_tld}/%{project}/%{repo}

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
BuildRequires:  llvm-toolset-7-cmake
BuildRequires:  llvm-toolset-7-runtime
BuildRequires:  llvm-toolset-7-cmake-data
BuildRequires:  libtool
BuildRequires:  golang
#BuildRequires:  strace

# TODO: Change to a release version
Source0:        proxy-full.tar.xz

%description
The Istio Proxy is a microservice proxy that can be used on the client and server side, and forms a microservice mesh. The Proxy supports a large number of features.

########### istio-proxy ###############
%package istio-proxy
Summary:  The istio envoy proxy

%description istio-proxy
The Istio Proxy is a microservice proxy that can be used on the client and server side, and forms a microservice mesh. The Proxy supports a large number of features.

This package contains the envoy program.

istio-proxy is the proxy required by the Istio Pilot Agent that talks to Istio pilot

%prep
%setup -q -n %{name}

%build

#ln -s /usr/bin/cmake3 cmake
if [[ ${PATH} != *"llvm-toolset"* ]]; then
  source /opt/rh/llvm-toolset-7/enable
fi

if [[ ${PATH} != *"devtoolset"* ]]; then
  source /opt/rh/devtoolset-4/enable
fi

ln -s /usr/bin/aclocal aclocal-1.15
ln -s /usr/bin/automake automake-1.15

export PATH=$(pwd):$PATH

cd proxy

bazel --output_base=${RPM_BUILD_DIR}/istio-proxy/bazel/base --output_user_root=${RPM_BUILD_DIR}/istio-proxy/bazel/root --batch build --config=release "//..."
#bazel --batch build --config=release --experimental_external_repositories --experimental_repository_cache=${RPM_BUILD_DIR}/istio-proxy/bazel/X "//..."

#bazel --output_base=${RPM_BUILD_DIR}/proxy/bazel/base --output_user_root=${RPM_BUILD_DIR}/proxy/bazel/root --batch build --config=release "//src/envoy -//external:android/crosstool -//external:android/sdk -//external:android/dx_jar_import -//external:android_sdk_for_testing -//external:android_ndk_for_testing -//external:has_androidsdk -//external:java_toolchain -//external:databinding_annotation_processor -//external:local_jdk -//external:jre-default -//external:jre -//external:jni_md_header-linux -//external:jni_md_header-freebsd -//external:jni_md_header-darwin -//external:jni_header -//external:jinja2 -//external:jdk-default -//external:jdk -//external:javac -//external:java_toolchain -//external:java -//external:jar -//external:go_sdk -//tools/deb:all -//:deb_version -//:darwin -//src/envoy:envoy_tar"
#bazel --output_base=${RPM_BUILD_DIR}/proxy/bazel/base --output_user_root=${RPM_BUILD_DIR}/proxy/bazel/root --batch version 

%install
rm -rf $RPM_BUILD_ROOT
mkdir -p $RPM_BUILD_ROOT%{_bindir}

cp -pav ${RPM_BUILD_DIR}/istio-proxy/proxy/bazel-bin/src/envoy/envoy $RPM_BUILD_ROOT%{_bindir}/

%files
%{_bindir}/envoy

%changelog
* Mon Mar 5 2018 Bill DeCoste <wdecoste@redhat.com>
- First package 
