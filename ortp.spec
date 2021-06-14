#
# Conditional build:
%bcond_without	static_libs	# Static library
#
Summary:	RTP/RTCP protocol library
Summary(pl.UTF-8):	Biblioteka obsługująca protokół RTP/RTCP
Name:		ortp
Version:	4.5.15
Release:	1
License:	GPL v3+
Group:		Libraries
#Source0Download: https://gitlab.linphone.org/BC/public/ortp/tags
Source0:	https://gitlab.linphone.org/BC/public/ortp/-/archive/%{version}/%{name}-%{version}.tar.bz2
# Source0-md5:	e03716372f79b5fdcd1c5e9c3918fcde
Patch0:		%{name}-am.patch
Patch1:		%{name}-pc.patch
URL:		http://www.linphone.org/technical-corner/ortp
BuildRequires:	bctoolbox-devel >= 0.2.0
BuildRequires:	cmake >= 3.1
BuildRequires:	doxygen
BuildRequires:	libstdc++-devel
BuildRequires:	openssl-devel
BuildRequires:	pkgconfig
BuildRequires:	rpm-build >= 4.6
BuildRequires:	rpmbuild(macros) >= 1.605
Requires:	bctoolbox >= 0.2.0
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
Requires:	bctoolbox-devel >= 0.2.0
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
BuildArch:	noarch

%description apidocs
API documentation for ortp library.

%description apidocs -l pl.UTF-8
Dokumentacja API biblioteki ortp.

%prep
%setup -q
%patch0 -p1
%patch1 -p1

%build
# use cmake instead of autotools:
# - to get cmake target files for other linphone projects
# - configure.ac seems outdated (version 1.0.1, soname 13)
install -d build
cd build
%cmake .. \
	%{!?with_static_libs:-DENABLE_STATIC=NO} \
	-DENABLE_STRICT=NO
%{__make}

%install
rm -rf $RPM_BUILD_ROOT

%{__make} -C build install \
	DESTDIR=$RPM_BUILD_ROOT

# packaged as %doc
%{__rm} -r $RPM_BUILD_ROOT%{_docdir}/ortp-.
# packaged as %doc in -apidocs
%{__rm} -r $RPM_BUILD_ROOT%{_docdir}/ortp-4.5.0

# disable completeness check incompatible with split packaging
%{__sed} -i -e '/^foreach(target .*IMPORT_CHECK_TARGETS/,/^endforeach/d; /^unset(_IMPORT_CHECK_TARGETS)/d' $RPM_BUILD_ROOT%{_libdir}/cmake/ortp/ortpTargets.cmake

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
%attr(755,root,root) %{_libdir}/libortp.so
%{_includedir}/ortp
%{_pkgconfigdir}/ortp.pc
%{_libdir}/cmake/ortp

%if %{with static_libs}
%files static
%defattr(644,root,root,755)
%{_libdir}/libortp.a
%endif

%files apidocs
%defattr(644,root,root,755)
%doc build/doc/html/*.{css,html,js,png}
