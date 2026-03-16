Name: %{_cross_os}libnuma
Version: 2.0.19
Release: 1%{?dist}
Summary: NUMA policy library
License: GPL-2.0-only AND LGPL-2.1-only
URL: https://github.com/numactl/numactl
Source0: https://github.com/numactl/numactl/archive/v%{version}/numactl-v%{version}.tar.gz

%description
%{summary}.

%package devel
Summary: Files for development using the NUMA policy library
Requires: %{name}

%description devel
%{summary}.

%prep
%autosetup -n numactl-%{version} -p1

%build
autoreconf -fi
%cross_configure \
  --disable-static \
  --enable-shared \

%force_disable_rpath

%make_build

%install
%make_install

%files
%license LICENSE.GPL2 LICENSE.LGPL2.1
%{_cross_attribution_file}
%{_cross_libdir}/*.so.*
%exclude %{_cross_bindir}
%exclude %{_cross_docdir}
%exclude %{_cross_mandir}

%files devel
%{_cross_libdir}/*.so
%{_cross_includedir}/*
%{_cross_pkgconfigdir}/*.pc

%changelog
