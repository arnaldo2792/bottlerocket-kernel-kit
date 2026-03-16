%global nscq_ver 580.95.05

%if "%{?_cross_arch}" == "aarch64"
%global nvidia_arch sbsa
%else
%global nvidia_arch %{_cross_arch}
%endif

Name: %{_cross_os}libnvidia-nscq-580
Version: %{nscq_ver}
Release: 1%{?dist}
Summary: NVIDIA NVSwitch Configuration and Query library
License: LicenseRef-NVIDIA-AWS-EULA
URL: https://developer.nvidia.com/cuda-toolkit-archive
Source0: https://developer.download.nvidia.com/compute/cuda/repos/amzn2023/x86_64/libnvidia-nscq-%{nscq_ver}-1.x86_64.rpm
Source1: https://developer.download.nvidia.com/compute/cuda/repos/amzn2023/sbsa/libnvidia-nscq-%{nscq_ver}-1.aarch64.rpm

%description
%{summary}.

%prep
mkdir nscq
rpm2cpio %{_sourcedir}/libnvidia-nscq-%{nscq_ver}-1.%{_cross_arch}.rpm | cpio -idmv -D nscq

%build

%install
install -d %{buildroot}%{_cross_libdir}
install -m 755 nscq/usr/lib64/libnvidia-nscq.so.%{nscq_ver} %{buildroot}%{_cross_libdir}

# Create SONAME symlink
pushd nscq/usr/lib64
for lib in $(find -maxdepth 1 -type f -name 'libnvidia-nscq.so.*' -printf '%%P\n'); do
  soname="$(%{_cross_target}-readelf -d "${lib}" | awk '/SONAME/{print $5}' | tr -d '[]')"
  [ -n "${soname}" ] || continue
  [ "${lib}" == "${soname}" ] && continue
  ln -s "${lib}" %{buildroot}/%{_cross_libdir}/"${soname}"
done
popd

%files
%{_cross_attribution_file}
%{_cross_libdir}/libnvidia-nscq.so.*

%changelog
