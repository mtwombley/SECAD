%define qt5 1

%if 0%{?suse_version}
%define dist .openSUSE%(echo %{suse_version} | sed 's/0$//')
%endif

%if 0%{?sles_version}
%define dist .SUSE%(echo %{sles_version} | sed 's/0$//')
%endif

%if %(if [[ "%{vendor}" == obs://* ]] ; then echo 1 ; else echo 0 ; fi)
%define opensuse_bs 1
%endif

%if 0%{?centos_ver}
%define centos_version %{centos_ver}00
%endif

Summary: CAD program for creating virtual LEGO models
Name: secad
URL: http://secad.org
%if 0%{?suse_version} || 0%{?sles_version}
Group: Productivity/Graphics/Viewers
%endif
%if 0%{?mdkversion} || 0%{?rhel_version} 
Group: Graphics
%endif
%if 0%{?fedora} || 0%{?centos_version}
Group: Amusements/Graphics
%endif
Version: 23.03
%if 0%{?opensuse_bs}
Release: <CI_CNT>.<B_CNT>%{?dist}
%else
Release: 1%{?dist}
%endif
%if 0%{?mdkversion} || 0%{?rhel_version} || 0%{?fedora} || 0%{?centos_version} || 0%{?scientificlinux_version} || 0%{?mageia}
License: GPLv2+
%endif
%if 0%{?suse_version} || 0%{?sles_version}
License: GPL-2.0+
BuildRequires: fdupes
%endif
Packager: Peter Bartfai <pbartfai@stardust.hu>
BuildRoot: %{_builddir}/%{name}

%if 0%{?fedora} || 0%{?rhel_version} || 0%{?centos_version} || 0%{?scientificlinux_version}
%if ( 0%{?centos_version}>=600 || 0%{?rhel_version}>=600 || 0%{?scientificlinux_version}>=600 )
%if 0%{?qt5}
BuildRequires: qt5-qtbase-devel >= 5.4.0, qt5-linguist
%else
BuildRequires: qt-devel >= 1:4.7.0
%endif
%endif
%endif
%if 0%{?fedora}
%if 0%{?qt5}
BuildRequires: qt5-qtbase-devel >= 5.4.0, qt5-linguist, qt5-qtgamepad-devel
%else
BuildRequires: qt-devel
%endif
%endif
%if 0%{?opensuse_bs}!=1
BuildRequires: git
%endif
%if (0%{?rhel_version}<700 && 0%{?centos_version}<700 && 0%{?scientificlinux_version}<600)
%else
BuildRequires: libjpeg-turbo-devel
%endif
BuildRequires: gcc-c++, libpng-devel, make


%if 0%{?fedora}
BuildRequires: libjpeg-turbo-devel
%if 0%{?opensuse_bs}
BuildRequires: samba4-libs
%if 0%{?fedora_version}==22
BuildRequires: qca
%endif
%if 0%{?fedora_version}==23
BuildRequires: qca, gnu-free-sans-fonts
%endif
%endif
%endif

%if 0%{?suse_version}
BuildRequires: update-desktop-files
%if 0%{?qt5}
BuildRequires: libqt5-qtbase-devel >= 5.4.0, zlib-devel, libqt5-linguist
%else
BuildRequires: libqt4-devel
%endif
Requires(pre): gconf2
%if 0%{?suse_version} > 1220
BuildRequires: glu-devel
%endif
%if 0%{?opensuse_bs}
BuildRequires:	-post-build-checks
%endif
%endif

%if 0%{?sles_version}
%if 0%{?opensuse_bs}
BuildRequires:	-post-build-checks
%endif
Requires(post): desktop-file-utils
%endif

%if 0%{?mageia}
%if 0%{?qt5}
BuildRequires: qttools5
%ifarch x86_64
BuildRequires: lib64qt5base5-devel
%else
BuildRequires: libqt5base5-devel
%endif
%if 0%{?opensuse_bs}
%ifarch x86_64
BuildRequires: lib64sane1, lib64proxy-webkit
%else
BuildRequires: libsane1, libproxy-webkit
%endif
%endif
%else
BuildRequires: libqt4-devel
%if 0%{?opensuse_bs}
%ifarch x86_64
BuildRequires: lib64sane1, lib64uuid-devel, lib64proxy-webkit
%else
BuildRequires: libsane1, libuuid-devel, libproxy-webkit
%endif
%endif
%endif
%endif

%if 0%{?mdkversion}
BuildRequires: libqt4-devel
# For openSUSE Build Service
%if 0%{?opensuse_bs}
%if (0%{?mdkversion} != 200910) && (0%{?mdkversion} != 201000)
BuildRequires: kde-l10n-en_GB
%endif
BuildRequires: aspell-en, myspell-en_US
%endif
%endif

%if ( 0%{?centos_version}<600 && 0%{?centos_version}>=500 ) || ( 0%{?rhel_version}<600 && 0%{?rhel_version}>=500 )
BuildRequires: qt4-devel >= 1:4.7.0
%endif

%description
CAD program for creating virtual LEGO models.
It has an intuitive interface, designed to allow 
new users to start creating new models without 
having to spend too much time learning the 
application.

%prep
cd $RPM_SOURCE_DIR
if [ -s secad.tar.gz ] ; then
	if [ -d secad ] ; then rm -rf secad ; fi
	tar zxf secad.tar.gz
else
	if [ -f secad-git.tar.gz ] ; then
		if [ -d secad ] ; then rm -rf secad ; fi
		mkdir secad
		cd secad
		tar zxf ../secad-git.tar.gz --strip=1
	elif [ -d secad ] ; then
		cd secad
		git pull
		cd ..
	else
		git clone https://github.com/sezide/secad
	fi
fi

%build
cd $RPM_SOURCE_DIR/secad
%ifarch i386 i486 i586 i686
%define qplatform linux-g++-32
%endif
%ifarch x86_64
%define qplatform linux-g++-64
%endif
%if ( 0%{?centos_version}<600 && 0%{?centos_version}>=500 ) || ( 0%{?rhel_version}<600 && 0%{?rhel_version}>=500 )
if [ -x %{_libdir}/qt4/bin/qmake ] ; then
export PATH=%{_libdir}/qt4/bin:$PATH
fi
%endif
%if (0%{?qt5}!=1)
%ifarch x86_64
export RPM_OPT_FLAGS="$RPM_OPT_FLAGS -I%{_libdir}/qt4/include"
%endif
%endif
%if 0%{?fedora}==23
%ifarch x86_64
export RPM_OPT_FLAGS="$RPM_OPT_FLAGS -fPIC"
export Q_CXXFLAGS="$Q_CXXFLAGS -fPIC"
%endif
%endif
%if 0%{?qt5}
export RPM_OPT_FLAGS="$RPM_OPT_FLAGS -fPIC"
if which qmake-qt5 >/dev/null 2>/dev/null ; then
        qmake-qt5 -spec %{qplatform} DISABLE_UPDATE_CHECK=1 LDRAW_LIBRARY_PATH=/usr/share/ldraw QMAKE_CXXFLAGS+="$Q_CXXFLAGS"
else
        qmake -spec %{qplatform} DISABLE_UPDATE_CHECK=1 LDRAW_LIBRARY_PATH=/usr/share/ldraw QMAKE_CXXFLAGS+="$Q_CXXFLAGS"
fi
%else
if which qmake-qt4 >/dev/null 2>/dev/null ; then
	qmake-qt4 -spec %{qplatform} DISABLE_UPDATE_CHECK=1 LDRAW_LIBRARY_PATH=/usr/share/ldraw QMAKE_CXXFLAGS+="$Q_CXXFLAGS"
else
	qmake -spec %{qplatform} DISABLE_UPDATE_CHECK=1 LDRAW_LIBRARY_PATH=/usr/share/ldraw QMAKE_CXXFLAGS+="$Q_CXXFLAGS"
fi
%endif
make clean
make TESTING="$RPM_OPT_FLAGS"
%if 0%{?qt5}
if which lrelease-qt5 >/dev/null 2>/dev/null ; then
        lrelease-qt5 secad.pro
else
        lrelease secad.pro
fi
%else
if which lrelease-qt4 >/dev/null 2>/dev/null ; then
	lrelease-qt4 secad.pro
else
	lrelease secad.pro
fi
%endif
%if 0%{?qt5} != 1
%endif

%install
cd $RPM_SOURCE_DIR/secad
install -d $RPM_BUILD_ROOT%{_bindir}
install -d $RPM_BUILD_ROOT%{_datadir}/secad
install -d $RPM_BUILD_ROOT%{_datadir}/icons/hicolor/scalable/mimetypes
install -d $RPM_BUILD_ROOT%{_datadir}/icons/hicolor/scalable/apps
install -d $RPM_BUILD_ROOT%{_mandir}/man1
install -m 755 build/release/secad $RPM_BUILD_ROOT%{_bindir}/secad
install -m 644 docs/README.md $RPM_BUILD_ROOT%{_datadir}/secad/README.md
install -m 644 docs/CREDITS.txt $RPM_BUILD_ROOT%{_datadir}/secad/CREDITS.txt
install -m 644 docs/COPYING.txt $RPM_BUILD_ROOT%{_datadir}/secad/COPYING.txt
install -m 644 docs/secad.1 $RPM_BUILD_ROOT%{_mandir}/man1/secad.1
gzip -f $RPM_BUILD_ROOT%{_mandir}/man1/secad.1
mkdir -p $RPM_BUILD_ROOT%{_datadir}/mime/packages/
mkdir -p $RPM_BUILD_ROOT%{_datadir}/applications/
install -m 644 qt/secad.xml  \
				$RPM_BUILD_ROOT%{_datadir}/mime/packages/secad.xml
install -m 644 qt/secad.desktop \
				$RPM_BUILD_ROOT%{_datadir}/applications/secad.desktop
install -m 644 tools/icon/scalable/mimetypes/application-vnd.secad.svg \
				$RPM_BUILD_ROOT%{_datadir}/icons/hicolor/scalable/mimetypes/application-vnd.secad.svg
install -m 644 tools/icon/scalable/apps/secad.svg \
				$RPM_BUILD_ROOT%{_datadir}/icons/hicolor/scalable/apps/secad.svg
%if 0%{?suse_version}
%suse_update_desktop_file secad Graphics
%endif

%files
%if 0%{?sles_version} || 0%{?suse_version}
%defattr(-,root,root)
%endif
%{_bindir}/secad
%dir %{_datadir}/secad
%doc %{_datadir}/secad/README.md
%doc %{_datadir}/secad/CREDITS.txt
%doc %{_datadir}/secad/COPYING.txt
%{_datadir}/mime/packages/secad.xml
%{_datadir}/applications/secad.desktop
%{_datadir}/icons/hicolor/scalable/mimetypes/application-vnd.secad.svg
%{_datadir}/icons/hicolor/scalable/apps/secad.svg
%if 0%{?mdkversion} || 0%{?mageia}
%{_mandir}/man1/secad.1.xz
%else
%{_mandir}/man1/secad.1.gz
%endif

%clean
rm -rf $RPM_BUILD_ROOT

%changelog
* Sun Jan 30 2022 - sT331h0rs3 (at) gmail.com 0.92
- Actualize SECAD version

* Sat May 08 2021 - sT331h0rs3 (at) gmail.com 0.91
- Build with Qt5 by default
- Actualize SECAD version
- Fix paths to SVG files

* Tue Sep 16 2016 - pbartfai (at) stardust.hu 0.90
- Initial version

