%define debug_package %{nil}

Name:           libqhyccd
Version:        4.0.15
Release:        1
Summary:        QHY camera SDK
License:        expat
URL:            https://www.qhyccd.com/
Prefix:         %{_prefix}
Provides:       libqhyccd = %{version}-%{release}
Obsoletes:      libqhyccd < 4.0.15
Requires:       libusbx
Requires:       fxload
Requires:       libqhyccd-firmware = %{version}-%{release}
Source:         libqhyccd-%{version}.tar.gz
Patch0:         02-pkg-config.patch
Patch1:         03-remove-config.h.patch
Patch2:         04-tidy-includes.patch
Patch3:         05-compile-under-c.patch
Patch4:         06-remove-proto-varnames.patch
Patch5:         07-udev-fixup.patch

%description
libqhyccd is a user-space driver for QHY astronomy cameras.

%package        devel
Summary:        Development files for %{name}
Group:          Development/Libraries
Requires:       %{name}%{?_isa} = %{version}-%{release}
Provides:       libqhyccd-devel = %{version}-%{release}
Obsoletes:      libqhyccd-devel < 4.0.15

%description    devel
The %{name}-devel package contains libraries and header files for
developing applications that use %{name}.

%package        firmware
Summary:        Firmware files for %{name}
Provides:       libqhyccd-firmware = %{version}-%{release}
Obsoletes:      libqhyccd-firmware < 4.0.15
BuildArch:	noarch

%description    firmware
The %{name}-firmware package contains firmware files for QHY cameras

%prep
%setup -q
%patch0 -p0
%patch1 -p0
%patch2 -p0
%patch3 -p0
%patch4 -p0
%patch5 -p0

%build

sed -e "s!@LIBDIR@!%{_libdir}!g" -e "s!@VERSION@!%{version}!g" < \
    libqhyccd.pc.in > libqhyccd.pc

%install
mkdir -p %{buildroot}%{_libdir}/pkgconfig
mkdir -p %{buildroot}%{_includedir}
mkdir -p %{buildroot}%{_docdir}/%{name}-%{version}
mkdir -p %{buildroot}/sbin
mkdir -p %{buildroot}%{_udevrulesdir}
mkdir -p %{buildroot}/lib/firmware/qhy

case %{_arch} in
  i386)
    cp usr/local/lib/x86/libqhyccd*.so.%{version} %{buildroot}%{_libdir}
    cp usr/local/lib/x86/libqhyccd*.a %{buildroot}%{_libdir}
    cp sbin/x86/fxload %{buildroot}/sbin/qhyfxload
    ;;
  x86_64)
    cp usr/local/lib/x64/libqhyccd*.so.%{version} %{buildroot}%{_libdir}
    cp usr/local/lib/x64/libqhyccd*.a %{buildroot}%{_libdir}
    cp sbin/x64/fxload %{buildroot}/sbin/qhyfxload
    ;;
  *)
    echo "unknown target architecture %{_arch}"
    exit 1
    ;;
esac

ln -sf %{name}.so.%{version} %{buildroot}%{_libdir}/%{name}.so.4
cp usr/local/include/qhyccd*.h %{buildroot}%{_includedir}
cp *.pc %{buildroot}%{_libdir}/pkgconfig
cp usr/local/doc/* %{buildroot}%{_docdir}/%{name}-%{version}
cp -r usr/local/testapp %{buildroot}%{_docdir}/%{name}-%{version}
cp -r usr/local/cmake_modules %{buildroot}%{_docdir}/%{name}-%{version}
cp lib/udev/rules.d/85-qhyccd.rules %{buildroot}%{_udevrulesdir}
cp lib/firmware/qhy/* %{buildroot}/lib/firmware/qhy

%post
/sbin/ldconfig

%post firmware
/sbin/udevadm control --reload-rules

%postun
/sbin/ldconfig

%postun firmware
/sbin/udevadm control --reload-rules

%files
/sbin/qhyfxload
%{_libdir}/*.so.*

%files devel
%{_includedir}/qhyccd*.h
%{_libdir}/pkgconfig/%{name}*.pc
%{_libdir}/*.a
%{_docdir}/%{name}-%{version}/*.pdf
%{_docdir}/%{name}-%{version}/testapp/*/*
%{_docdir}/%{name}-%{version}/cmake_modules/*

%files firmware
%{_udevrulesdir}/*.rules
/lib/firmware/qhy/*

%changelog
* Wed Mar 6 2019 James Fidell <james@openastroproject.org> - 4.0.15-1
- Initial RPM release

