set -x

mkdir /tmp/proxy
pushd /tmp/proxy

if [ ! -d "proxy" ]; then
  #clone proxy
  PROXY_VERSION=0.6.0
  git clone https://github.com/istio/proxy -b ${PROXY_VERSION}
fi

if [ ! -d "recipes" ]; then
  git clone https://github.com/bdecoste/proxy-rpm
  mv proxy-rpm/proxy/* .
  rm -rf proxy-rpm
fi

if [ ! -d "bazelorig" ]; then
  #fetch 
  pushd /tmp/proxy/proxy
  bazel --output_base=/tmp/proxy/bazel/base --output_user_root=/tmp/proxy/bazel/root --batch fetch //...
  popd
  cp -rfp bazel bazelorig
fi

# replace links with copies (links are fully qualified paths so don't travel)
#cp -rfL /tmp/bazel proxy
rm -rf bazel
cp -rfp bazelorig bazel

INSTALL_HASH=e85ea7cbd5c513a863eccd3090ecfbd5

pushd /tmp/proxy/bazel
find . -lname '/*' -exec ksh -c '
  for link; do
    target=$(readlink "$link")
    link=${link#./}
    root=${link//+([!\/])/..}; root=${root#/}; root=${root%..}
    rm "$link"
    target="$root${target#/}"
#    echo "before $target    $link"
    target=$(echo $target | sed "s|../../../tmp/proxy/bazel/base|../../../base|")
    target=$(echo $target | sed "s|../../tmp/proxy/bazel/base|../../base|")
    target=$(echo $target | sed "s|../../../tmp/proxy/bazel/root|../../../root|")
    target=$(echo $target | sed "s|../tmp/proxy/bazel/root|../root|")
    target=$(echo $target | sed "s|../../../usr/lib/jvm|/usr/lib/jvm|")
#   echo "after  $target    $link"
    ln -s "$target" "$link"
  done
' _ {} +
popd

#prune git
find . -name ".git*" | xargs rm -rf

#prune logs
find . -name "*.log" | xargs rm -rf

#prune go sdk
GO_HOME=/usr/lib/golang
rm -rf bazel/base/external/go_sdk/{api,bin,lib,pkg,src,test,misc,doc,blog}
ln -s ${GO_HOME}/api bazel/base/external/go_sdk/api
ln -s ${GO_HOME}/bin bazel/base/external/go_sdk/bin
ln -s ${GO_HOME}/lib bazel/base/external/go_sdk/lib
ln -s ${GO_HOME}/pkg bazel/base/external/go_sdk/pkg
ln -s ${GO_HOME}/src bazel/base/external/go_sdk/src
ln -s ${GO_HOME}/test bazel/base/external/go_sdk/test

# remove fetch-build
ENVOY_HASH=2c744dffd279d7e9e0910ce594eb4f4f
rm -rf bazel/base/external/envoy_deps_cache_${ENVOY_HASH}

# use custom dependency recipes
cp -rf recipes/*.sh bazel/base/external/envoy/ci/build_container/build_recipes

# remove hardcoded path for g++
cp -f CROSSTOOL bazel/base/external/local_config_cc/CROSSTOOL

popd

# create tarball
pushd /tmp
rm -rf proxy-full.tar.gz
tar cvf proxy-full.tar proxy --exclude=proxy/bazelorig --atime-preserve
gzip proxy-full.tar
popd




