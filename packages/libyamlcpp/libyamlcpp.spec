%define debug_package %{nil}

Name: %{_cross_os}libyamlcpp
Version: 0.9.0
Release: 1%{?dist}
Summary: A YAML parser and emitter in C++
License: MIT
URL: https://github.com/jbeder/yaml-cpp
Source0: https://github.com/jbeder/yaml-cpp/archive/yaml-cpp-%{version}/yaml-cpp-yaml-cpp-%{version}.tar.gz

%description
%{summary}.

%package devel
Summary: Files for development using the C++ YAML library
Requires: %{name}

%description devel
%{summary}.

%prep
%autosetup -n yaml-cpp-yaml-cpp-%{version} -p1

%build
%{cross_cmake} . \
  -DYAML_BUILD_SHARED_LIBS:BOOL=ON \
  -DYAML_CPP_BUILD_TESTS:BOOL=OFF \
  -DYAML_CPP_BUILD_TOOLS:BOOL=OFF \
  -DCMAKE_POSITION_INDEPENDENT_CODE:BOOL=ON \
  -DCMAKE_INSTALL_PREFIX:PATH=%{_cross_prefix} \
  -DYAML_ENABLE_PIC:BOOL=ON \
  -G Ninja

cmake --build .

%install
DESTDIR="%{buildroot}" cmake --install .

%files
%license LICENSE
%{_cross_attribution_file}
%{_cross_libdir}/*.so.*

%files devel
%{_cross_libdir}/*.so
%{_cross_libdir}/cmake/
%{_cross_includedir}/*
%{_cross_pkgconfigdir}/*.pc

%changelog
