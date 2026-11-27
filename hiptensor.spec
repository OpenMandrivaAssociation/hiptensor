# Tensor contractions for HIP. TheRock 10.2.

# Fat HIP device instances. -flto plus ninja -j32 SIGKILL'd clang
# (znver1 680715, x86_64 680716). Each unit compiles every GPU target.
# 8 jobs on the full list was SIGKILL'd at 116/333 (x86_64 702866 on
# c64-5). That builder's rpmbuild_timeout is 36000s, not 200000s.
# hipTensor upstream does not support gfx803, gfx906, or gfx1030.
# aarch64 builds the RDNA3/4 set at 8 jobs: 32 jobs times 4 arches is
# more concurrent device compiles than the x86 OOM. x86 also keeps
# CDNA gfx908/gfx90a/gfx942.
%define _disable_lto 1
%ifarch aarch64
%global ht_ninja_jobs 8
%global ht_gpu_targets gfx1100;gfx1101;gfx1200;gfx1201
%else
%global ht_ninja_jobs 8
%global ht_gpu_targets gfx908;gfx90a;gfx942;gfx1100;gfx1101;gfx1102;gfx1200;gfx1201
%endif

Name:		hiptensor
Version:	10.2.0
Release:	1
Summary:	HIP tensor contraction library
License:	MIT
Group:		System/Libraries
URL:		https://github.com/ROCm/rocm-libraries
Source0:	https://github.com/ROCm/rocm-libraries/releases/download/therock-10.2/hiptensor.tar.gz#/hiptensor-%{version}.tar.gz

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
# ph300 filled its root while packing another ROCm library. The ninja
# objects are not needed once the files are in the buildroot.
rm -rf build

%files
%license LICENSE
%doc README.md
# cmake installs a second copy. %license already owns LICENSE.
%exclude %{_docdir}/hiptensor/LICENSE
%{_libdir}/libhiptensor.so.*

%files devel
%{_includedir}/hiptensor/
%{_libdir}/libhiptensor.so
%{_libdir}/cmake/hiptensor/
