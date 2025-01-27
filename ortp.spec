#
# Conditional build:
%bcond_without	static_libs	# static library
#
Summary:	RTP/RTCP protocol library
Summary(pl.UTF-8):	Biblioteka obsługująca protokół RTP/RTCP
Name:		ortp
Version:	5.3.104
Release:	1
License:	AGPL v3+
Group:		Libraries
#Source0Download: https://gitlab.linphone.org/BC/public/ortp/tags
Source0:	https://gitlab.linphone.org/BC/public/ortp/-/archive/%{version}/%{name}-%{version}.tar.bz2
# Source0-md5:	cfed5cb02b559827dc67b2bddfa0c7e9
Patch1:		%{name}-pc.patch
URL:		https://www.linphone.org/technical-corner/mediastreamer2-ortp
BuildRequires:	bctoolbox-devel >= 5.3.0
BuildRequires:	cmake >= 3.22
BuildRequires:	doxygen
BuildRequires:	libstdc++-devel >= 6:7
BuildRequires:	openssl-devel
BuildRequires:	pkgconfig
BuildRequires:	rpm-build >= 4.6
BuildRequires:	rpmbuild(macros) >= 1.605
Requires:	bctoolbox >= 5.3.0
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
Requires:	bctoolbox-devel >= 5.3.0
Requires:	libstdc++-devel >= 6:7
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
BuildArch:	noarch

%description apidocs
API documentation for ortp library.

%description apidocs -l pl.UTF-8
Dokumentacja API biblioteki ortp.

%prep
%setup -q
%patch -P 1 -p1

%build
# use cmake instead of autotools:
# - to get cmake target files for other linphone projects
# - configure.ac seems outdated (version 1.0.1, soname 13)
%if %{with static_libs}
%cmake -B builddir-static \
	-DBUILD_SHARED_LIBS=OFF \
	-DENABLE_DOC=OFF \
	-DENABLE_STRICT=OFF \
	-DENABLE_UNIT_TESTS=OFF

%{__make} -C builddir-static
%endif

%cmake -B builddir \
	-DENABLE_STRICT=OFF

%{__make} -C builddir

%install
rm -rf $RPM_BUILD_ROOT

%if %{with static_libs}
%{__make} -C builddir-static install \
	DESTDIR=$RPM_BUILD_ROOT
%endif

%{__make} -C builddir install \
	DESTDIR=$RPM_BUILD_ROOT

# packaged as %doc
%{__rm} -r $RPM_BUILD_ROOT%{_docdir}/ortp-5.3.0

%clean
rm -rf $RPM_BUILD_ROOT

%post	-p /sbin/ldconfig
%postun	-p /sbin/ldconfig

%files
%defattr(644,root,root,755)
%doc AUTHORS.md CHANGELOG.md README.md
%attr(755,root,root) %{_libdir}/libortp.so.15

%files devel
%defattr(644,root,root,755)
%attr(755,root,root) %{_bindir}/ortp-tester
%attr(755,root,root) %{_libdir}/libortp.so
%{_includedir}/ortp
%{_datadir}/ortp-tester
%{_pkgconfigdir}/ortp.pc
%dir %{_datadir}/Ortp
%{_datadir}/Ortp/cmake

%if %{with static_libs}
%files static
%defattr(644,root,root,755)
%{_libdir}/libortp.a
%endif

%files apidocs
%defattr(644,root,root,755)
%doc builddir/doc/html/*.{css,html,js,png}
