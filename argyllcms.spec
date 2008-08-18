Name:    argyllcms
Version: 1.0.2
Release: %mkrel 1
Summary: ICC compatible color management system

Group:     Graphics
License:   GPLv3 and BSD-like
URL:       http://www.argyllcms.com/
Source0:   http://www.argyllcms.com/Argyll_V%{version}_src.zip
# (fc) 1.0.1-1mdv change build system to use autotools (and build with system libusb) (Alastair M. Robinson)
Patch0:  http://www.blackfiveservices.co.uk/Argyll_V1.0.1_autotools.patch
# (fc) 1.0.0-1mdv remove call to additional internal libusb api, not needed
Patch1:  argyllcms-1.0.0-libusb.patch

BuildRoot: %{_tmppath}/%{name}-%{version}-%{release}

BuildRequires: libtiff-devel, libusb-devel
BuildRequires: libx11-devel, libxext-devel, libxxf86vm-devel, libxinerama-devel
BuildRequires: libxscrnsaver-devel
BuildRequires: libxrandr-devel

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

#needed by patch0
autoreconf -i


%build

%configure2_5x

#parallel build is broken
make

%install
rm -rf %{buildroot}

%makeinstall_std

install -d -m 0755 %{buildroot}%{_datadir}/hal/fdi/policy/10osvendor
install -p -m 0644 libusb/19-color.fdi \
        %{buildroot}%{_datadir}/hal/fdi/policy/10osvendor/

install -d -m 0755 %{buildroot}%{_datadir}/PolicyKit/policy
install -m 644 libusb/color-device-file.policy %{buildroot}%{_datadir}/PolicyKit/policy

%clean
rm -rf %{buildroot}

%files
%defattr(-,root,root,-)
%doc %{_datadir}/doc/argyll
%{_bindir}/*
%{_datadir}/color/argyll
%{_datadir}/hal/fdi/policy/10osvendor/19-color.fdi
%{_datadir}/PolicyKit/policy/color-device-file.policy
