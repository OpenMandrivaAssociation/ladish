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
URL:            http://ladish.org
License:        GPLv2
Group:          Sound
BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-buildroot

Requires:   laditools
Requires:   ladish-alsapid
BuildRequires:  jackit-devel >= 1.9.0
BuildRequires:  alsa-lib-devel
BuildRequires:  libuuid-devel
BuildRequires:  dbus-devel
BuildRequires:  expat-devel
BuildRequires:  gtk2-devel
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
