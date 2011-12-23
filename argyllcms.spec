Name:    argyllcms
Version: 1.3.5
Release: %mkrel 1
Summary: ICC compatible color management system

%define icclib_version 2.12-1mdv

Group:     Graphics
License:   GPLv3 and BSD-like
URL:       http://gitorious.org/hargyllcms
Source0:   http://people.freedesktop.org/~hughsient/releases/hargyllcms-%{version}.tar.xz
Patch0:    argyllcms-1.3.5-fedora-ColorHug.patch

BuildRoot: %{_tmppath}/%{name}-%{version}-%{release}

BuildRequires: libtiff-devel
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

%prep
%setup -q -n hargyllcms-%{version}
%patch0 -p1 -b .colorhug

autoreconf -i

%build
%configure
#parallel build is broken
make

%install
rm -rf %{buildroot}
%makeinstall_std

%clean
rm -rf %{buildroot}

%files
%defattr(0644,root,root,0755)
%doc %{_defaultdocdir}/argyll
%attr(0755,root,root) %{_bindir}/*
%{_datadir}/color/argyll
/lib/udev/rules.d/55-Argyll.rules
