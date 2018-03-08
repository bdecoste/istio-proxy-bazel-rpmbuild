set -x
set -e

mock -r epel-7-x86_64 --old-chroot --clean
mock -r epel-7-x86_64 --old-chroot --init
mock -r epel-7-x86_64 --old-chroot --install devtoolset-4-gcc
mock -r epel-7-x86_64 --old-chroot --install devtoolset-4-gcc-c++
mock -r epel-7-x86_64 --old-chroot --install devtoolset-4-libatomic-devel
mock -r epel-7-x86_64 --old-chroot --install devtoolset-4-libstdc++-devel
mock -r epel-7-x86_64 --old-chroot --install bazel
mock -r epel-7-x86_64 --old-chroot --install wget
mock -r epel-7-x86_64 --old-chroot --install git
mock -r epel-7-x86_64 --old-chroot --install libtool
mock -r epel-7-x86_64 --old-chroot --install cmake3
mock -r epel-7-x86_64 --old-chroot --install golang

#mock -r epel-7-x86_64 --old-chroot --install strace

#mock -r epel-7-x86_64 --old-chroot --no-clean --rebuild proxy-0.6.1.git.f005e33-1.el7.src.rpm

