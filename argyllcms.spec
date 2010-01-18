Name:    argyllcms
Version: 1.1.0
Release: %mkrel 1
Summary: ICC compatible color management system

%define icclib_version 2.12-1mdv
%define icclib_libname  %mklibname icc 2

Group:     Graphics
License:   GPLv3 and BSD-like
URL:       http://www.argyllcms.com/
Source0:   http://www.argyllcms.com/Argyll_V%{version}_src.zip
# (fc) 1.0.1-1mdv change build system to use autotools , build with system libusb and icclib (Alastair M. Robinson, Roland Mas) (Debian)
Patch0:    Argyll_V1.1.0_RC3_autotools.patch
# (fc) 1.0.0-1mdv remove call to additional internal libusb api, not needed
Patch1:    argyllcms-1.0.0-libusb.patch
# (fc) 1.1.0-1mdv fix crash in dispwin (upstream)
Patch2:    argyllcms-1.1.0-crashfix.patch

BuildRoot: %{_tmppath}/%{name}-%{version}-%{release}

BuildRequires: libtiff-devel, libusb-devel
BuildRequires: libx11-devel, libxext-devel, libxxf86vm-devel, libxinerama-devel
BuildRequires: libxscrnsaver-devel
BuildRequires: libxrandr-devel
BuildRequires: icclib-devel >= %{icclib_version}
Requires: %{icclib_libname} >= %{icclib_version}

%description
The Argyll color management system supports accurate ICC profile creation for
scanners, CMYK printers, film recorders and calibration and profiling of
displays.

Spectral sample data is supported, allowing a selection of illuminants observer
types, and paper fluorescent whitener additive compensation. Profiles can also
incorporate source specific gamut mappings for perceptual and saturation
intents. Gamut mapping and profile linking uses the CIECAM02 appearance model,
a unique gamut mapping algorithm, and a wide selection of rendering intents. It
also includes code for the fastest portable 8 bit raster color conversion
engine available anywhere, as well as support for fast, fully accurate 16 bit
conversion. Device color gamuts can also be viewed and compared using a VRML
viewer.

%prep
%setup -q -n Argyll_V%{version}
%patch0 -p1 -b .autotools
%patch1 -p1 -b .libusb
%patch2 -p1 -b .crashfix

#needed by patch0
autoreconf -i

%build

%configure2_5x

#parallel build is broken
make

%check
make check

%install
rm -rf %{buildroot}

%makeinstall_std

install -d -m 0755 %{buildroot}%{_sysconfdir}/udev/rules.d/
sed -e 's/MODE="666"/ENV{ACL_MANAGE}="1"/g' -e 's/SYSFS/ATTRS/g' libusb/55-Argyll.rules > %{buildroot}%{_sysconfdir}/udev/rules.d/55-Argyll.rules


%clean
rm -rf %{buildroot}

%files
%defattr(-,root,root,-)
%doc %{_datadir}/doc/argyll
%{_sysconfdir}/udev/rules.d/*.rules
%{_bindir}/*
%{_datadir}/color/argyll
%{_libdir}/argyll
