Name: %{_cross_os}libevent
Version: 2.1.12
Release: 1%{?dist}
Summary: An event notification library
License: BSD-3-Clause
URL: https://libevent.org/
Source0: https://github.com/libevent/libevent/archive/release-2.1.12-stable/libevent-release-2.1.12-stable.tar.gz

%description
%{summary}.

%package devel
Summary: Files for development using libevent
Requires: %{name}

%description devel
%{summary}.

%prep
%autosetup -n libevent-release-2.1.12-stable -p1

%build
%{cross_cmake} . \
  -DCMAKE_SKIP_RPATH=ON \
  -DCMAKE_POSITION_INDEPENDENT_CODE=ON \
  -DEVENT__DISABLE_OPENSSL:BOOL=ON \
  -DEVENT__DISABLE_BENCHMARK:BOOL=ON \
  -DEVENT__DISABLE_TESTS:BOOL=ON \
  -DEVENT__DISABLE_REGRESS:BOOL=ON \
  -DEVENT__DISABLE_SAMPLES:BOOL=ON \
  -DEVENT__LIBRARY_TYPE:STRING=DEFAULT \
  -DCMAKE_INSTALL_PREFIX:PATH=%{_cross_prefix} \
  -G Ninja

cmake --build .

%install
DESTDIR="%{buildroot}" cmake --install .

%files
%license LICENSE
%{_cross_attribution_file}
%{_cross_libdir}/*.so.*
%exclude %{_cross_bindir}/*.py

%files devel
%{_cross_libdir}/*.so
%{_cross_libdir}/*.a
%dir %{_cross_includedir}
%{_cross_includedir}/*
%{_cross_pkgconfigdir}/*.pc
%{_cross_libdir}/cmake

%changelog
