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
%global project         istio
%global repo            proxy
# https://github.com/istio/proxy
%global provider_prefix %{provider}.%{provider_tld}/%{project}/%{repo}
%global import_path     proxy

%define _disable_source_fetch 0

Name:           proxy
Version:        0.6.%{git_bump}.git.%{git_shortcommit}
Release:        1%{?dist}
Summary:        The Istio Proxy is a microservice proxy that can be used on the client and server side, and forms a microservice mesh. The Proxy supports a large number of features.
License:        ASL 2.0
URL:            https://%{provider_prefix}
# TODO: Change to a release version
Source0:        proxy.tar.gz
Source1:        bazel-0.11.0-installer-linux-x86_64.sh
Source2:        proxy-cache.tar.gz


# e.g. el6 has ppc64 arch without gcc-go, so EA tag is required
#ExclusiveArch:  %{?go_arches:%{go_arches}}%{!?go_arches:%{ix86} x86_64 aarch64 %{arm}}
# If go_compiler is not set to 1, there is no virtual provide. Use golang instead.
#BuildRequires:  golang >= 1.9

%description
The Istio Proxy is a microservice proxy that can be used on the client and server side, and forms a microservice mesh. The Proxy supports a large number of features.

########### istio-proxy ###############
%package envoy
Summary:  The istio envoy proxy
Requires: istio-proxy = %{version}-%{release}

%description envoy
The Istio Proxy is a microservice proxy that can be used on the client and server side, and forms a microservice mesh. The Proxy supports a large number of features.

This package contains the envoy program.

istio-proxy is the proxy required by the Istio Pilot Agent that talks to Istio pilot

%prep
%setup -q -n %{name}

tar xvf %{SOURCE2} -C /tmp

%build

mkdir -p /tmp/tmpcache
#bazel --output_user_root=/tmp/cache version
bazel --output_user_root=/tmp/tmpcache build --config=release --fetch=false //... || :

pushd /tmp/tmpcache
WORKSPACE_HASH=$(find . -maxdepth 1 -type d -not -name "HASH" -not -name "install" | sed "s/.//" | sed "s/\///")
WORKSPACE_HASH=$(echo $WORKSPACE_HASH)
popd

pushd /tmp/tmpcache/install
MANIFEST_HASH=$(find . -maxdepth 1 -type d -not -name "HASH" -not -name "install" | sed "s/.//" | sed "s/\///")
MANIFEST_HASH=$(echo $MANIFEST_HASH)
popd

mv /tmp/cache/HASH /tmp/cache/${WORKSPACE_HASH}
mv /tmp/cache/install/HASH /tmp/cache/install/${MANIFEST_HASH}

bazel --output_user_root=/tmp/cache build --config=release --fetch=false //...

%install
rm -rf $RPM_BUILD_ROOT
mkdir -p $RPM_BUILD_ROOT%{_bindir}

cp -pav bazel-bin/src/envoy/envoy $RPM_BUILD_ROOT%{_bindir}/

%files envoy
%{_bindir}/envoy

%changelog
* Mon Mar 5 2018 Bill DeCoste <wdecoste@redhat.com>
- First package 
