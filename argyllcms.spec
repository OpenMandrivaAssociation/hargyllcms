%define alphaversion Beta7

Name:    argyllcms
Version: 0.70
Release: %mkrel 0.1.%{alphaversion}.2
Summary: ICC compatible color management system

Group:     Graphics
License:   GPLv3
URL:       http://www.argyllcms.com/
Source0:   http://www.argyllcms.com/argyllV%{version}%{alphaversion}_src.zip
# unbind Huey from HID driver
Source1:   96-Argyll.rules
Patch0:    %{name}-0.70-build.patch
BuildRoot: %{_tmppath}/%{name}-%{version}-%{release}

BuildRequires: jam, libtiff-devel, libusb-devel
BuildRequires: libx11-devel, libxext-devel, libxxf86vm-devel, libxinerama-devel
BuildRequires: libxscrnsaver-devel

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
%setup -q -c
# Remove useless bundled libs to make sure we don't accidentally include them
rm -fr tiff libusb libusbw

%patch0 -p1 -b .build

%build
CCOPTFLAG=`echo %{optflags} | sed -e 's/-Wp,-D_FORTIFY_SOURCE=2//g'`
NUMBER_OF_PROCESSORS="$RPM_N_CPUS"
export CCOPTFLAG RPM_N_CPUS

sh ./makeall.ksh

%install
rm -rf %{buildroot}
mkdir -p %{buildroot}%{_prefix} %{buildroot}%{_datadir}
export DOTDOT=%{buildroot}%{_prefix}

sh ./makeinstall.ksh 

mv %{buildroot}%{_prefix}/ref %{buildroot}%{_datadir}/argyllcms
chmod 755 %{buildroot}%{_bindir}/*

mv %{buildroot}%{_bindir}/icclink  %{buildroot}%{_bindir}/argyll-icclink

mkdir -p %{buildroot}%{_sysconfdir}/udev/rules.d
install -m 644 %{SOURCE1} %{buildroot}%{_sysconfdir}/udev/rules.d
# remove unpackaged files
rm -f $RPM_BUILD_ROOT%{_bindir}/*.txt

%clean
rm -rf %{buildroot}

%files
%defattr(-,root,root,-)
%doc doc/ *.txt
%config(noreplace) %{_sysconfdir}/udev/rules.d/96-Argyll.rules
%{_bindir}/*
%{_datadir}/argyllcms
