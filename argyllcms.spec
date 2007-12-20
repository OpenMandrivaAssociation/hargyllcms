%define alphaversion Beta7

Name:    argyllcms
Version: 0.70
Release: %mkrel 0.1.%{alphaversion}.4
Summary: ICC compatible color management system

Group:     Graphics
License:   GPLv3 and BSD-like
URL:       http://www.argyllcms.com/
Source0:   http://www.argyllcms.com/argyllV%{version}%{alphaversion}_src.zip
# add ACL for colorimeter devices (Nicolas Mailhot)
Source2:   argyllcms-0.70-19-color.fdi
Source3:   argyllcms-device-file.policy
# (fc) 0.70-0.1.beta7.1mdv fix build to use system libtiff and libusb and link with -lm
Patch0:  argyllcms-0.70-build.patch
# (Daniel Berrange, Fedora) 0.70-0.1.beta7.3mdv fix buffer overflow in dispread
Patch1:  argyllcms-0.70-dispread-buffer-overflow.patch
# (Daniel Berrange, Fedora) 0.70-0.1.beta7.3mdv fix buffer overflow in iccdump
Patch2:  argyllcms-0.70-iccdump-buffer-overflow.patch
# (fc) 0.70-0.1.beta7.4mdv fix usb unbinding (Graeme Gill)
Patch3:  argyllcms-0.70-unbind-device.patch
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
%patch1 -p1 -b .dispread-buffer-overflow
%patch2 -p1 -b .iccdump-buffer-overflow
%patch3 -p1 -b .unbind-device

%build
CCOPTFLAG=`echo %{optflags} | sed -e 's/-Wp,-D_FORTIFY_SOURCE=2/-Wp,-D_FORTIFY_SOURCE=1/g'`
NUMBER_OF_PROCESSORS="$RPM_N_CPUS"
export CCOPTFLAG RPM_N_CPUS

sh ./makeall.ksh

%install
rm -rf %{buildroot}
mkdir -p %{buildroot}%{_prefix} %{buildroot}%{_datadir}
export DOTDOT=%{buildroot}%{_prefix}

sh ./makeinstall.ksh 

mv %{buildroot}%{_prefix}/ref %{buildroot}%{_datadir}/argyllcms
mv %{buildroot}%{_bindir}/*.gam %{buildroot}%{_datadir}/argyllcms
chmod 755 %{buildroot}%{_bindir}/*

# fix conflict with lcms version
mv %{buildroot}%{_bindir}/icclink  %{buildroot}%{_bindir}/icclink-%{name}

install -d -m 0755 %{buildroot}%{_datadir}/hal/fdi/policy/10osvendor
install -p -m 0644 %{SOURCE2} \
        %{buildroot}%{_datadir}/hal/fdi/policy/10osvendor/19-color.fdi

mkdir -p %{buildroot}%{_datadir}/PolicyKit/policy
install -m 644 %{SOURCE3} %{buildroot}%{_datadir}/PolicyKit/policy

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
%{_datadir}/PolicyKit/policy/argyllcms-device-file.policy
