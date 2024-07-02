# TODO:
# - own UID/GID
Summary:	RADIUS proxy that in addition to to usual RADIUS UDP transport, also supports TLS (RadSec)
Summary(pl.UTF-8):	Proxy RADIUS, poza zwyczajowym transportem UDP, obsługujące także TLS (RadSec)
Name:		radsecproxy
Version:	1.10.1
Release:	1
License:	BSD
Group:		Networking/Daemons/Radius
#Source0Download: https://github.com/radsecproxy/radsecproxy/releases
Source0:	https://github.com/radsecproxy/radsecproxy/releases/download/%{version}/%{name}-%{version}.tar.gz
# Source0-md5:	df7b4115361505fa0089d054673d0c70
Source1:	%{name}.init
Source2:	%{name}.logrotate
URL:		https://github.com/radsecproxy/radsecproxy
BuildRequires:	autoconf >= 2.50
BuildRequires:	automake
BuildRequires:	nettle-devel
Requires(post,preun):	/sbin/chkconfig
Requires:	openssl >= 1.0.0b
Requires:	rc-scripts >= 0.4.3.0
Obsoletes:	radsecproxy-upstart
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
radsecproxy is a generic RADIUS proxy that in addition to to usual
RADIUS UDP transport, also supports TLS (RadSec). The aim is for the
proxy to have sufficient features to be flexible, while at the same
time to be small, efficient and easy to configure. Currently the
executable on Linux is only about 48 kB, and it uses about 64 kB
(depending on the number of peers) while running.

%description -l pl.UTF-8
radsecproxy to ogólne proxy RADIUS, które, poza zwyczajowym
transportem UDP RADIUS, obsługuje także TLS (RadSec). Celem projektu
jest dostarczenie wystarczająco dużej funkcjonalności, aby było
elastyczne, a jednocześnie małe, wydajne i łatwe do skonfigurowania.
Obecnie rozmiar binarki pod Linuksem to tylko około 48 kB, a w czasie
działania zużywa około 64 kB (w zależności od liczby partnerów).

%prep
%setup -q

%build
%{__aclocal}
%{__autoconf}
%{__automake}
%configure

%{__make}

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT%{_sysconfdir}/radsecproxy.conf.d \
	$RPM_BUILD_ROOT/etc/{rc.d/init.d,sysconfig,logrotate.d,init}

%{__make} install \
	DESTDIR=$RPM_BUILD_ROOT

cp -p radsecproxy.conf-example $RPM_BUILD_ROOT%{_sysconfdir}/%{name}.conf

install -p %{SOURCE1} $RPM_BUILD_ROOT/etc/rc.d/init.d/%{name}
cp -p %{SOURCE2} $RPM_BUILD_ROOT/etc/logrotate.d/%{name}

install -p radsecproxy.conf.5 $RPM_BUILD_ROOT/%{_mandir}/man5

%clean
rm -rf $RPM_BUILD_ROOT

%post
/sbin/chkconfig --add %{name}
%service %{name} restart "RADIUS secure proxy"

%preun
if [ "$1" = "0" ]; then
	%service %{name} stop
	/sbin/chkconfig --del %{name}
fi

%files
%defattr(644,root,root,755)
%doc AUTHORS ChangeLog LICENSE README THANKS
%attr(640,root,root) %config(noreplace,missingok) %verify(not md5 mtime size) %{_sysconfdir}/radsecproxy.conf
%attr(640,root,root) %config(noreplace,missingok) %verify(not md5 mtime size) /etc/logrotate.d/%{name}
%attr(750,root,root) %dir %{_sysconfdir}/radsecproxy.conf.d
%attr(755,root,root) %{_sbindir}/radsecproxy
%attr(755,root,root) %{_bindir}/radsecproxy-conf
%attr(755,root,root) %{_bindir}/radsecproxy-hash
%attr(754,root,root) /etc/rc.d/init.d/%{name}
%{_mandir}/man5/radsecproxy.conf.5*
%{_mandir}/man8/radsecproxy.8*
%{_mandir}/man8/radsecproxy-hash.8*
