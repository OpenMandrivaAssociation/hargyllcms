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


%changelog
* Tue Apr 24 2012 Dmitry Mikhirev <dmikhirev@mandriva.org> 1.4.0-1
+ Revision: 793149
- update to 1.4.0

* Tue Mar 27 2012 Dmitry Mikhirev <dmikhirev@mandriva.org> 1.3.7-2
+ Revision: 787527
- fix license info
- fix devel package dependencies
- add documentation

* Tue Mar 27 2012 Dmitry Mikhirev <dmikhirev@mandriva.org> 1.3.7-1
+ Revision: 787512
- update to 1.3.7

* Fri Dec 23 2011 Dmitry Mikhirev <dmikhirev@mandriva.org> 1.3.5-1
+ Revision: 744894
- new version 1.3.5
  use hargyllcms sources

* Sun Dec 05 2010 Oden Eriksson <oeriksson@mandriva.com> 1.1.0-4mdv2011.0
+ Revision: 609990
- rebuild

* Thu Jan 28 2010 Frederic Crozat <fcrozat@mandriva.com> 1.1.0-3mdv2010.1
+ Revision: 497591
- Patch3: remove unneeded part of udev rules, requires udev >= 151 instead

* Wed Jan 27 2010 Frederic Crozat <fcrozat@mandriva.com> 1.1.0-2mdv2010.1
+ Revision: 497375
- Replace patch1 with new version from Roland Mas: argyllcms uses now its own local libusb, since it contains changes for some spectrometers.

* Mon Jan 18 2010 Frederic Crozat <fcrozat@mandriva.com> 1.1.0-1mdv2010.1
+ Revision: 493142
- Release 1.1.0 final
- Patch0 (upstream): fix crash in dispwin

* Thu Jan 14 2010 Frederic Crozat <fcrozat@mandriva.com> 1.1.0-0.rc4.2mdv2010.1
+ Revision: 491514
- Fix udev warning in rules file

* Wed Jan 06 2010 Frederic Crozat <fcrozat@mandriva.com> 1.1.0-0.rc4.1mdv2010.1
+ Revision: 486744
- Release 1.1.0 RC4
- Remove patch4, merged upstream
- Regenerate patch0

* Wed Oct 28 2009 Frederic Crozat <fcrozat@mandriva.com> 1.0.4-2mdv2010.0
+ Revision: 459667
- Adapt udev rules for ACL and install it by default

* Tue Jun 30 2009 Frederic Crozat <fcrozat@mandriva.com> 1.0.4-1mdv2010.0
+ Revision: 390977
- Release 1.0.4
- Regenerate 0 (partially merged)

* Tue Jun 09 2009 Frederic Crozat <fcrozat@mandriva.com> 1.0.3-3mdv2010.0
+ Revision: 384450
- Update patch0 with debian version which includes icclib update (fixes various CVE correctly)
- Build with system icclib
- Build various internal libraries as shared libraries

* Thu Apr 16 2009 Frederic Crozat <fcrozat@mandriva.com> 1.0.3-2mdv2009.1
+ Revision: 367783
- Update patch0 with addition from Roland Mas
- enable make check
- Patch2 (Fedora): CVE-2009-0583,0584
- Patch3 (Fedora): CVE-2009-0792
- Patch4: fix header and str_fmt errors

* Thu Sep 04 2008 Frederic Crozat <fcrozat@mandriva.com> 1.0.3-1mdv2009.0
+ Revision: 280459
- Release 1.0.3
- Regenerate patch1

* Mon Aug 18 2008 Frederic Crozat <fcrozat@mandriva.com> 1.0.2-1mdv2009.0
+ Revision: 273320
- Release 1.0.2
- Remove patches 2, 3 (merged upstream)

* Thu Jul 31 2008 Frederic Crozat <fcrozat@mandriva.com> 1.0.1-1mdv2009.0
+ Revision: 257520
- Release 1.0.1
- Remove patches 0 (fixed differently), 1 (merged upstream)
- Patch0: autotool based build system, from Alastair M. Robinsin
- Patch1: remvoe call to additional internal libusb api, not needed
- Patch2 (Fedora): double free fix
- Patch3: various upstream fixes

* Thu Jul 03 2008 Frederic Crozat <fcrozat@mandriva.com> 1.0.0-1mdv2009.0
+ Revision: 231173
- Fix BuildRequires
- Release 1.0.0
- Update patch0 to link with system libusb
- Patch1: various fixes from upstream (use ARGYLL_INGORE_XRANDR1_1=1 to disable xrandr 1.2 support in argyllcms)

* Wed Jan 16 2008 Frederic Crozat <fcrozat@mandriva.com> 0.70-0.1.Beta8.1mdv2008.1
+ Revision: 153663
- Release 0.70 beta8
- Remove patches 1, 2, 3, merged upstream

  + Olivier Blin <blino@mandriva.org>
    - restore BuildRoot

  + Thierry Vignaud <tv@mandriva.org>
    - kill re-definition of %%buildroot on Pixel's request

* Mon Dec 17 2007 Frederic Crozat <fcrozat@mandriva.com> 0.70-0.1.Beta7.4mdv2008.1
+ Revision: 121764
- Remove source1 and replace with patch3: fix usb unbinding (Graeme Grill)
- Update source2 with latest version from Fedora
- Clean specfile

* Thu Dec 13 2007 Frederic Crozat <fcrozat@mandriva.com> 0.70-0.1.Beta7.3mdv2008.1
+ Revision: 119409
- Sources 2, 3 : add HAL / PK files to set ACL on usb device node (initial work from Nicolas Mailhot)
- Patch1, 2: fix buffer overflows (Daniel Berrange, Fedora), allow build in FORTIFY_SOURCE=1
- move .gam files in datadir, rename icclink to icclink-argyll
- fix doc packaging

* Tue Dec 11 2007 Frederic Crozat <fcrozat@mandriva.com> 0.70-0.1.Beta7.2mdv2008.1
+ Revision: 117271
- Add udev rules for Huey colorimeter to unbind from usbhid module
- Fix package version

* Mon Dec 10 2007 Frederic Crozat <fcrozat@mandriva.com> 0.70-0.1.Beta7mdv2008.1
+ Revision: 117020
- import argyllcms


