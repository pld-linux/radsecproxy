####
# TODO:
# - docbook2x is required for manual build
Summary:	RADIUS proxy that in addition to to usual RADIUS UDP transport, also supports TLS (RadSec)
Name:		radsecproxy
Version:	1.4
Release:	2
License:	GPLv2+ or BSD-like
Group:		Networking/Daemons/Radius
Source0:	http://software.uninett.no/radsecproxy/%{name}-%{version}.tar.gz
# Source0-md5:	7b5248b2a7a133561cf685730824c893
Source1:	%{name}.init
Source2:	%{name}.logrotate
Source3:	%{name}.upstart
URL:		http://software.uninett.no/radsecproxy/
#For manual creation:
#BuildRequires:	docbook2x-to-man
BuildRequires:	openssl-devel
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
radsecproxy is a generic RADIUS proxy that in addition to to usual
RADIUS UDP transport, also supports TLS (RadSec). The aim is for the
proxy to have sufficient features to be flexible, while at the same
time to be small, efficient and easy to configure. Currently the
executable on Linux is only about 48 Kb, and it uses about 64 Kb
(depending on the number of peers) while running.

%package upstart
Summary:	Upstart job description for %{name}
Summary(pl.UTF-8):	Opis zadania Upstart dla %{name}
Group:		Daemons
Requires:	%{name} = %{version}-%{release}
Requires:	upstart >= 0.6

%description upstart
Upstart job description for %{name}.

%description upstart -l pl.UTF-8
Opis zadania Upstart dla %{name}.

%prep
%setup -q

%build
%configure
%{__make}

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT%{_sysconfdir}/radsecproxy.conf.d \
	$RPM_BUILD_ROOT/etc/{rc.d/init.d,sysconfig,logrotate.d,init}

%{__make} install \
	DESTDIR=$RPM_BUILD_ROOT

install radsecproxy.conf-example $RPM_BUILD_ROOT%{_sysconfdir}/%{name}.conf

install %{SOURCE1} $RPM_BUILD_ROOT/etc/rc.d/init.d/%{name}
install %{SOURCE2} $RPM_BUILD_ROOT/etc/logrotate.d/%{name}
install %{SOURCE3} $RPM_BUILD_ROOT/etc/init/%{name}.conf

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

%post upstart
%upstart_post %{name}

%postun upstart
%upstart_postun %{name}

%files
%defattr(644,root,root,755)
%doc AUTHORS ChangeLog README
%attr(640,root,root) %config(noreplace,missingok) %verify(not md5 mtime size) %{_sysconfdir}/radsecproxy.conf
%attr(640,root,root) %config(noreplace,missingok) %verify(not md5 mtime size) /etc/logrotate.d/%{name}
%attr(750,root,root) %dir %{_sysconfdir}/radsecproxy.conf.d
%attr(755,root,root) %{_sbindir}/radsecproxy
%attr(755,root,root) %{_bindir}/catgconf
%attr(754,root,root) /etc/rc.d/init.d/%{name}
%{_mandir}/man1/*
# With manual created:
#%{_mandir}/man5/*

%files upstart
%defattr(644,root,root,755)
%config(noreplace) %verify(not md5 mtime size) /etc/init/%{name}.conf
