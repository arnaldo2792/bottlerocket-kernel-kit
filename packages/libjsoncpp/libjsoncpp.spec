%define debug_package %{nil}

Name: %{_cross_os}libjsoncpp
Version: 1.9.6
Release: 1%{?dist}
Summary: A C++ library for interacting with JSON
License: MIT
URL: https://github.com/open-source-parsers/jsoncpp
Source0: https://github.com/open-source-parsers/jsoncpp/archive/%{version}/jsoncpp-%{version}.tar.gz

%description
%{summary}.

%package devel
Summary: Files for development using the C++ JSON library
Requires: %{name}

%description devel
%{summary}.

%prep
%autosetup -n jsoncpp-%{version} -p1

%build
%global jsoncpp_build %{_builddir}/jsoncpp-build

mkdir %{jsoncpp_build}
pushd %{jsoncpp_build}
%{cross_cmake} ../jsoncpp-%{version} \
  -DCMAKE_INSTALL_PREFIX:PATH=%{_cross_prefix} \
  -DCMAKE_POSITION_INDEPENDENT_CODE:BOOL=ON \
  -DJSONCPP_WITH_TESTS:BOOL=OFF \
  -DJSONCPP_WITH_CMAKE_PACKAGE:BOOL=ON \
  -DJSONCPP_WITH_POST_BUILD_UNITTEST:BOOL=OFF \
  -DBUILD_STATIC_LIBS:BOOL=ON \
  -DBUILD_SHARED_LIBS:BOOL=ON \
  -DBUILD_OBJECT_LIBS:BOOL=OFF \
  -G Ninja

cmake --build .
popd

%install
pushd %{jsoncpp_build}
DESTDIR="%{buildroot}" cmake --install .
popd

%files
%license LICENSE
%{_cross_attribution_file}
%{_cross_libdir}/*.so.*

%files devel
%{_cross_libdir}/cmake
%{_cross_libdir}/*.a
%{_cross_libdir}/*.so
%{_cross_includedir}/*
%{_cross_pkgconfigdir}/*.pc

%changelog
