%define	use_gstreamer	0

Summary:	ID3 Tagger
Name:		kid3
Version:	3.9.4
Release:	4
License:	GPLv2+
Group:		Sound
Url:		https://kid3.kde.org
Source0:	http://prdownloads.sourceforge.net/kid3/%{name}-%{version}.tar.gz
Patch0:		kid3-3.9.2-compile.patch
BuildRequires:	cmake >= 2.8
BuildRequires:	cmake(ECM)
BuildRequires:	cmake(KF5KIO)
BuildRequires:	cmake(KF5DocTools)
BuildRequires:	cmake(Qt5Test)
BuildRequires:	cmake(Qt5Multimedia)
BuildRequires:	gettext
BuildRequires:	qt5-devel
BuildRequires:	chromaprint-devel
BuildRequires:	docbook-style-xsl
BuildRequires:	pkgconfig(ogg)
BuildRequires:	pkgconfig(vorbis)
BuildRequires:	pkgconfig(zlib)
BuildRequires:	id3lib-devel
BuildRequires:	taglib-devel >= 1.4
BuildRequires:	pkgconfig(flac++)
BuildRequires:	readline-devel
BuildRequires:	xsltproc
BuildRequires:	python
%if %{use_gstreamer}
BuildRequires:	pkgconfig(gstreamer-1.0) >= 0.10
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
Summary:	Efficient Qt ID3 tag editor
Group:		Sound
Requires:	xdg-utils

%description	qt
If you want to easily tag multiple MP3, Ogg/Vorbis, FLAC, MPC,
MP4/AAC, MP2, Speex, TrueAudio and WavPack files (e.g. full albums)
without typing the same information again and again and have control
over both ID3v1 and ID3v2 tags, then Kid3 is the program you are
looking for. This package provides Kid3 built without KDE dependencies.

#--------------------------------------------------------------------

%package	cli
Summary:	Efficient CLI ID3 tag editor
Group:		Sound

%description	cli
If you want to easily tag multiple MP3, Ogg/Vorbis, FLAC, MPC,
MP4/AAC, MP2, Speex, TrueAudio and WavPack files (e.g. full albums)
without typing the same information again and again and have control
over both ID3v1 and ID3v2 tags, then Kid3 is the program you are
looking for. This package provides Kid3 built without GUI dependencies.


#--------------------------------------------------------------------

%prep
%autosetup -p1

%build
%cmake_kde5	-DBUILD_SHARED_LIBS:BOOL=OFF \
		-DWITH_TAGLIB=ON \
		-DWITH_ID3LIB=ON \
		-DWITH_VORBIS=ON \
		-DWITH_FLAC=ON \
		-DWITH_CHROMAPRINT=ON \
		-DWITH_APPS="Qt;CLI;KDE" \
		-DWITH_QT5=ON \
		-DPYTHON_EXECUTABLE=%__python \
%if %{use_gstreamer}
		-DWITH_GSTREAMER=ON \
		-DWITH_FFMPEG=OFF \
%else
		-DWITH_GSTREAMER=OFF \
		-DWITH_FFMPEG=ON \
%endif
		-DWITH_PHONON=ON
%ninja


%install
%ninja_install -C build

%find_lang kid3 --with-man
%find_lang kid3-qt --with-man
%find_lang kid3-cli --with-man

#--------------------------------------------------------------------

%files -f kid3.lang
%doc AUTHORS ChangeLog COPYING LICENSE README
%{_docdir}/HTML/*/%{name}/*
%{_kde5_bindir}/%{name}
%{_datadir}/applications/org.kde.kid3.desktop
%{_kde5_iconsdir}/hicolor/*/apps/%{name}.png
%{_kde5_iconsdir}/hicolor/scalable/apps/%{name}.svgz
%{_datadir}/dbus-1/interfaces/*.xml
%{_datadir}/metainfo/org.kde.kid3.appdata.xml
%{_datadir}/kxmlgui5/kid3/kid3ui.rc
%{_mandir}/man1/kid3.1*

#--------------------------------------------------------------------

%files qt -f kid3-qt.lang
%dir %{_datadir}/%{name}/
%dir %{_datadir}/%{name}/translations/
%{_bindir}/%{name}-qt
%{_datadir}/applications/org.kde.kid3-qt.desktop
%{_datadir}/icons/hicolor/*/apps/%{name}-qt.png
%{_datadir}/icons/hicolor/scalable/apps/%{name}-qt.svg
# This is not needed for qt
#{_datadir}/dbus-1/interfaces/*.xml
%{_datadir}/%{name}/translations/*.qm
%{_docdir}/%{name}-qt
%{_datadir}/metainfo/org.kde.kid3-qt.appdata.xml
%{_mandir}/man1/kid3-qt.1*

%files cli -f kid3-cli.lang
%{_bindir}/kid3-cli
%{_mandir}/man1/kid3-cli.1*
