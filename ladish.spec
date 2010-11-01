%define branch 1
%{?_branch: %{expand: %%global branch 1}}

%if %branch
%define git_snapshot git20101101
%endif

Name:           ladish
Summary:        LADI Audio Session Handler
Version:        0.3
%if %branch
Release: 		%mkrel -c %git_snapshot 1
%else
Release: 		%mkrel 1
%endif

%if %branch
Source:         http://ladish.org/download/%{name}-%version.%git_snapshot.tar.bz2
%else
Source:         http://ladish.org/download/%name-%version.tar.bz2
%endif
URL:            http://ladish.org
License:        GPLv2
Group:          Sound
BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-buildroot 

Requires:   laditools
BuildRequires:  libjack-devel >= 1.9.0
BuildRequires:  alsa-lib-devel
BuildRequires:  libuuid-devel
BuildRequires:  libdbus-1-devel
BuildRequires:  expat-devel
BuildRequires:  gtk2-devel
BuildRequires:  dbus-glib-devel
BuildRequires:  boost-devel
BuildRequires:  flowcanvas-devel >= 0.6.4
BuildRequires:  pygtk2.0-devel
BuildRequires:  python-yaml


%description
Session management system
for JACK applications on GNU/Linux. Its aim is to have
many different audio programs running at once, to save their setup,
close them down and then easily reload the setup at some other
time. ladish doesn't deal with any kind of audio or MIDI data itself;
it just runs programs, deals with saving/loading (arbitrary) data and
connects JACK ports together. 
Ladish has a GUI frontend called gladish, based on lpatchage (LADI Patchage)
and the ladish_control command line app for headless operation.

%package -n laditools
Summary:    Tools to configure Jack
Group:      Sound
Requires:   jackit >= 1.9.0
Requires:   pygtk2.0 pygtk2.0-libglade librsvg
Requires:   python-vte python-pyxml 
Provides:   laditools

%description -n laditools
A suite of tools to configure and control the Jack Audio Connection Kit.
Laditools contains laditray, a tray icon control tool for Jack D-Bus.
This package is mandatory for installing the LADI Audio Session Handler.

%prep
%if %branch
%setup -q -n %{name}-%{version}.%git_snapshot
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

%clean
#rm -rf %{buildroot}

%files 
%defattr(-,root,root)
%doc %{_datadir}/%{name}/README
%doc %{_datadir}/%{name}/AUTHORS
%doc %{_datadir}/%{name}/COPYING
%doc %{_datadir}/%{name}/NEWS

%{_bindir}/gladish
%{_bindir}/ladishd
%{_bindir}/jmcore
%{_bindir}/ladiconfd
%{_bindir}/ladish_control
%{_libdir}/libalsapid.so

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

