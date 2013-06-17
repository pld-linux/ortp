#
# Conditional build:
%bcond_without	zrtp	# ZRTP (RFC 6189: Media Path Key Agreement for Unicast Secure RTP) support; GPL v3
#
Summary:	RTP/RTCP protocol library
Summary(pl.UTF-8):	Biblioteka obsługująca protokół RTP/RTCP
Name:		ortp
Version:	0.22.0
Release:	1
%if %{with zrtp}
License:	GPL v3+
%else
License:	LGPL v2.1+
%endif
Group:		Libraries
Source0:	http://download.savannah.nongnu.org/releases/linphone/ortp/sources/%{name}-%{version}.tar.gz
# Source0-md5:	119357e1d904be0289e57c80e5ad90ba
Patch0:		%{name}-i486.patch
Patch1:		%{name}-libssl-not-required.patch
URL:		http://www.linphone.org/eng/documentation/dev/ortp.html
BuildRequires:	autoconf >= 2.50
BuildRequires:	automake
BuildRequires:	doxygen
BuildRequires:	libtool >= 2:2.0
%{?with_zrtp:BuildRequires:	libzrtpcpp-devel >= 2.0.0}
BuildRequires:	openssl-devel
BuildRequires:	srtp-devel
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
%{?with_zrtp:Requires:	libzrtpcpp-devel >= 2.0.0}
Requires:	openssl-devel
Requires:	srtp-devel

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

%prep
%setup -q
%patch0 -p1
%patch1 -p1

%build
%{__libtoolize}
%{__aclocal}
%{__autoconf}
%{__autoheader}
%{__automake}
%configure \
	--disable-silent-rules \
	--disable-strict \
	--enable-ipv6 \
%if "%{_lib}" == "lib64"
	--enable-mode64bit=yes \
%else
	--enable-mode64bit=no \
%endif
	--enable-static \
	%{?with_zrtp:--enable-zrtp}

%{__make}

%install
rm -rf $RPM_BUILD_ROOT

%{__make} install \
	DESTDIR=$RPM_BUILD_ROOT

%{__rm} -r $RPM_BUILD_ROOT%{_docdir}/%{name}-%{version}

%clean
rm -rf $RPM_BUILD_ROOT

%post	-p /sbin/ldconfig
%postun	-p /sbin/ldconfig

%files
%defattr(644,root,root,755)
%doc AUTHORS ChangeLog NEWS README TODO doc/html
%attr(755,root,root) %{_libdir}/libortp.so.*.*.*
%attr(755,root,root) %ghost %{_libdir}/libortp.so.9

%files devel
%defattr(644,root,root,755)
%doc doc/html/*
%attr(755,root,root) %{_libdir}/libortp.so
%{_libdir}/libortp.la
%{_includedir}/ortp
%{_pkgconfigdir}/ortp.pc

%files static
%defattr(644,root,root,755)
%{_libdir}/libortp.a
