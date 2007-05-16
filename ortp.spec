# TODO:
# 	- fix gtk-doc
# - sparc fails:
#stun.c: In function `stunRand':
#stun.c:762: warning: implicit declaration of function `gethrtime'
#make[3]: *** [stun.lo] Error 1
Summary:	RTP/RTCP protocol library
Summary(pl.UTF-8):	Biblioteka obsługująca protokół RTP/RTCP
Name:		ortp
Version:	0.11.0
Release:	1
License:	LGPL
Group:		Libraries
Source0:	http://download.savannah.nongnu.org/releases/linphone/ortp/sources/%{name}-%{version}.tar.gz
# Source0-md5:	c2595b0caf99f922946fcb16e3250787
URL:		http://www.linphone.org/index.php/v2/code_review/ortp
BuildRequires:	autoconf
BuildRequires:	automake
BuildRequires:	glib2-devel >= 2.0.0
BuildRequires:	gtk-doc
BuildRequires:	libtool
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%define specflags -fno-strict-aliasing

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

%build
%{__libtoolize}
%{__aclocal}
%{__autoconf}
%{__automake}
%configure \
	--with-html-dir=%{_gtkdocdir}
%{__make}

%install
rm -rf $RPM_BUILD_ROOT

%{__make} install \
	DESTDIR=$RPM_BUILD_ROOT

%clean
rm -fr $RPM_BUILD_ROOT

%post	-p /sbin/ldconfig
%postun	-p /sbin/ldconfig

%files
%defattr(644,root,root,755)
%doc README NEWS AUTHORS ChangeLog
%attr(755,root,root) %{_libdir}/lib*.so.*.*

%files devel
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/lib*.so
%{_libdir}/*.la
%{_includedir}/ortp
%{_gtkdocdir}/ortp
%{_pkgconfigdir}/*

%files static
%defattr(644,root,root,755)
%{_libdir}/lib*.a
