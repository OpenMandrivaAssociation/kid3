%define	use_gstreamer	0

Summary:		ID3 Tagger
Name:		kid3
Version:		2.2
Release:		1
License:		GPLv2+
Group:		Sound
Url:		http://kid3.sourceforge.net/
Source0:		http://prdownloads.sourceforge.net/kid3/%{name}-%{version}.tar.gz
BuildRequires:	cmake >= 2.8
BuildRequires:	gettext
BuildRequires:	kdelibs4-devel
BuildRequires:	qt4-devel
BuildRequires:	chromaprint-devel
BuildRequires:	docbook-style-xsl
BuildRequires:	libogg-devel
BuildRequires:	libvorbis-devel
BuildRequires:	id3lib-devel
BuildRequires:	taglib-devel >= 1.4
BuildRequires:	libmp4v2-devel
BuildRequires:	libtunepimp-devel
BuildRequires:	libflac++-devel
%if %{use_gstreamer}
BuildRequires:	libgstreamer-devel >= 0.10
%else
BuildRequires:	ffmpeg-devel
%endif
Requires:	xdg-utils

%description
If you want to easily tag multiple MP3, Ogg/Vorbis, FLAC, MPC, MP4/AAC,
MP2, Speex, TrueAudio, WavPack, WMA, WAV and AIFF files (e.g. full albums)
without typing the same information again and again, and have control over
both ID3v1 and ID3v2 tags, then Kid3 is the program you are looking for.
With Kid3 you can:
- Edit ID3v1.1 tags
- Edit all ID3v2.3 and ID3v2.4 frames
- Convert between ID3v1.1, ID3v2.3 and ID3v2.4 tags
- Edit tags of multiple files
- Generate tags from filenames
- Generate filenames from tags
- Generate play-list files
- Automatic case conversion and string translation
- Import and export album data
- Import from gnudb.org, TrackType.org, MusicBrainz, Discogs, Amazon.

#--------------------------------------------------------------------

%package	qt
Summary:		Efficient Qt ID3 tag editor
Group:		Sound
Requires:	xdg-utils

%description	qt
If you want to easily tag multiple MP3, Ogg/Vorbis, FLAC, MPC,
MP4/AAC, MP2, Speex, TrueAudio and WavPack files (e.g. full albums)
without typing the same information again and again and have control
over both ID3v1 and ID3v2 tags, then Kid3 is the program you are
looking for. This package provides Kid3 built without KDE dependencies.

#--------------------------------------------------------------------

%prep
%setup -q


%build
# First the KDE version
mkdir kde
cd kde
%cmake_kde4	-DBUILD_SHARED_LIBS:BOOL=OFF \
		-DWITH_TAGLIB=ON -DWITH_MP4V2=ON \
		-DWITH_ID3LIB=ON -DWITH_VORBIS=ON \
		-DWITH_FLAC=ON -DWITH_CHROMAPRINT=ON \
%if %{use_gstreamer}
		-DWITH_GSTREAMER=ON -DWITH_FFMPEG=OFF \
%else
		-DWITH_GSTREAMER=OFF -DWITH_FFMPEG=ON \
%endif
		-DWITH_PHONON=ON ../..
%make
cd ../..

# Then the "pure QT" version
mkdir qt
cd qt
%cmake_qt4	-DBUILD_SHARED_LIBS:BOOL=OFF -DWITH_KDE=OFF \
		-DWITH_TAGLIB=ON -DWITH_MP4V2=ON \
		-DWITH_ID3LIB=ON -DWITH_VORBIS=ON \
		-DWITH_FLAC=ON -DWITH_CHROMAPRINT=ON \
%if %{use_gstreamer}
		-DWITH_GSTREAMER=ON -DWITH_FFMPEG=OFF \
%else
		-DWITH_GSTREAMER=OFF -DWITH_FFMPEG=ON \
%endif
		-DWITH_PHONON=ON -DWITH_DBUS=ON \
		-DWITH_DOCDIR=share/doc/%{name}-qt-%{version} \
		-DQT_PHONON_INCLUDE_DIR=/usr/include/phonon ../..
%make

%install
rm -rf %{buildroot}

%makeinstall_std -C kde/build
%makeinstall_std -C qt/build

mkdir -p %{buildroot}%{_mandir}/man1
install -m 0644 deb/kid3{,-qt}.1 %{buildroot}%{_mandir}/man1/

install -pm 644 AUTHORS ChangeLog COPYING LICENSE README \
    %{buildroot}%{_docdir}/%{name}-qt-%{version}


# This only finds the files for the KDE version
%find_lang %{name}
#grep -F kid3 %{name}.lang > %{name}-kde.lang


#--------------------------------------------------------------------

%files -f %{name}.lang
%doc AUTHORS ChangeLog COPYING LICENSE README
%{_docdir}/HTML/*/%{name}/*
%{_kde_bindir}/%{name}
%{_kde_applicationsdir}/%{name}.desktop
%{_kde_appsdir}/%{name}/*
%{_kde_iconsdir}/hicolor/*/apps/%{name}.png
%{_kde_iconsdir}/hicolor/scalable/apps/%{name}.svgz
%{_datadir}/dbus-1/interfaces/*.xml
%{_mandir}/man1/%{name}.1*

#--------------------------------------------------------------------

%files qt
%doc %{_docdir}/%{name}-qt-%{version}/
%dir %{_datadir}/%{name}-qt/
%dir %{_datadir}/%{name}-qt/translations/
%{_bindir}/%{name}-qt
%{_datadir}/applications/%{name}-qt.desktop
%{_datadir}/icons/hicolor/*/apps/%{name}-qt.png
%{_datadir}/icons/hicolor/scalable/apps/%{name}-qt.svg
# This is not needed for qt
#{_datadir}/dbus-1/interfaces/*.xml
%{_datadir}/%{name}-qt/translations/*.qm
%{_mandir}/man1/%{name}-qt.1*



%changelog
* Wed Oct 31 2012 Giovanni Mariani <mc2374@mclink.it> 2.2-1
- New version 2.2
- Dropped P0 (applied upstream)
- Added some explicit options to cmake command line
- Added means and BReqs to use ffmpeg or gstreamer to do chromaprint decoding

* Sat Oct 11 2012 Giovanni Mariani <mc2374@mclink.it> 2.1-1
- New version 2.1
- Removed BuildRoot, %%defattr, %%mkrel and %%clean section
- Added BReq for have chromaprint support
- Added P0 to fix build with ffmpeg 0.11
- Fix file lists

* Thu Nov 10 2011 Andrey Bondrov <abondrov@mandriva.org> 2.0.1-1mdv2011.0
+ Revision: 729605
- New version 2.0.1, sync with Giovanni Mariani's work in MIB - add pure qt4 subpackage

* Sun Feb 06 2011 Funda Wang <fwang@mandriva.org> 1.6-1
+ Revision: 636402
- update to new version 1.6

* Sat Sep 25 2010 Funda Wang <fwang@mandriva.org> 1.5-1mdv2011.0
+ Revision: 580970
- new version 1.5

* Sat Mar 06 2010 Funda Wang <fwang@mandriva.org> 1.4-1mdv2010.1
+ Revision: 514910
- update to new version 1.4

* Fri Nov 06 2009 Funda Wang <fwang@mandriva.org> 1.3-1mdv2010.1
+ Revision: 460660
- new version 1.3

* Fri May 01 2009 Funda Wang <fwang@mandriva.org> 1.2-1mdv2010.0
+ Revision: 369671
- New version 1.2

* Sun Oct 26 2008 Funda Wang <fwang@mandriva.org> 1.1-1mdv2009.1
+ Revision: 297418
- import kid3


