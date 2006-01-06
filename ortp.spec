# TODO:
# 	- fix gtk-doc
Summary:	RTP/RTCP protocol library
Summary(pl):	Biblioteka obs³uguj±ca protokó³ RTP/RTCP
Name:		ortp
Version:	0.8.1
Release:	1
License:	LGPL
Group:		Libraries
Source0:	http://www.linphone.org/ortp/sources/%{name}-%{version}.tar.gz
# Source0-md5:	5d8a8da638aec3a80214d64e0c7929af
URL:		http://www.linphone.org/ortp/
BuildRequires:	autoconf
BuildRequires:	automake
BuildRequires:	glib2-devel >= 2.0.0
BuildRequires:	gtk-doc
BuildRequires:	libtool
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
ortp is a library for handling RTP/RTCP packets. (See RFC 1889 and
1890 for more information about the protocol)

%description -l pl
ortp to biblioteka obs³uguj±ca pakiety RTP/RTCP. Wiêcej informacji o
protokole znajduje siê w RFC 1889 i 1890.

%package devel
Summary:	Header files to develop applications using ortp
Summary(pl):	Pliki nag³ówkowe do tworzenia aplikacji u¿ywaj±cych ortp
Group:		Development/Libraries
Requires:	%{name} = %{version}-%{release}

%description devel
Header files for the ortp library.

%description devel -l pl
Pliki nag³ówkowe dla biblioteki ortp.

%package static
Summary:	Static ortp library
Summary(pl):	Statyczna biblioteka ortp
Group:		Development/Libraries
Requires:	%{name}-devel = %{version}-%{release}

%description static
Static ortp library.

%description static -l pl
Statyczna biblioteka ortp.

%prep
%setup -q

%build
%{__libtoolize}
%{__aclocal}
%{__autoconf}
%{__automake}
%configure \
	--disable-gtk-doc \
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
