#
# Conditional build:
%bcond_without	kernel		# backfire kernel module
%bcond_without	userspace	# userspace programs
%bcond_with	verbose		# verbose kernel module build (V=1)

%if 0%{?_pld_builder:1} && %{with kernel} && %{with userspace}
%{error:kernel and userspace cannot be built at the same time on PLD builders}
exit 1
%endif

%if %{without userspace}
%define		_enable_debug_packages	0
%endif

Summary:	Programs that test various rt-linux features
Summary(pl.UTF-8):	Programy testujące różne właściwości rt-linuksa
%define	pname	rt-tests
Name:		%{pname}%{?_pld_builder:%{?with_kernel:-kernel}}%{_alt_kernel}
Version:	1.4
%define	rel	1
Release:	%{rel}%{?_pld_builder:%{?with_kernel:@%{_kernel_ver_str}}}
License:	GPL v2
Group:		Applications/System
Source0:	https://www.kernel.org/pub/linux/utils/rt-tests/%{pname}-%{version}.tar.xz
# Source0-md5:	e056b5cd0e8f327bf1c9ecd3517f6815
# https://bugs.launchpad.net/ubuntu/+source/rt-tests/+bug/881771/+attachment/2572753/+files/0001-Fix-deprecated-removed-spinlock-declaration.patch
# + http://www.spinics.net/lists/linux-rt-users/msg08966.html
Patch0:		%{pname}-backfire.patch
URL:		https://rt.wiki.kernel.org/index.php/Cyclictest
%{?with_kernel:%{expand:%buildrequires_kernel kernel%%{_alt_kernel}-module-build >= 3:2.6.20.2}}
%ifarch %{ix86} %{x8664} x32 ia64 mipx ppc
BuildRequires:	numactl-devel
%endif
BuildRequires:	python-modules
BuildRequires:	rpmbuild(macros) >= 1.701
BuildRequires:	tar >= 1:1.22
BuildRequires:	xz
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
Programs that test various rt-linux features.

%description -l pl.UTF-8
Programy testujące różne właściwości rt-linuksa.

%define	kernel_pkg()\
%package -n kernel%{_alt_kernel}-char-backfire\
Summary:	Linux kernel module to benchmark signal delivery\
Summary(pl.UTF-8):	Moduł jądra Linuksa do testowania dostarczania sygnałów\
Release:	%{rel}@%{_kernel_ver_str}\
Group:		Base/Kernel\
Requires(post,postun):	/sbin/depmod\
%requires_releq_kernel\
Requires(postun):	%releq_kernel\
\
%description -n kernel%{_alt_kernel}-char-backfire\
Linux kernel "backfire" module sends a signal from driver to user.\
It's primary use is benchmarking signal delivery.\
\
%description -n kernel%{_alt_kernel}-char-backfire -l pl.UTF-8\
Moduł jądra Linuksa "backfire" wysyła sygnał ze sterownika do\
użytkownika. Głównym zastosowaniem jest testowanie wydajności\
dostarczania sygnałów.\
\
%if %{with kernel}\
%files -n kernel%{_alt_kernel}-char-backfire\
%defattr(644,root,root,755)\
/lib/modules/%{_kernel_ver}/kernel/drivers/char/backfire.ko*\
%endif\
\
%post	-n kernel%{_alt_kernel}-char-backfire\
%depmod %{_kernel_ver}\
\
%postun	-n kernel%{_alt_kernel}-char-backfire\
%depmod %{_kernel_ver}\
%{nil}

%define build_kernel_pkg()\
%build_kernel_modules -C src/backfire -m backfire\
\
%install_kernel_modules -D installed -m src/backfire/backfire -d kernel/drivers/char\
%{nil}

%{?with_kernel:%{expand:%create_kernel_packages}}

%prep
%setup -q -n %{pname}-%{version}
%patch0 -p1

%build
%if %{with userspace}
CFLAGS="%{rpmcflags}" \
%{__make} \
	prefix="%{_prefix}" \
	CC="%{__cc}" \
	LDFLAGS="%{rpmldflags}"
%endif

%{?with_kernel:%{expand:%build_kernel_packages}}

%install
rm -rf $RPM_BUILD_ROOT

%if %{with userspace}
%{__make} install \
	DESTDIR=$RPM_BUILD_ROOT \
	prefix="%{_prefix}" \
	PYLIB="%{py_sitescriptdir}" \
	srcdir="%{_prefix}/src/%{name}-%{version}"

%py_comp $RPM_BUILD_ROOT%{py_sitescriptdir}
%py_ocomp $RPM_BUILD_ROOT%{py_sitescriptdir}
%endif

%if %{with kernel}
cp -a installed/* $RPM_BUILD_ROOT
%endif

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(644,root,root,755)
%doc README.markdown MAINTAINERS
%attr(755,root,root) %{_bindir}/cyclicdeadline
%attr(755,root,root) %{_bindir}/cyclictest
%attr(755,root,root) %{_bindir}/deadline_test
%attr(755,root,root) %{_bindir}/determine_maximum_mpps.sh
%attr(755,root,root) %{_bindir}/get_cpuinfo_mhz.sh
%attr(755,root,root) %{_bindir}/hackbench
%attr(755,root,root) %{_bindir}/hwlatdetect
%attr(755,root,root) %{_bindir}/pi_stress
%attr(755,root,root) %{_bindir}/pip_stress
%attr(755,root,root) %{_bindir}/pmqtest
%attr(755,root,root) %{_bindir}/ptsematest
%attr(755,root,root) %{_bindir}/queuelat
%attr(755,root,root) %{_bindir}/rt-migrate-test
%attr(755,root,root) %{_bindir}/signaltest
%attr(755,root,root) %{_bindir}/sigwaittest
%attr(755,root,root) %{_bindir}/ssdd
%attr(755,root,root) %{_bindir}/svsematest
%{_mandir}/man8/cyclictest.8*
%{_mandir}/man8/deadline_test.8*
%{_mandir}/man8/hackbench.8*
%{_mandir}/man8/hwlatdetect.8*
%{_mandir}/man8/pi_stress.8*
%{_mandir}/man8/pip_stress.8*
%{_mandir}/man8/pmqtest.8*
%{_mandir}/man8/ptsematest.8*
%{_mandir}/man8/queuelat.8*
%{_mandir}/man8/rt-migrate-test.8*
%{_mandir}/man8/signaltest.8*
%{_mandir}/man8/sigwaittest.8*
%{_mandir}/man8/ssdd.8*
%{_mandir}/man8/svsematest.8*
%{py_sitescriptdir}/hwlatdetect.py*
%{_prefix}/src/%{name}-%{version}
