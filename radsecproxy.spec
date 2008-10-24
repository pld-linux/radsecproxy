# TODO:
# - own UID/GID
Summary:	RADIUS proxy that in addition to to usual RADIUS UDP transport, also supports TLS (RadSec)
Name:		radsecproxy
Version:	1.2
Release:	0.3
License:	GPLv2+ or BSD-like
Group:		Networking/Daemons/Radius
Source0:	http://software.uninett.no/radsecproxy/%{name}-%{version}.tar.gz
# Source0-md5:	e209054731b3316301d0920c15a0a5b2
Source1:	%{name}.init
URL:		http://software.uninett.no/radsecproxy/
BuildRequires:	openssl-devel
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
radsecproxy is a generic RADIUS proxy that in addition to to usual
RADIUS UDP transport, also supports TLS (RadSec). The aim is for the
proxy to have sufficient features to be flexible, while at the same
time to be small, efficient and easy to configure. Currently the
executable on Linux is only about 48 Kb, and it uses about 64 Kb
(depending on the number of peers) while running.

%prep
%setup -q

%build
%configure \
	--enable-shadow \
	--with-secure-path \

%{__make}

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT%{_sysconfdir}/radsecproxy.conf.d \
	$RPM_BUILD_ROOT/etc/{rc.d/init.d,sysconfig}

%{__make} install \
	DESTDIR=$RPM_BUILD_ROOT

mv $RPM_BUILD_ROOT%{_sysconfdir}/radsecproxy.conf-example \
	$RPM_BUILD_ROOT%{_sysconfdir}/radsecproxy.conf

install %{SOURCE1} $RPM_BUILD_ROOT/etc/rc.d/init.d/%{name}

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
%doc AUTHORS ChangeLog README
%attr(640,root,root) %config(noreplace,missingok) %verify(not md5 mtime size) %{_sysconfdir}/radsecproxy.conf
%attr(750,root,root) %dir %{_sysconfdir}/radsecproxy.conf.d
%attr(755,root,root) %{_sbindir}/radsecproxy
%attr(754,root,root) /etc/rc.d/init.d/%{name}
%{_mandir}/man1/*
%{_mandir}/man5/*
