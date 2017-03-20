# TODO:
# 	- package the 'backfire' kernel module properly

Summary:	Programs that test various rt-linux features
Name:		rt-tests
Version:	1.0
Release:	1
License:	GPL v2
Group:		Applications
Source0:	https://www.kernel.org/pub/linux/utils/rt-tests/%{name}-%{version}.tar.xz
# Source0-md5:	3818d2d0a3069291864bf85fde40883b
URL:		https://rt.wiki.kernel.org/index.php/Cyclictest
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
Programs that test various rt-linux features.

%prep
%setup -q

%build
%{__make} \
	prefix="%{_prefix}" \
	CC="%{__cc}" \
	CFLAGS="%{rpmcflags}" \
	LDFLAGS="%{rpmldflags}"

%install
rm -rf $RPM_BUILD_ROOT

%{__make} install \
	DESTDIR=$RPM_BUILD_ROOT \
	prefix="%{_prefix}" \
	PYLIB="%{py_sitescriptdir}" \
	srcdir="%{_prefix}/src/%{name}-%{version}"

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(644,root,root,755)
%doc README.markdown MAINTAINERS
%attr(755,root,root) %{_bindir}/cyclictest
%attr(755,root,root) %{_bindir}/hackbench
%attr(755,root,root) %{_bindir}/hwlatdetect
%attr(755,root,root) %{_bindir}/pi_stress
%attr(755,root,root) %{_bindir}/pip_stress
%attr(755,root,root) %{_bindir}/pmqtest
%attr(755,root,root) %{_bindir}/ptsematest
%attr(755,root,root) %{_bindir}/rt-migrate-test
%attr(755,root,root) %{_bindir}/sendme
%attr(755,root,root) %{_bindir}/signaltest
%attr(755,root,root) %{_bindir}/sigwaittest
%attr(755,root,root) %{_bindir}/svsematest
%{_mandir}/man4/backfire.4*
%{_mandir}/man8/cyclictest.8*
%{_mandir}/man8/hackbench.8*
%{_mandir}/man8/hwlatdetect.8*
%{_mandir}/man8/pi_stress.8*
%{_mandir}/man8/pmqtest.8*
%{_mandir}/man8/ptsematest.8*
%{_mandir}/man8/sendme.8*
%{_mandir}/man8/signaltest.8*
%{_mandir}/man8/sigwaittest.8*
%{_mandir}/man8/svsematest.8*
%{py_sitescriptdir}/hwlatdetect.py
%{_prefix}/src/%{name}-%{version}
