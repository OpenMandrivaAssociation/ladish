%global	debug_package %{nil}

%define	tools_commit 61f59ae812ade134ceb45cfed6b06d1a9c96bb7f
#define	commit_short %%(echo %%{commit} | head -c6)
%define	commit_short gfcd24852

%bcond_without gui
# The present release don't build the old shared library
%bcond_with alsapid

Summary:	LADI Audio Session Handler
Name:		ladish
Version:	1.3
Release:	4
License:	GPLv2+
Group:		Sound
# Original Url: https://ladish.org
Url:		https://gitea.ladish.org/LADI/ladish
Source0:	https://dl.ladish.org/ladish/%{name}-%{version}-%{commit_short}.tar.bz2
Source1:	laditools-%{tools_commit}.tar.xz
Patch0:		ladish-1.3-build-locale.patch
Patch1:		ladish-1.3-aarch64.patch
BuildRequires:	meson
BuildRequires:	git
BuildRequires:	intltool
BuildRequires:librsvg
BuildRequires:	boost-devel
BuildRequires:	pkgconfig(alsa)
BuildRequires: 	pkgconfig(expat)
BuildRequires: 	pkgconfig(jack) >= 1.9.0
BuildRequires:	pkgconfig(uuid)
%if %{with gui}
BuildRequires:	pkgconfig(dbus-1)
BuildRequires:	pkgconfig(dbus-glib-1)
BuildRequires:	pkgconfig(gtkmm-2.4)
BuildRequires:	pkgconfig(libgnomecanvasmm-2.6)
%endif
# For laditools
BuildRequires:	pkgconfig(gtk+-3.0)
BuildRequires:	pkgconfig(librsvg-2.0)
BuildRequires:	pkgconfig(python3)
BuildRequires:	python-distutils-extra
BuildRequires:	python-setuptools
%if %{with alsapid}
Requires:	ladish-alsapid
%else
%rename	ladish-alsapid
%endif
Requires:	laditools
Recommends:	a2jmidid

%description
Session management system for JACK applications on GNU/Linux. Its aim
is to have many different audio programs running at once, to save their
setup, close them down and then easily reload the setup at some other
time. ladish doesn't deal with any kind of audio or MIDI data itself;
it just runs programs, deals with saving/loading (arbitrary) data and
connects JACK ports together.
Ladish has a GUI frontend called gladish, based on lpatchage (LADI Patchage)
and the ladish_control command line app for headless operation.

%files
%doc AUTHORS NEWS README.adoc
%{_bindir}/ladishd
%{_bindir}/jmcore
%{_bindir}/ladiconfd
%{_bindir}/%{name}_control
%dir %{_datadir}/%{name}
%if %{with gui}
%{_bindir}/gladish
%{_datadir}/applications/gladish.desktop
%{_datadir}/%{name}/gladish.ui
%{_datadir}/%{name}/*.png
#{_datadir}/dbus-1/services/org.ladish.service
#{_datadir}/dbus-1/services/org.ladish.conf.service
#{_datadir}/dbus-1/services/org.ladish.jmcore.service
%{_iconsdir}/hicolor/*/apps/gladish.png
%endif
%lang(bg) %{_localedir}/bg/LC_MESSAGES/%{name}.mo
%lang(de) %{_localedir}/de/LC_MESSAGES/%{name}.mo
%lang(fr) %{_localedir}/fr/LC_MESSAGES/%{name}.mo
%lang(ru) %{_localedir}/ru/LC_MESSAGES/%{name}.mo

#-----------------------------------------------------------------------------

%if %{with alsapid}
%package alsapid
Summary: Preloaded library for Ladish-ALSA interface
Group:	Sound

%description alsapid
Part of the LADI Audio Session Handler. This library is preloaded to the
ladish daemon for better interfacing ladish with ALSA

%files alsapid
%{_prefix}/lib/libalsapid.so
%endif

#----------------------------------------------------------------------------
# Compat drop-in library for old lash library
#

%define	major	1
%define	libname	%mklibname lash %{major}
%define	devname	%mklibname lash -d

%package -n %{libname}
Summary:	Compatibility library for lash
Group:	System/Libraries

%description -n %{libname}
Compatibility library for lash, usable as drop-in replacement

%files -n %{libname}
%doc README.adoc
%{_libdir}/liblash.so*

#----------------------------------------------------------------------------
# Devel files for the lash compat library
#

%package -n %{devname}
Summary:	Development files for lash compat library
Group:	Development/C++
Requires:	%{name} = %{version}-%{release}
Requires:	%{libname} = %{version}-%{release}
Conflicts:	%{devname} < %{version}-%{release}

%description -n %{devname}
This package contains the development files for the lash compatibility drop-in
library.

%files -n %{devname}
%doc COPYING
%{_includedir}/lash-1.0/lash/*.h
%{_libdir}/pkgconfig/liblash.pc

#-----------------------------------------------------------------------------

%package -n laditools
Summary:	Tools to configure Jack
Group:		Sound
Provides:	python-laditools = %{version}-%{release}
#Requires:	python-vte
Requires:	python-yaml
Requires:	python-dbus

%description -n laditools
This is a set of tools aiming to achieve the goals of the LADI project to
improve desktop integration and user workflow of Linux audio system based on
JACK and ladish.
This package is mandatory for installing the LADI Audio Session Handler.

%files -n laditools
%doc COPYING
%{_bindir}/g15ladi
%{_bindir}/wmladi
%{_bindir}/ladi-control-center
%{_bindir}/ladi-player
%{_bindir}/ladi-system-log
%{_bindir}/ladi-system-tray
%{py_puresitedir}/laditools
%{py_puresitedir}/laditools-1.1*.egg-info
%{_datadir}/applications/ladi-control-center.desktop
%{_datadir}/applications/ladi-player.desktop
%{_datadir}/applications/ladi-system-log.desktop
%{_datadir}/applications/ladi-system-tray.desktop
%{_datadir}/laditools/*
%lang(es) %{_localedir}/es/LC_MESSAGES/laditools.mo
%lang(it) %{_localedir}/it/LC_MESSAGES/laditools.mo
%lang(pt) %{_localedir}/pt/LC_MESSAGES/laditools.mo

#-----------------------------------------------------------------------------

%prep
%setup -q -n %{name}-%{version}-%{commit_short} -a1
mv laditools-%{tools_commit} laditools
%autopatch -p1


%build
# Build the main stuff
%meson  \
	-Dliblash=enabled \
%if %{with gui}
	-Dgladish=enabled \
%else
	-Dgladish=disabled \
%endif
	-Dpylash=disabled

%meson_build

# Build the laditools
pushd laditools
	%py_build
popd


%install
%meson_install

# Install laditools
pushd laditools
	%py_install
	mkdir -p %{buildroot}%{_datadir}/locale
	mkdir -p %{buildroot}%{_datadir}/applications
	cp -r build/mo/* %{buildroot}%{_datadir}/locale
	cp build/share/applications/* %{buildroot}%{_datadir}/applications
# The installation process "eats" the shebang for the tools: reinstall them manually
	cp ./{g15ladi,ladi-control-center,ladi-player,ladi-system-log,ladi-system-tray,wmladi} %{buildroot}%{_bindir}
popd

# Add a compatibility symlink for old lash library
ln -s liblash.so %{buildroot}%{_libdir}/liblash.so.1

# We pick those with our macro
rm -f %{buildroot}%{_datadir}/%{name}/{AUTHORS,NEWS,README.adoc}

# Fix perms
chmod +x %{buildroot}%{py_puresitedir}/laditools/*.py
chmod +x %{buildroot}%{py_puresitedir}/laditools/gtk/*.py

