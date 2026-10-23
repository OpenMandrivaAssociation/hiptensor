# Tensor contractions for HIP. TheRock 10.1.

# Fat HIP device instances. -flto plus ninja -j32 SIGKILL'd clang
# (znver1 680715, x86_64 680716). Without LTO, -j4 still cannot finish
# inside Timeout(36000): znver1 680758 was at 121/333 after 8h.
# aarch64 680717 at -j32 with -flto reached 113/333 and timed out.
# Device link time tracks the GPU list. hipTensor upstream does not
# support gfx803, gfx906, or gfx1030. aarch64 builds the RDNA3/4 set
# used by hipBLASLt. x86 also keeps CDNA gfx908/gfx90a/gfx942.
%define _disable_lto 1
%ifarch aarch64
%global ht_ninja_jobs 32
%global ht_gpu_targets gfx1100;gfx1101;gfx1200;gfx1201
%else
%global ht_ninja_jobs 8
%global ht_gpu_targets gfx908;gfx90a;gfx942;gfx1100;gfx1101;gfx1102;gfx1200;gfx1201
%endif

Name:		hiptensor
Version:	10.1.0
Release:	1
Summary:	HIP tensor contraction library
License:	MIT
Group:		System/Libraries
URL:		https://github.com/ROCm/rocm-libraries
Source0:	https://github.com/ROCm/rocm-libraries/releases/download/therock-10.1/hiptensor.tar.gz#/hiptensor-%{version}.tar.gz

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
%cmake %{rocm_cmake_fhs} \
	-DAMDGPU_TARGETS="%{ht_gpu_targets}" \
	-DGPU_TARGETS="%{ht_gpu_targets}" \
	-DCMAKE_BUILD_TYPE=Release \
	-DCMAKE_CXX_COMPILER=hipcc \
	-DHIPTENSOR_BUILD_TESTS=OFF \
	-DHIPTENSOR_BUILD_SAMPLES=OFF \
	-DROCM_PATH=%{_prefix} \
	-DCMAKE_PREFIX_PATH=%{_prefix} \
	-G Ninja
RPM_BUILD_NCPUS=%{ht_ninja_jobs}
export RPM_BUILD_NCPUS
%ninja_build

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
