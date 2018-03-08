set -x

#rm -rf proxy/bazel/base/external/local_config_cc/dummy_toolchain.bzl
#cp proxy/bazel/base/external/bazel_tools/tools/cpp/dummy_toolchain.bzl proxy/bazel/base/external/local_config_cc

rm -rf proxy/bazel
cp -rfL /tmp/bazel proxy

pushd proxy/bazel/base
rm -rf install
ln -s ../root/install/0ee37c46238c245908cbdbda1c10dbff/ install
popd

rm -rf proxy/bazel/base/external/envoy_deps_cache_fbe7fd77b8354b9a6f47b8e24c1a5f25

rm -rf proxy-full.tar.gz
tar cvf proxy-full.tar proxy
gzip proxy-full.tar

