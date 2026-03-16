%define debug_package %{nil}

Name: %{_cross_os}libfmt
Version: 10.2.1
Release: 1%{?dist}
Summary: A modern formatting library for C++
License: MIT
URL: https://fmt.dev/
Source0: https://github.com/fmtlib/fmt/archive/%{version}/fmt-%{version}.tar.gz

%description
%{summary}.

%package devel
Summary: Files for development using the C++ formatting library
Requires: %{name}

%description devel
%{summary}.

%prep
%autosetup -n fmt-%{version} -p1

%build
%{cross_cmake} . \
  -DBUILD_SHARED_LIBS:BOOL=ON \
  -DBUILD_STATIC_LIBS:BOOL=OFF \
  -DCMAKE_POSITION_INDEPENDENT_CODE=ON \
  -DFMT_TEST:BOOL=OFF \
  -DFMT_DOC:BOOL=OFF \
  -DCMAKE_INSTALL_PREFIX:PATH=%{_cross_prefix} \
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
%{_cross_pkgconfigdir}/*.pc
%{_cross_libdir}/cmake
%{_cross_includedir}/*


%changelog
