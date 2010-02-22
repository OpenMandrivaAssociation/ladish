%define name    ladish
%define version 0.2
%define release %mkrel 1

Name:           %{name} 
Summary:        LADI Audio Session Handler
Version:        %{version} 
Release:        %{release}

Source:         http://ladish.org/download/%name-%version.tar.bz2
URL:            http://ladish.org
License:        GPLv2
Group:          Sound
BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-buildroot 

Requires:	laditools
BuildRequires:  waf
BuildRequires:  libjack-devel >= 1.9.0
BuildRequires:  libuuid-devel
BuildRequires:  libdbus-1-devel
BuildRequires:  expat-devel
BuildRequires:  gtk2-devel
BuildRequires:  libglade2.0_0-devel
BuildRequires:  dbus-glib-devel
BuildRequires:  boost-devel
BuildRequires:  flowcanvas-devel
BuildRequires:  pygtk2.0-devel
BuildRequires:  pygtk2.0-libglade


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
Summary:	Tools to configure Jack
Group:		Sound
Requires:	jackit >= 1.9.0
Requires:	pygtk2.0
Requires:	python-vte python-pyxml
Provides:	laditools
%description -n laditools
A suite of tools to configure and control the Jack Audio Connection Kit.
Laditools contains laditray, a tray icon control tool for Jack D-Bus.
This package is mandatory for installing the LADI Audio Session Handler.
%prep
%setup -q

%build
./waf configure --prefix=%{_prefix} 
./waf

%install
rm -rf %buildroot
./waf install --destdir=%{buildroot}
cd laditools
python setup.py install --prefix=%{buildroot}%{_prefix}

%clean
rm -rf %{buildroot}

%files 
%defattr(-,root,root)
%doc %{_datadir}/%{name}/README
%doc %{_datadir}/%{name}/AUTHORS
%doc %{_datadir}/%{name}/COPYING
%doc %{_datadir}/%{name}/NEWS

%{_bindir}/gladish
%{_bindir}/ladishd
%{_bindir}/ladish_control
%dir %{_datadir}/%{name}
%{_datadir}/%{name}/ladish-logo-128x128.png
%{_datadir}/%{name}/gui.glade
%{_datadir}/dbus-1/services/org.ladish.service

%files -n laditools
%doc %{_docdir}/laditools/*
%{_bindir}/g15ladi
%{_bindir}/ladiconf
%{_bindir}/ladilog
%{_bindir}/laditray
%{_bindir}/wmladi
%{_libdir}/python2.6/site-packages/laditools
%{_libdir}/python2.6/site-packages/laditools-1.0_rc1-py2.6.egg-info
%{_datadir}/applications/*
%{_datadir}/laditools/*
%{_datadir}/pixmaps/*.svg

