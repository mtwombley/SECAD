# Maintainer: Peter Bartfai <pbartfai[at]stardust[dot]hu>
pkgname=secad
pkgver=18.02
pkgrel=1
pkgdesc="SECAD is a CAD program for creating virtual LEGO models."
url="http://secad.org"
arch=('x86_64' 'i686')
license=('GPL')
#Qt4.x
depends=('qt4' 'libpng' 'libjpeg-turbo' 'mesa-libgl')
#Qt5.x
#depends=('qt5-base' 'qt5-tools' 'qt5-gamepad' 'libpng' 'libjpeg-turbo' 'mesa-libgl')
makedepends=('glu' 'ca-certificates')
conflicts=()
replaces=()
backup=()
source=("secad-git.tar.gz")
md5sums=(SKIP)

build() {
  cd ${srcdir}/secad-git
  if test "$CARCH" == x86_64; then
    PLATFORM=linux-g++-64
  else
    PLATFORM=linux-g++-32
  fi
  if [ -x /usr/bin/qmake ] ; then qmake -spec $PLATFORM DISABLE_UPDATE_CHECK=1 LDRAW_LIBRARY_PATH=/usr/share/ldraw ; lrelease secad.pro ;
  elif [ -x /usr/bin/qmake-qt4 ] ; then qmake-qt4 -spec $PLATFORM DISABLE_UPDATE_CHECK=1 LDRAW_LIBRARY_PATH=/usr/share/ldraw ; lrelease-qt4 secad.pro ;
  elif [ -x /usr/bin/qmake-qt5 ] ; then qmake-qt5 -spec $PLATFORM DISABLE_UPDATE_CHECK=1 LDRAW_LIBRARY_PATH=/usr/share/ldraw ; lrelease-qt5 secad.pro ; fi
  make 
}
 
package() {
  cd "${srcdir}/secad-git"
  mkdir -p ${pkgdir}/usr/bin
  mkdir -p ${pkgdir}/usr/share/secad
  install -m 755 build/release/secad ${pkgdir}/usr/bin
  install -m 644 docs/README.md  ${pkgdir}/usr/share/secad/README.md
  install -m 644 docs/CREDITS.txt ${pkgdir}/usr/share/secad/CREDITS.txt
  install -m 644 docs/COPYING.txt ${pkgdir}/usr/share/secad/COPYING.txt
  mkdir -p ${pkgdir}/usr/share/mime/packages/
  mkdir -p ${pkgdir}/usr/share/applications/
  mkdir -p ${pkgdir}/usr/share/icons/hicolor/scalable/mimetypes
  install -m 644 qt/secad.xml  \
				${pkgdir}/usr/share/mime/packages/secad.xml
  install -m 644 qt/secad.desktop \
				${pkgdir}/usr/share/applications/secad.desktop
  install -m 644 resources/application-vnd.secad.svg \
				${pkgdir}/usr/share/icons/hicolor/scalable/mimetypes/application-vnd.secad.svg
  make INSTALL_ROOT="${pkgdir}" install
}

