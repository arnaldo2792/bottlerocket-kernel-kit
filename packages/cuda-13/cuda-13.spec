%global cuda_major 13
%global cuda_minor 0
%global cuda_ver %{cuda_major}.%{cuda_minor}
%global cuda_rpm_ver %{cuda_major}-%{cuda_minor}-%{cuda_major}.%{cuda_minor}.96-1
%global libcublas_rpm_ver %{cuda_major}-%{cuda_minor}-%{cuda_major}.1.0.3-1
%global culibos_rpm_ver %{cuda_major}-%{cuda_minor}-%{cuda_major}.%{cuda_minor}.85-1
%global crt_rpm_ver %{cuda_major}-%{cuda_minor}-%{cuda_major}.%{cuda_minor}.88-1
%global cccl_rpm_ver %{cuda_major}-%{cuda_minor}-%{cuda_major}.%{cuda_minor}.85-1

%if "%{?_cross_arch}" == "aarch64"
%global nvidia_arch sbsa
%else
%global nvidia_arch %{_cross_arch}
%endif

Name: %{_cross_os}cuda-13
Version: %{cuda_ver}
Release: 1%{?dist}
Summary: CUDA development libraries
License: LicenseRef-NVIDIA-AWS-EULA
URL: https://developer.nvidia.com/cuda-toolkit-archive
Source0: https://developer.download.nvidia.com/compute/cuda/repos/amzn2023/x86_64/cuda-driver-devel-%{cuda_rpm_ver}.x86_64.rpm 
Source1: https://developer.download.nvidia.com/compute/cuda/repos/amzn2023/sbsa/cuda-driver-devel-%{cuda_rpm_ver}.aarch64.rpm 
Source2: https://developer.download.nvidia.com/compute/cuda/repos/amzn2023/x86_64/libcublas-devel-%{libcublas_rpm_ver}.x86_64.rpm
Source3: https://developer.download.nvidia.com/compute/cuda/repos/amzn2023/sbsa/libcublas-devel-%{libcublas_rpm_ver}.aarch64.rpm
Source4: https://developer.download.nvidia.com/compute/cuda/repos/amzn2023/x86_64/cuda-cudart-devel-%{cuda_rpm_ver}.x86_64.rpm
Source5: https://developer.download.nvidia.com/compute/cuda/repos/amzn2023/sbsa/cuda-cudart-devel-%{cuda_rpm_ver}.aarch64.rpm
Source6: https://developer.download.nvidia.com/compute/cuda/repos/amzn2023/x86_64/cuda-culibos-devel-%{culibos_rpm_ver}.x86_64.rpm
Source7: https://developer.download.nvidia.com/compute/cuda/repos/amzn2023/sbsa/cuda-culibos-devel-%{culibos_rpm_ver}.aarch64.rpm
Source8: https://developer.download.nvidia.com/compute/cuda/repos/amzn2023/x86_64/cuda-crt-%{crt_rpm_ver}.x86_64.rpm
Source9: https://developer.download.nvidia.com/compute/cuda/repos/amzn2023/sbsa/cuda-crt-%{crt_rpm_ver}.aarch64.rpm
Source10: https://developer.download.nvidia.com/compute/cuda/repos/amzn2023/x86_64/cuda-cccl-%{cccl_rpm_ver}.x86_64.rpm
Source11: https://developer.download.nvidia.com/compute/cuda/repos/amzn2023/sbsa/cuda-cccl-%{cccl_rpm_ver}.aarch64.rpm
Source12: https://developer.download.nvidia.com/compute/cuda/repos/amzn2023/x86_64/cuda-cudart-%{cuda_rpm_ver}.x86_64.rpm
Source13: https://developer.download.nvidia.com/compute/cuda/repos/amzn2023/sbsa/cuda-cudart-%{cuda_rpm_ver}.aarch64.rpm
Source14: https://developer.download.nvidia.com/compute/cuda/repos/amzn2023/x86_64/libcublas-%{libcublas_rpm_ver}.x86_64.rpm
Source15: https://developer.download.nvidia.com/compute/cuda/repos/amzn2023/sbsa/libcublas-%{libcublas_rpm_ver}.aarch64.rpm
Source16: NVidiaEULAforAWS.pdf

%description
%{summary}.

%package cudart
Summary: CUDA Runtime Library
Requires: %{name}

%description cudart
%{summary}.

%package cublas
Summary: CUDA cuBLAS Library
Requires: %{name}

%description cublas
%{summary}.

# TODO: cccl can be its own devel package?
%package devel
Summary: File for development with CUDA libraries
Requires: %{name}
Requires: %{name}-cudart
Requires: %{name}-cublas

%description devel
%{summary}.

%prep
mkdir cuda
rpm2cpio %{_sourcedir}/cuda-driver-devel-%{cuda_rpm_ver}.%{_cross_arch}.rpm | cpio -idmv -D cuda
rpm2cpio %{_sourcedir}/libcublas-devel-%{libcublas_rpm_ver}.%{_cross_arch}.rpm | cpio -idmv -D cuda
rpm2cpio %{_sourcedir}/cuda-cudart-devel-%{cuda_rpm_ver}.%{_cross_arch}.rpm | cpio -idmv -D cuda
rpm2cpio %{_sourcedir}/cuda-culibos-devel-%{culibos_rpm_ver}.%{_cross_arch}.rpm | cpio -idmv -D cuda
rpm2cpio %{_sourcedir}/cuda-crt-%{crt_rpm_ver}.%{_cross_arch}.rpm | cpio -idmv -D cuda
rpm2cpio %{_sourcedir}/cuda-cccl-%{cccl_rpm_ver}.%{_cross_arch}.rpm | cpio -idmv -D cuda
rpm2cpio %{_sourcedir}/cuda-cudart-%{cuda_rpm_ver}.%{_cross_arch}.rpm | cpio -idmv -D cuda
rpm2cpio %{_sourcedir}/libcublas-%{libcublas_rpm_ver}.%{_cross_arch}.rpm | cpio -idmv -D cuda

# Unnecessary files
rm -rf cuda/usr/local/cuda-13.0/src cuda/usr/share/

%build

%install
%global cuda_root %{_cross_libdir}/cuda
%global cuda_13_root %{cuda_root}/cuda-13.0
%global cuda_13_targets %{cuda_13_root}/targets/%{nvidia_arch}-linux
%global cuda_13_include %{cuda_13_targets}/include
%global cuda_13_lib %{cuda_13_targets}/lib
%global cuda_13_lib_stubs %{cuda_13_targets}/lib/stubs

install -d %{buildroot}%{_cross_pkgconfigdir}
install -d %{buildroot}%{cuda_root}
install -d %{buildroot}%{cuda_13_root}
install -d %{buildroot}%{cuda_13_targets}
install -d %{buildroot}%{cuda_13_lib}
install -d %{buildroot}%{cuda_13_lib_stubs}
install -d %{buildroot}%{cuda_13_include}

pushd cuda/usr/local/cuda-13.0/targets/%{nvidia_arch}-linux/
# Libraries in this directory are used by applications at runtime they can
# be provided at the standard location
pushd lib
install -p -m 0755 *.so* %{buildroot}%{_cross_libdir}
install -p -m 0644 *.a %{buildroot}%{_cross_libdir}
rm -rf *.so* *.a
popd

# Stub libraries are installed in this directory and are used for development
# only. They provide symbols at build time and the produced artifacts load from
# actual library from the host, which provides the functionality (the userspace
# libraries provided by the NVIDIA kmods).
pushd lib/stubs
for f in $(find -name "*.so"); do
  install "$f" %{buildroot}%{cuda_13_lib_stubs}
  rm -rf "$f"
done
popd

# Install CMAKE files, downstream applications require them
pushd lib/cmake
install -d %{buildroot}%{_cross_libdir}/cmake
# Create directory structure
for f in $(find -type d); do
  install -d "%{buildroot}%{_cross_libdir}/cmake/$f"
done

for f in $(find -type f); do
  install -d "%{buildroot}%{_cross_libdir}/cmake/$f"
  rm -rf "$f"
done
popd

# Create headers directory structure, it is too nested and there are too many
# directories to do this by hand
pushd include
for d in $(find -type d); do
  install -d "%{buildroot}%{cuda_13_include}/$d"
done
popd

# Non-executable files (headers)
for f in $(find -type f ! -executable); do
  install -p -m 0644 "$f" "%{buildroot}%{cuda_13_targets}/$f"
  rm -rf "$f"
done
popd

pushd cuda/usr/lib64/pkgconfig/
install -p -m 0644 *.pc %{buildroot}%{_cross_pkgconfigdir}
rm -rf *.pc
popd

install -p -m 0644 %{S:16} .

# Fail if there was a file that wasn't processed
missing="$(find cuda -type f)"
if [[ -n "${missing}" ]]; then
  echo "Uninstalled files: ${missing}"
  exit 1
fi

%files
%license NVidiaEULAforAWS.pdf
%dir %{cuda_13_root}
%dir %{cuda_13_targets}
%dir %{cuda_13_lib}
%{_cross_attribution_file}

%files cudart
%{_cross_libdir}/libcudart.so.*

%files cublas
%{_cross_libdir}/libcublas.so.*
%{_cross_libdir}/libcublasLt.so.*
%{_cross_libdir}/libnvblas.so.*

%files devel
%{_cross_pkgconfigdir}
%{_cross_libdir}/cmake
%{_cross_libdir}/*.so
%{_cross_libdir}/*.a
%dir %{cuda_13_include}
%{cuda_13_include}
%dir %{cuda_13_lib_stubs}
%{cuda_13_lib_stubs}

%changelog
