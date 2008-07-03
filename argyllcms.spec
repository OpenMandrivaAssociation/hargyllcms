Name:    argyllcms
Version: 1.0.0
Release: %mkrel 1
Summary: ICC compatible color management system

Group:     Graphics
License:   GPLv3 and BSD-like
URL:       http://www.argyllcms.com/
Source0:   http://www.argyllcms.com/Argyll_V%{version}_src.zip
# add ACL for colorimeter devices (Nicolas Mailhot)
Source2:   argyllcms-0.70-19-color.fdi
Source3:   argyllcms-device-file.policy
# (fc) 0.70-0.1.beta7.1mdv fix build to use system libusb 
Patch0:  argyllcms-1.0.0-libusb.patch
# (fc) 1.0.0-1mdv various upstream fixes
Patch1:	 argyllcms-1.0.0-variousfixes.patch
BuildRoot: %{_tmppath}/%{name}-%{version}-%{release}

BuildRequires: jam, libtiff-devel, libusb-devel
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
%patch0 -p1 -b .libusb
%patch1 -p1 -b .variousfixes


%build
CCOPTFLAG="%{optflags}"
NUMBER_OF_PROCESSORS="$RPM_N_CPUS"
export CCOPTFLAG NUMBER_OF_PROCESSORS

sh ./makeall.sh

%install
rm -rf %{buildroot}
mkdir -p %{buildroot}%{_datadir}/argyllcms

sh ./makeinstall.sh 

mv bin %{buildroot}%{_prefix}
chmod 755  %{buildroot}%{_bindir}/*
cp ref/* %{buildroot}%{_datadir}/argyllcms

install -d -m 0755 %{buildroot}%{_datadir}/hal/fdi/policy/10osvendor
install -p -m 0644 libusb/19-color.fdi \
        %{buildroot}%{_datadir}/hal/fdi/policy/10osvendor/

install -d -m 0755 %{buildroot}%{_datadir}/PolicyKit/policy
install -m 644 libusb/color-device-file.policy %{buildroot}%{_datadir}/PolicyKit/policy

# remove unpackaged files
rm -f $RPM_BUILD_ROOT%{_bindir}/*.txt

%clean
rm -rf %{buildroot}

%files
%defattr(-,root,root,-)
%doc doc/*.html doc/*.jpg *.txt
%{_bindir}/*
%{_datadir}/argyllcms
%{_datadir}/hal/fdi/policy/10osvendor/19-color.fdi
%{_datadir}/PolicyKit/policy/color-device-file.policy
