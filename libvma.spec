Name:               libvma
Version:            9.8.1
Release:            1
Summary:            A library that boosts performance for message-based and streaming applications
License:            GPLv2 or BSD
URL:                https://github.com/Mellanox/libvma
Source:             https://github.com/Mellanox/libvma/archive/%{version}.tar.gz
Patch0000:          add-loongarch64-support-for-libvma.patch

ExcludeArch:        %{arm}
Requires:           pam
Requires(post):     /sbin/ldconfig
Requires(postun):   /sbin/ldconfig
BuildRequires:      rdma-core-devel libnl3-devel automake autoconf libtool g++
Provides:           %{name}-utils = %{version}-%{release}
Obsoletes:          %{name}-utils < %{version}-%{release}

%description
Mellanox's Messaging Accelerator (VMA) is dynamically linked user space Linux
library for transparently enhancing the performance of networking-heavy
applications. It boosts performance for message-based and streaming applications
such as those found in financial services market data environments and Web2.0
clusters.

%package            devel
Summary:            Header files for libvma
Requires:           %{name} = %{version}-%{release}

%description        devel
Headers files for libvma.

%package_help

%prep
%autosetup -n %{name}-%{version} -p1

%build
./autogen.sh
%configure
%make_build V=1

%install
%{make_install}

find $RPM_BUILD_ROOT%{_libdir} -name '*.la' -delete
install -D -m 644 contrib/scripts/vma.service $RPM_BUILD_ROOT/%{_prefix}/lib/systemd/system/vma.service
rm -f $RPM_BUILD_ROOT/%{_sysconfdir}/init.d/vma

%post
%systemd_post vma.service

%preun
%systemd_preun vma.service

%postun
%systemd_postun_with_restart vma.service

%files
%defattr(-,root,root)
%doc README.md
%license LICENSE
%config(noreplace) %{_sysconfdir}/libvma.conf
%{_bindir}/vma_stats
%{_libdir}/%{name}.so
%{_libdir}/%{name}*.so.*
%{_sbindir}/vmad
%{_unitdir}/vma.service
%{_mandir}/man7/vma.*
%{_mandir}/man8/vmad.*
%{_mandir}/man8/vma_stats.*

%files devel
%defattr(-,root,root)
%{_includedir}/*

%files help
%defattr(-,root,root)
%{_pkgdocdir}/README.md
%{_pkgdocdir}/README
%{_pkgdocdir}/CHANGES


%changelog
* Sat Jul 15 2023 wulei <wu_lei@hoperun.com> - 9.8.1-1
- Update to 9.8.1

* Mon Feb 6 2023 Wenlong Zhang <zhangwenlong@loongson.cn> - 8.9.4-13
- add loongarch64 support for libvma

* Tue Aug 10 2021 wangyue <wangyue92@huawei.com> - 8.9.4-12
- fix build error with glibc-2.34

* Tue Jun 08 2021 wulei <wulei80@huawei.com> - 8.9.4-11
- fixes failed: g++: No such file or directory

* Wed Mar 10 2021 maminjie <maminjie1@huawei.com> - 8.9.4-10
- Remove ExecReload that is not supported

* Thu Sep 3 2020 zhaowei<zhaowei23@huawei.com> - 8.9.4-9
-update source URL

* Thu May 21 2020 yanan li <liyanan032@huawei.com> - 8.9.4-8
- Slove the problem of pointer value misalignment caused by gcc 9.x enabling verification.

* Sun Jan 19 2020 lijin Yang <yanglijin@huawei.com> - 8.9.4-7
- Type: enhancement
- ID: NA
- SUG: NA
- DESC: update the tar package

* Tue Nov 26 2019 openEuler Buildteam <buildteam@openeuler.org> - 8.0.1-6
- Package init
