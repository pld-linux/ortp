#
# Conditional build:
%bcond_without	static_libs	# Static library
#
Summary:	RTP/RTCP protocol library
Summary(pl.UTF-8):	Biblioteka obsługująca protokół RTP/RTCP
Name:		ortp
Version:	1.0.2
Release:	1
License:	LGPL v2.1+
Group:		Libraries
Source0:	https://linphone.org/releases/sources/ortp/%{name}-%{version}.tar.gz
# Source0-md5:	82629e99befa578341e0bdc225924135
URL:		http://www.linphone.org/eng/documentation/dev/ortp.html
BuildRequires:	autoconf >= 2.50
BuildRequires:	automake
BuildRequires:	bctoolbox-devel
BuildRequires:	doxygen
BuildRequires:	libtool >= 2:2.0
BuildRequires:	openssl-devel
BuildRequires:	pkgconfig
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%define		specflags	-fno-strict-aliasing

%description
ortp is a library for handling RTP protocol (RFC 3550).

%description -l pl.UTF-8
ortp to biblioteka obsługująca protokół RTP (RFC 3550).

%package devel
Summary:	Header files to develop applications using ortp
Summary(pl.UTF-8):	Pliki nagłówkowe do tworzenia aplikacji używających ortp
Group:		Development/Libraries
Requires:	%{name} = %{version}-%{release}
Requires:	openssl-devel

%description devel
Header files for the ortp library.

%description devel -l pl.UTF-8
Pliki nagłówkowe dla biblioteki ortp.

%package static
Summary:	Static ortp library
Summary(pl.UTF-8):	Statyczna biblioteka ortp
Group:		Development/Libraries
Requires:	%{name}-devel = %{version}-%{release}

%description static
Static ortp library.

%description static -l pl.UTF-8
Statyczna biblioteka ortp.

%package apidocs
Summary:	API documentation for ortp library
Summary(pl.UTF-8):	Dokumentacja API biblioteki ortp
Group:		Documentation
%if "%{_rpmversion}" >= "5"
BuildArch:	noarch
%endif

%description apidocs
API documentation for ortp library.

%description apidocs -l pl.UTF-8
Dokumentacja API biblioteki ortp.

%prep
%setup -q -n %{name}-%{version}-0

%build
%{__libtoolize}
%{__aclocal} -I m4
%{__autoconf}
%{__autoheader}
%{__automake}
%configure \
	--disable-silent-rules \
	--disable-strict \
%if "%{_lib}" == "lib64"
	--enable-mode64bit=yes \
%else
	--enable-mode64bit=no \
%endif
	--enable-ssl-hmac \
	%{?with_static_libs:--enable-static}

%{__make}

%install
rm -rf $RPM_BUILD_ROOT

%{__make} install \
	DESTDIR=$RPM_BUILD_ROOT

# packaged as %doc
%{__rm} -r $RPM_BUILD_ROOT%{_docdir}/ortp-1.0.1

%clean
rm -rf $RPM_BUILD_ROOT

%post	-p /sbin/ldconfig
%postun	-p /sbin/ldconfig

%files
%defattr(644,root,root,755)
%doc AUTHORS ChangeLog NEWS README.md
%attr(755,root,root) %{_libdir}/libortp.so.*.*.*
%attr(755,root,root) %ghost %{_libdir}/libortp.so.13

%files devel
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/libortp.so
%{_libdir}/libortp.la
%{_includedir}/ortp
%{_pkgconfigdir}/ortp.pc

%if %{with static_libs}
%files static
%defattr(644,root,root,755)
%{_libdir}/libortp.a
%endif

%files apidocs
%defattr(644,root,root,755)
%doc doc/html/*
