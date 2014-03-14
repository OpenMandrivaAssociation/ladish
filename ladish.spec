%define branch 0
%{?_branch: %{expand: %%global branch 1}}

%if %branch
%define git_snapshot git20101228
%endif

Name:           ladish
Summary:        LADI Audio Session Handler
Version:        1
%if %branch
Release:        %git_snapshot
%else
Release:        4
%endif

%if %branch
Source:         http://ladish.org/download/%{name}-%version-%git_snapshot.tar.bz2
%else
Source:         http://ladish.org/download/%name-%version-with-deps.tar.bz2
%endif
Patch0:		ladish-glibc.patch
URL:            http://ladish.org
License:        GPLv2
Group:          Sound
BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-buildroot

Requires:   laditools
Requires:   ladish-alsapid
BuildRequires:  jackit-devel >= 1.9.0
BuildRequires:  libalsa-devel
BuildRequires:  libuuid-devel
BuildRequires:  dbus-devel
BuildRequires:  expat-devel
BuildRequires:  gtk+2.0-devel
BuildRequires:  dbus-glib-devel
BuildRequires:  boost-devel
BuildRequires:  flowcanvas-devel >= 0.6.4
BuildRequires:  pygtk2.0-devel
BuildRequires:  python-yaml
BuildRequires:  intltool
Suggests:       a2jmidid

%description
Session management system for JACK applications on GNU/Linux. Its aim
is to have many different audio programs running at once, to save their
setup, close them down and then easily reload the setup at some other
time. ladish doesn't deal with any kind of audio or MIDI data itself;
it just runs programs, deals with saving/loading (arbitrary) data and
connects JACK ports together.
Ladish has a GUI frontend called gladish, based on lpatchage (LADI Patchage)
and the ladish_control command line app for headless operation.

%package -n laditools
Summary:    Tools to configure Jack
Group:      Sound
Requires:   jackit >= 1.9.0
Requires:   pygtk2.0 pygtk2.0-libglade
Requires:   python-vte python-pyxml python-yaml
Requires:   python-dbus

%description -n laditools
A suite of tools to configure and control the Jack Audio Connection Kit.
Laditools contains laditray, a tray icon control tool for Jack D-Bus.
This package is mandatory for installing the LADI Audio Session Handler.

%package alsapid
Summary:    Preloaded library for Ladish-ALSA interface
Group:      Sound

%description alsapid
Part of the LADI Audio Session Handler. This library is preloaded to the
ladish daemon for better interfacing ladish with ALSA

%prep
%if %branch
%setup -q -n %{name}-%{version}-%{git_snapshot}
%else
%setup -q
%endif
%apply_patches

%build
./waf configure --prefix=%{_prefix}
./waf

%install
rm -rf %buildroot
./waf install --destdir=%{buildroot}
cd laditools
python setup.py install --prefix=%{buildroot}%{_prefix}

#Fix desktop file category syntax
perl -pi -e 's/AudioVideo/AudioVideo;/g' %buildroot/%{_datadir}/applications/laditray.desktop
perl -pi -e 's/Settings/Settings;/g' %buildroot/%{_datadir}/applications/ladiconf.desktop

%clean
rm -rf %{buildroot}

%files
%defattr(-,root,root)
%doc %{_datadir}/%{name}/README
%doc %{_datadir}/%{name}/AUTHORS
%doc %{_datadir}/%{name}/COPYING
%doc %{_datadir}/%{name}/NEWS

%lang(de) %{_localedir}/de/LC_MESSAGES/ladish.mo
%lang(fr) %{_localedir}/fr/LC_MESSAGES/ladish.mo
%lang(ru) %{_localedir}/ru/LC_MESSAGES/ladish.mo

%{_bindir}/gladish
%{_bindir}/ladishd
%{_bindir}/jmcore
%{_bindir}/ladiconfd
%{_bindir}/ladish_control

%dir %{_datadir}/%{name}
%{_datadir}/%{name}/gladish.ui
%{_datadir}/%{name}/*.png

%{_datadir}/dbus-1/services/org.ladish.service
%{_datadir}/dbus-1/services/org.ladish.conf.service
%{_datadir}/dbus-1/services/org.ladish.jmcore.service

%{_iconsdir}/hicolor/*/apps/gladish.png

%files -n laditools
%doc %{_docdir}/laditools/*
%{_bindir}/g15ladi
%{_bindir}/ladiconf
%{_bindir}/ladilog
%{_bindir}/laditray
%{_bindir}/wmladi
%{python_sitelib}/laditools
%{python_sitelib}/laditools-1.0_rc2-py%{python_version}.egg-info
%{_datadir}/applications/*
%{_datadir}/laditools/*
%{_datadir}/pixmaps/*.svg

%files alsapid
%{_prefix}/lib/libalsapid.so


%changelog
* Tue Apr 17 2012 Frank Kober <emuse@mandriva.org> 1-4
+ Revision: 791523
- rebuild for dependency check

* Sat Dec 24 2011 Frank Kober <emuse@mandriva.org> 1-3
+ Revision: 745022
- rebuild to link against newer libpng

* Fri Dec 23 2011 Frank Kober <emuse@mandriva.org> 1-2
+ Revision: 744880
- cleanup some warnings

* Thu Dec 22 2011 Frank Kober <emuse@mandriva.org> 1-1
+ Revision: 744587
- new version 1

* Wed Apr 20 2011 Frank Kober <emuse@mandriva.org> 0.3-5
+ Revision: 656129
- Suggests a2jmidid added

* Sun Feb 27 2011 Funda Wang <fwang@mandriva.org> 0.3-4
+ Revision: 640608
- rebuild
- rebuild
- rebuild to obsolete old packages

* Mon Feb 14 2011 Frank Kober <emuse@mandriva.org> 0.3-3
+ Revision: 637800
- add python-dbus requires

* Fri Jan 21 2011 Frank Kober <emuse@mandriva.org> 0.3-2
+ Revision: 632074
- rebuild for new flowcanvas

* Sun Jan 09 2011 Frank Kober <emuse@mandriva.org> 0.3-1
+ Revision: 630832
- new version 0.3

* Wed Dec 29 2010 Frank Kober <emuse@mandriva.org> 0.3-0.git20101228.1mdv2011.0
+ Revision: 625887
- %%{_localedir} doesn't seem to exist
- new git snapshot

* Sun Dec 12 2010 Frank Kober <emuse@mandriva.org> 0.3-0.git20101212.1mdv2011.0
+ Revision: 620613
- new git snapshot

* Mon Nov 01 2010 Frank Kober <emuse@mandriva.org> 0.3-0.git20101101.1mdv2011.0
+ Revision: 591667
- fix path for alsapid.so
- add alsa-lib-devel BR
- update to current git version

* Sun Apr 04 2010 Frank Kober <emuse@mandriva.org> 0.2-3mdv2010.1
+ Revision: 531470
- add librsvg to Requires

* Sat Mar 20 2010 Frank Kober <emuse@mandriva.org> 0.2-2mdv2010.1
+ Revision: 525524
- bump release 2
- add pygtk2.0-libglade to laditools Requires

* Tue Feb 23 2010 Stéphane Téletchéa <steletch@mandriva.org> 0.2-1mdv2010.1
+ Revision: 510274
- Fix python path since it does not matter if this ends in lib or lib64 dirs

  + Frank Kober <emuse@mandriva.org>
    - wrong BR name fixed
    - BR adjusted
    - missing pygtk2.0 added to Requires
    - import ladish


