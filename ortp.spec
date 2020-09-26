#
# Conditional build:
%bcond_without	static_libs	# Static library
#
Summary:	RTP/RTCP protocol library
Summary(pl.UTF-8):	Biblioteka obsługująca protokół RTP/RTCP
Name:		ortp
Version:	4.4.0
Release:	1
License:	GPL v3+
Group:		Libraries
#Source0Download: https://gitlab.linphone.org/BC/public/ortp/tags
Source0:	https://gitlab.linphone.org/BC/public/ortp/-/archive/%{version}/%{name}-%{version}.tar.bz2
# Source0-md5:	33df5f50a6ce40cc114c1393a30959b7
Patch0:		%{name}-am.patch
URL:		http://www.linphone.org/technical-corner/ortp
BuildRequires:	autoconf >= 2.50
BuildRequires:	automake
BuildRequires:	bctoolbox-devel
BuildRequires:	doxygen
BuildRequires:	libstdc++-devel
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
Requires:	libstdc++-devel
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
%if "%{_rpmversion}" >= "4.6"
BuildArch:	noarch
%endif

%description apidocs
API documentation for ortp library.

%description apidocs -l pl.UTF-8
Dokumentacja API biblioteki ortp.

%prep
%setup -q
%patch0 -p1

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

# obsoleted by pkg-config
%{__rm} $RPM_BUILD_ROOT%{_libdir}/libortp.la

# packaged as %doc
%{__rm} -r $RPM_BUILD_ROOT%{_docdir}/ortp-1.0.1

%clean
rm -rf $RPM_BUILD_ROOT

%post	-p /sbin/ldconfig
%postun	-p /sbin/ldconfig

%files
%defattr(644,root,root,755)
%doc AUTHORS.md CHANGELOG.md README.md
%attr(755,root,root) %{_libdir}/libortp.so.*.*.*
%attr(755,root,root) %ghost %{_libdir}/libortp.so.13

%files devel
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/libortp.so
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
