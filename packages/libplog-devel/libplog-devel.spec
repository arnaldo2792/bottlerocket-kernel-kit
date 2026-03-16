%global debug_package %{nil}

Name: %{_cross_os}libplog-devel
Version: 1.1.11
Release: 1%{?dist}
Summary: Portable, simple and extensible C++ logging library
License: MIT
URL: https://github.com/SergiusTheBest/plog
Source0: https://github.com/SergiusTheBest/plog/archive/%{version}/plog-%{version}.tar.gz

%description
%{summary}.

%prep
%autosetup -n plog-%{version} -p1

%build
%{cross_cmake} . \
  -DPLOG_BUILD_SAMPLES:BOOL=OFF \
  -DPLOG_BUILD_TESTS:BOOL=OFF \
  -DCMAKE_INSTALL_PREFIX:PATH=%{_cross_prefix} \
  -G Ninja

cmake --build .

%install
DESTDIR="%{buildroot}" cmake --install .

%files
%license LICENSE
%{_cross_includedir}/*
%{_cross_attribution_file}
%{_cross_libdir}/cmake
%exclude %{_cross_docdir}
%changelog
