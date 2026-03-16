%global debug_package %{nil}

Name: %{_cross_os}libtclap-devel
Version: 1.4.0
Release: 1%{?dist}
Summary: Files for development using the library for command line parsing
License: MIT
URL: http://tclap.sourceforge.net/
Source0: tclap.tar.gz
Patch0001: 0001-CMakeLists-prevent-installing-html-docs.patch

%description
%{summary}.

%prep
%autosetup -n tclap-82abdc943e23b2f91678fb86c436962182ca9a29 -p1

%build
%{cross_cmake} . \
  -DBUILD_DOC:BOOL=OFF \
  -DBUILD_EXAMPLES:BOOL=OFF \
  -DBUILD_UNITTESTS:BOOL=OFF \
  -DCMAKE_INSTALL_PREFIX:PATH=%{_cross_prefix} \
  -G Ninja

cmake --build .

%install
DESTDIR="%{buildroot}" cmake --install .

%files
%license COPYING
%{_cross_attribution_file}
%{_cross_includedir}/*
%{_cross_pkgconfigdir}/*.pc
%{_cross_libdir}/cmake

%changelog
