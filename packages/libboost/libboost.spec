%define debug_package %{nil}

Name: %{_cross_os}libboost
Version: 1.85.0
Release: 1%{?dist}
Summary: Portable C++ source libraries
License: BSL-1.0
URL: https://www.boost.org/
Source0: https://github.com/boostorg/boost/releases/download/boost-%{version}/boost-%{version}-cmake.tar.gz

%description
%{summary}.

%package devel
Summary: Files for development using Boost
Requires: %{name}

%description devel
%{summary}.

%prep
%autosetup -n boost-%{version} -p1

%build
%{cross_cmake} . \
  -DBUILD_SHARED_LIBS=ON \
  -DBUILD_TESTING=OFF \
  -DBOOST_STACKTRACE_ENABLE_ADDR2LINE=OFF \
  -DBOOST_STACKTRACE_ENABLE_NOOP=OFF \
  -DBOOST_INCLUDE_LIBRARIES="algorithm;asio;circular_buffer;filesystem;iterator;process;regex;stacktrace;system;container;context;coroutine" \
  -DCMAKE_INSTALL_PREFIX:PATH=%{_cross_prefix} \
  -DCMAKE_POSITION_INDEPENDENT_CODE=ON \
  -G Ninja

cmake --build .

%install
DESTDIR="%{buildroot}" cmake --install .

%files
%license LICENSE_1_0.txt
%{_cross_attribution_file}
%{_cross_libdir}/*.so.*

%files devel
%{_cross_includedir}/boost/
%{_cross_libdir}/cmake/*
%{_cross_libdir}/*.so
%{_cross_libdir}/*.a

%changelog
