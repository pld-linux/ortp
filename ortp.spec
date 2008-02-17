Summary:	RTP/RTCP protocol library
Summary(pl.UTF-8):	Biblioteka obsługująca protokół RTP/RTCP
Name:		ortp
Version:	0.13.1
Release:	1
License:	LGPL v2.1+
Group:		Libraries
Source0:	http://download.savannah.nongnu.org/releases/linphone/ortp/sources/%{name}-%{version}.tar.gz
# Source0-md5:	293f16da6dd434e68652f0f725b7f97c
Patch0:		%{name}-i486.patch
URL:		http://www.linphone.org/index.php/eng/code_review/ortp
BuildRequires:	autoconf >= 2.50
BuildRequires:	automake
BuildRequires:	libtool
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%define		specflags	-fno-strict-aliasing

%description
ortp is a library for handling RTP/RTCP packets. (See RFC 1889 and
1890 for more information about the protocol)

%description -l pl.UTF-8
ortp to biblioteka obsługująca pakiety RTP/RTCP. Więcej informacji o
protokole znajduje się w RFC 1889 i 1890.

%package devel
Summary:	Header files to develop applications using ortp
Summary(pl.UTF-8):	Pliki nagłówkowe do tworzenia aplikacji używających ortp
Group:		Development/Libraries
Requires:	%{name} = %{version}-%{release}

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

%build
%{__libtoolize}
%{__aclocal}
%{__autoconf}
%{__automake}
%configure \
%if "%{_lib}" == "lib64"
	--enable-mode64bit=yes \
%else
	--enable-mode64bit=no \
%endif
	--enable-ipv6
%{__make}

%install
rm -rf $RPM_BUILD_ROOT

%{__make} install \
	DESTDIR=$RPM_BUILD_ROOT

rm -r $RPM_BUILD_ROOT%{_datadir}/doc/ortp/html

%clean
rm -fr $RPM_BUILD_ROOT

%post	-p /sbin/ldconfig
%postun	-p /sbin/ldconfig

%files
%defattr(644,root,root,755)
%doc README NEWS AUTHORS ChangeLog doc/html
%attr(755,root,root) %{_libdir}/libortp.so.*.*.*
%attr(755,root,root) %ghost %{_libdir}/libortp.so.5

%files devel
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/libortp.so
%{_libdir}/libortp.la
%{_includedir}/ortp
%{_pkgconfigdir}/ortp.pc

%files static
%defattr(644,root,root,755)
%{_libdir}/libortp.a
