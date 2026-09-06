# Tensor contractions for HIP. TheRock 10.0.

Name:		hiptensor
Version:	10.0.0
Release:	1
Summary:	HIP tensor contraction library
License:	MIT
Group:		System/Libraries
URL:		https://github.com/ROCm/rocm-libraries
Source0:	https://github.com/ROCm/rocm-libraries/releases/download/therock-10.0/hiptensor.tar.gz#/hiptensor-%{version}.tar.gz

BuildRequires:	rocm-rpm-macros
BuildRequires:	cmake
BuildRequires:	ninja
BuildRequires:	rocm-cmake
BuildRequires:	hipcc
BuildRequires:	rocm-hip-devel
BuildRequires:	composable-kernel-devel
BuildRequires:	clang >= %{rocm_llvm_maj_ver}

%description
hipTensor implements tensor contractions and permutations on HIP,
built on Composable Kernel.

%package devel
Summary:	Development files for %{name}
Group:		Development/C++
Requires:	%{name}%{?_isa} = %{version}-%{release}

%description devel
Headers and CMake package for hipTensor.

%prep
%autosetup -n hiptensor -p1

%build
export CXX=hipcc
export CC=clang
CXXFLAGS=$(printf '%s' "%{optflags}" | sed -E 's/-mfpmath=[^ ]+//g')
export CXXFLAGS
%cmake %{rocm_cmake_fhs} %{rocm_cmake_gpu_targets} \
	-DCMAKE_BUILD_TYPE=Release \
	-DCMAKE_CXX_COMPILER=hipcc \
	-DHIPTENSOR_BUILD_TESTS=OFF \
	-DHIPTENSOR_BUILD_SAMPLES=OFF \
	-DROCM_PATH=%{_prefix} \
	-DCMAKE_PREFIX_PATH=%{_prefix} \
	-G Ninja
%ninja_build -C build

%install
%ninja_install -C build

%files
%license LICENSE.md
%doc README.md
%{_libdir}/libhiptensor.so.*

%files devel
%{_includedir}/hiptensor/
%{_libdir}/libhiptensor.so
%{_libdir}/cmake/hiptensor/
