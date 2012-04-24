%define major 0
%define libname %mklibname argyll %major
%define develname %mklibname argyll -d

Name:    argyllcms
Version: 1.4.0
Release: 1
Summary: ICC compatible color management system

%define icclib_version 2.12-1mdv

Group:     Graphics
License:   GPLv3 and BSD and MIT and AGPLv3
URL:       http://gitorious.org/hargyllcms
Source0:   http://people.freedesktop.org/~hughsient/releases/hargyllcms-%{version}.tar.xz
Patch0:    hargyllcms-1.4.0-mdv-linkage.patch

BuildRequires: libtiff-devel
BuildRequires: libjpeg-devel
BuildRequires: libx11-devel, libxext-devel, libxxf86vm-devel, libxinerama-devel
BuildRequires: libxscrnsaver-devel
BuildRequires: libxrandr-devel
BuildRequires: icclib-devel >= %{icclib_version}
BuildRequires: usb1.0-devel
Requires:      udev

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

%package -n %{libname}
Summary: Argyll CMS libraries
Group:   System/Libraries

%description -n %{libname}
This package contains shared libraries used by Argyll CMS.

%package -n %{develname}
Summary:  Argyll CMS development files
Group:    Development/C
Requires: %{libname} = %{version}

%description -n %{develname}
This package contains development files for Argyll CMS shared libraries.

%prep
%setup -q -n hargyllcms-%{version}
%patch0 -p1
autoreconf

%build
%configure --disable-static
#parallel build is broken
make

%install
%makeinstall_std

%if %{mdvver} <= 201100
rm -f %{buildroot}%{_libdir}/*.la
%endif

%files
%defattr(0644,root,root,0755)
%doc %{_defaultdocdir}/argyll
%attr(0755,root,root) %{_bindir}/*
%{_datadir}/color/argyll
/lib/udev/rules.d/55-Argyll.rules
%doc AUTHORS ChangeLog Readme.txt

%files -n %{libname}
%{_libdir}/libargyll*.so.%{major}*

%files -n %{develname}
%{_libdir}/libargyll*.so
%doc AUTHORS ChangeLog Readme.txt
