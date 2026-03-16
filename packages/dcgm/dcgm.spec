%define debug_package %{nil}

%global dcgm_major 4
%global dcgm_minor 4
%global dcgm_patch 2
%global dcgm_version %{dcgm_major}.%{dcgm_minor}.%{dcgm_patch}

Name: %{_cross_os}dcgm
Version: %{dcgm_version}
Release: 1%{?dist}
Summary: NVIDIA Data Center GPU Manager
License: Apache-2.0
URL: https://github.com/NVIDIA/DCGM
Source0: https://github.com/NVIDIA/DCGM/archive/v%{version}/DCGM-v%{version}.tar.gz
Source1: nvidia-dcgm.service
Source2: dcgm-sysusers.conf
Source3: dcgm-tmpfilesd.conf

Patch0001: 0001-CMakeLists-don-t-force-the-Catch2-dependency.patch
Patch0002: 0002-FindCuda-build-plugins-only-for-the-CUDA-versions-fo.patch
Patch0003: 0003-Fix-missing-include-headers.patch
Patch0004: 0004-cmake-guard-stub_library_test-behind-BUILD_TESTING.patch
Patch0005: 0005-Fix-compiler-warnings.patch
Patch0006: 0006-modules-mndiag-make-additional-binaries-optional.patch

BuildRequires: %{_cross_os}cuda-13-devel
BuildRequires: %{_cross_os}libboost-devel
BuildRequires: %{_cross_os}libevent-devel
BuildRequires: %{_cross_os}libfmt-devel
BuildRequires: %{_cross_os}libjsoncpp-devel
BuildRequires: %{_cross_os}libplog-devel
BuildRequires: %{_cross_os}libtclap-devel
BuildRequires: %{_cross_os}libyamlcpp-devel

Requires: %{_cross_os}cuda-13-cudart
Requires: %{_cross_os}cuda-13-cublas
Requires: %{_cross_os}libboost
Requires: %{_cross_os}libfmt
Requires: %{_cross_os}libnuma
Requires: %{_cross_os}libnvidia-nscq-580

%description
%{summary}.

%package devel
Summary: Development files for the libdcgm library
Requires: %{name}

%description devel
%{summary}.

%prep
%autosetup -n DCGM-%{version} -p1
# DCGM uses CMAKE as its build system so ideally it would use the cross_cmake
# macro. However, DCGM's compilation breaks when '--as-needed' and LTO are used.
# Since the macro writes the toolchain configuration file everytime its called,
# we can't control what goes into the LDFLAGS or CFLAGS with the macro.
# Instead, we prepare the toolchain configuration file and strip what breaks the
# compilation while keeping all other flags.
%write_cross_cmake_toolchain_conf

# Append linker flags to toolchain configuration file, so that unsupported
# flags can be replaced while all other flags provided by the SDK are kept.
cat >> %_cross_cmake_toolchain_conf << 'CROSS_CMAKE_TOOLCHAIN_EOF'
set(CMAKE_C_LINK_FLAGS "%{_cross_ldflags}")
set(CMAKE_CXX_LINK_FLAGS "%{_cross_ldflags}")
CROSS_CMAKE_TOOLCHAIN_EOF

# Remove unsupported linker flags and disable LTO, since this breaks how DCGM
# links agaisnt static libraries
sed -i -e 's/-Wl,--as-needed//g' \
  -e 's/-flto=auto -ffat-lto-objects//g' \
  %_cross_cmake_toolchain_conf

# Relax compiler errors on warnings
# TODO: The DCGM sources have too many compiler violations, some of them were
# fixed. 
sed -i 's/-Werror=format-security/-Wno-format-security -Wno-unused-result/g' \
  %_cross_cmake_toolchain_conf

%build
# Override the LDFLAGS after all the other cross-build flags are set. This is
# safe at this point since CMAKE will use the flags in the toolchain file.
CMAKE_TOOLCHAIN_FILE="%{_cross_cmake_toolchain_conf}" \
  export CMAKE_TOOLCHAIN_FILE ; \
  %set_cross_build_flags \
  export LDFLAGS="" ; \
  %{__cmake} . \
    -DINCLUDE_INSTALL_DIR:PATH=%{_cross_includedir} \
    -DLIB_INSTALL_DIR:PATH=%{_cross_libdir} \
    -DSYSCONF_INSTALL_DIR:PATH=%{_cross_sysconfdir} \
    -DSHARE_INSTALL_PREFIX:PATH=%{_cross_datadir} \
    -DCMAKE_INSTALL_PREFIX:PATH=%{_cross_prefix} \
    -DCUDA_ROOT=%{_cross_libdir}/cuda \
    -DBUILD_SHARED_LIBS:BOOL=ON \
    -DDCGM_BUILD_MULTINODE:BOOL=OFF \
    -DBUILD_TESTING:BOOL=OFF \
    -G Ninja

cmake --build . -v

%install
DESTDIR="%{buildroot}" cmake --install .

rm -rf %{buildroot}%{_cross_unitdir}/nvidia-dcgm.service
install -p -m 0644 %{S:1} %{buildroot}%{_cross_unitdir}
install -d %{buildroot}%{_cross_sysusersdir}
install -m 0644 %{S:2} %{buildroot}%{_cross_sysusersdir}/nvidia-dcgm.conf
install -d %{buildroot}%{_cross_tmpfilesdir }
install -m 0644 %{S:3} %{buildroot}%{_cross_tmpfilesdir}/nvidia-dcgm.conf

%files
%license LICENSE
%{_cross_attribution_file}
%{_cross_libdir}/*.so.*
%{_cross_bindir}/dcgmi
%{_cross_bindir}/nv-hostengine
%{_cross_libexecdir}/datacenter-gpu-manager-%{dcgm_major}/plugins/cudaless/*.so.*
%{_cross_libexecdir}/datacenter-gpu-manager-%{dcgm_major}/nvvs
%{_cross_libexecdir}/datacenter-gpu-manager-%{dcgm_major}/DcgmProfTesterKernels.ptx
%{_cross_unitdir}/nvidia-dcgm.service
%{_cross_sysusersdir}/nvidia-dcgm.conf
%{_cross_tmpfilesdir}/nvidia-dcgm.conf
%{_cross_bindir}/dcgmproftester13
%dir %{_cross_libexecdir}/datacenter-gpu-manager-%{dcgm_major}/plugins/cuda13
%{_cross_libexecdir}/datacenter-gpu-manager-%{dcgm_major}/plugins/cuda13
%exclude %{_cross_docdir}
%exclude %{_cross_usrsrc}
%exclude %{_cross_datadir}/dcgm_tests
%exclude %{_cross_datadir}/datacenter-gpu-manager-%{dcgm_major}/bindings
%exclude %{_cross_datadir}/datacenter-gpu-manager-%{dcgm_major}/collectd
%exclude %{_cross_sbindir}/gather-dcgm-logs.sh
%exclude %{_cross_rootdir}%{_systemdgeneratordir}/nvidia-dcgm-multinode-diagnostics-generator.sh

%files devel
%{_cross_libdir}/*.so
%{_cross_libdir}/*.a
%{_cross_includedir}/datacenter-gpu-manager-%{dcgm_major}/*.h
%{_cross_datadir}/cmake/

%changelog
