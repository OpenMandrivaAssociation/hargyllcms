%define lname hargyllcms
%define major 0
%define libname %mklibname argyll %{major}
%define devname %mklibname argyll -d

Summary:	ICC compatible color management system
Name:		argyllcms
Version:	1.5.1
Release:	1
Group:		Graphics
License:	GPLv3 and BSD and MIT and AGPLv3
Url:		http://gitorious.org/hargyllcms
Source0:	http://people.freedesktop.org/~hughsient/releases/%{lname}-%{version}.tar.xz
Patch0:		hargyllcms-1.4.0-mdv-linkage.patch

BuildRequires:	icclib-devel
BuildRequires:	jpeg-devel
BuildRequires:	tiff-devel
BuildRequires:	pkgconfig(x11)
BuildRequires:	pkgconfig(xext)
BuildRequires:	pkgconfig(xxf86vm)
BuildRequires:	pkgconfig(xinerama)
BuildRequires:	pkgconfig(xscrnsaver)
BuildRequires:	pkgconfig(xrandr)
BuildRequires:	pkgconfig(libusb-1.0)
Requires:	udev

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
Summary:	Argyll CMS libraries
Group:		System/Libraries

%description -n %{libname}
This package contains shared libraries used by Argyll CMS.

%package -n %{devname}
Summary:	Argyll CMS development files
Group:		Development/C
Requires:	%{libname} = %{version}

%description -n %{devname}
This package contains development files for Argyll CMS shared libraries.

%prep
%setup -qn %{lname}-%{version}
%apply_patches
mkdir -p m4
autoreconf -fi

%build
%configure2_5x \
	--disable-static

#parallel build is broke
%make -j1

%install
%makeinstall_std

%files
%doc %{_defaultdocdir}/argyll
%doc AUTHORS ChangeLog Readme.txt
%{_bindir}/*
%{_datadir}/color/argyll
/lib/udev/rules.d/55-Argyll.rules

%files -n %{libname}
%{_libdir}/libargyll*.so.%{major}*

%files -n %{devname}
%{_libdir}/libargyll*.so
%doc AUTHORS ChangeLog Readme.txt

