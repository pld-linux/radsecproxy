Summary:	RADIUS proxy that in addition to to usual RADIUS UDP transport, also supports TLS (RadSec)
Name:		radsecproxy
Version:	1.1
Release:	0.9
License:	Artistic License
######		Unknown group!
Group:		Productivity/Networking/Radius/Clients
Source0:	http://software.uninett.no/radsecproxy/%{name}-%{version}.tar.gz
# Source0-md5:	f7d0eaf1e9d963557affc90e61c0d1ae
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
%{__make} install \
	DESTDIR=$RPM_BUILD_ROOT

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(644,root,root,755)
%doc COPYING NEWS INSTALL AUTHORS ChangeLog
#%config(noreplace) %{_sysconfdir}/radsecproxy.conf
%attr(755,root,root) %{_sbindir}/radsecproxy
%{_mandir}/man1/*
%{_mandir}/man5/*
%{_sysconfdir}/radsecproxy.conf-example
