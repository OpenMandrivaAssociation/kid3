%define	use_gstreamer	0

Summary:	ID3 Tagger
Name:		kid3
Version:	3.9.7
Release:	1
License:	GPLv2+
Group:		Sound
Url:		https://kid3.kde.org
Source0:	http://prdownloads.sourceforge.net/kid3/%{name}-%{version}.tar.gz
Patch0:		kid3-3.9.2-compile.patch
BuildRequires:	cmake >= 3.16
BuildRequires:	docbook-style-xsl
BuildRequires:	gettext
BuildRequires:	python
BuildRequires:	xsltproc
BuildRequires:	cmake(ECM)
BuildRequires:	cmake(KF6Config)
BuildRequires:	cmake(KF6ConfigWidgets)
BuildRequires:	cmake(KF6CoreAddons)
BuildRequires:	cmake(KF6DocTools)
BuildRequires:	cmake(KF6KIO)
BuildRequires:	cmake(KF6WidgetsAddons)
BuildRequires:	cmake(KF6XmlGui)
BuildRequires:	id3lib-devel
BuildRequires:	pkgconfig(flac)
BuildRequires:	pkgconfig(flac++)
%if %{use_gstreamer}
BuildRequires:	pkgconfig(gstreamer-1.0)
%else
BuildRequires:	ffmpeg-devel
%endif
BuildRequires:	pkgconfig(libchromaprint)
BuildRequires:	pkgconfig(ogg)
BuildRequires:	pkgconfig(Qt6Core)
BuildRequires:	pkgconfig(Qt6Gui)
BuildRequires:	pkgconfig(Qt6DBus)
BuildRequires:	pkgconfig(Qt6Linguist)
BuildRequires:	pkgconfig(Qt6Multimedia)
BuildRequires:	pkgconfig(Qt6Network)
BuildRequires:	pkgconfig(Qt6Svg)
BuildRequires:	pkgconfig(Qt6Qml)
BuildRequires:	pkgconfig(Qt6Quick)
BuildRequires:	pkgconfig(Qt6QuickControls2)
BuildRequires:	pkgconfig(Qt6Test)
BuildRequires:	pkgconfig(Qt6Widgets)
BuildRequires:	pkgconfig(Qt6Xml)
BuildRequires:	pkgconfig(readline)
BuildRequires:	pkgconfig(taglib) >= 1.4
BuildRequires:	pkgconfig(vorbis)
BuildRequires:	pkgconfig(x11)
BuildRequires:	pkgconfig(xext)
BuildRequires:	pkgconfig(zlib)
Requires:	xdg-utils

%description
If you want to easily tag multiple MP3, Ogg/Vorbis, FLAC, MPC, MP4/AAC,
MP2, Speex, TrueAudio, WavPack, WMA, WAV and AIFF files (e.g. full albums)
without typing the same information again and again, and have control over
both ID3v1 and ID3v2 tags, then Kid3 is the program you are looking for.
With Kid3 you can:
- Edit ID3v1.1 tags.
- Edit all ID3v2.3 and ID3v2.4 frames.
- Convert between ID3v1.1, ID3v2.3 and ID3v2.4 tags.
- Edit tags of multiple files.
- Generate tags from filenames.
- Generate filenames from tags.
- Generate play-list files.
- Automatic case conversion and string translation.
- Import and export album data.
- Import from gnudb.org, TrackType.org, MusicBrainz, Discogs, Amazon.

%files -f %{name}.lang
%doc AUTHORS ChangeLog COPYING LICENSE README
%{_docdir}/HTML/*/%{name}/*
%{_kde5_bindir}/%{name}
%{_datadir}/applications/org.kde.%{name}.desktop
%{_kde5_iconsdir}/hicolor/*/apps/%{name}.png
%{_kde5_iconsdir}/hicolor/scalable/apps/%{name}.svgz
%{_datadir}/dbus-1/interfaces/*.xml
%{_datadir}/metainfo/org.kde.%{name}.appdata.xml
%{_datadir}/kxmlgui5/%{name}/kid3ui.rc
%{_mandir}/man1/%{name}.1*

#--------------------------------------------------------------------

%package	qt
Summary:	Efficient Qt ID3 tag editor
Group:	Sound
Requires:	xdg-utils

%description	qt
If you want to easily tag multiple MP3, Ogg/Vorbis, FLAC, MPC,
MP4/AAC, MP2, Speex, TrueAudio and WavPack files (e.g. full albums)
without typing the same information again and again and have control
over both ID3v1 and ID3v2 tags, then Kid3 is the program you are
looking for.
This package provides Kid3 built without KDE dependencies.

%files qt -f %{name}-qt.lang
%dir %{_datadir}/%{name}/
%dir %{_datadir}/%{name}/translations/
%{_bindir}/%{name}-qt
%{_datadir}/applications/org.kde.%{name}-qt.desktop
%{_datadir}/icons/hicolor/*/apps/%{name}-qt.png
%{_datadir}/icons/hicolor/scalable/apps/%{name}-qt.svg
# This is not needed for qt
#{_datadir}/dbus-1/interfaces/*.xml
%{_datadir}/%{name}/translations/*.qm
%{_docdir}/%{name}-qt
%{_datadir}/metainfo/org.kde.%{name}-qt.appdata.xml
%{_mandir}/man1/%{name}-qt.1*

#--------------------------------------------------------------------

%package	cli
Summary:	Efficient CLI ID3 tag editor
Group:	Sound

%description	cli
If you want to easily tag multiple MP3, Ogg/Vorbis, FLAC, MPC,
MP4/AAC, MP2, Speex, TrueAudio and WavPack files (e.g. full albums)
without typing the same information again and again and have control
over both ID3v1 and ID3v2 tags, then Kid3 is the program you are
looking for.
This package provides Kid3 built without GUI dependencies.

%files cli -f %{name}-cli.lang
%{_bindir}/%{name}-cli
%{_mandir}/man1/%{name}-cli.1*

#--------------------------------------------------------------------

%prep
%autosetup -p1


%build
%cmake	-DBUILD_SHARED_LIBS:BOOL=OFF \
		-DWITH_TAGLIB=ON \
		-DWITH_ID3LIB=ON \
		-DWITH_VORBIS=ON \
		-DWITH_FLAC=ON \
		-DWITH_CHROMAPRINT=ON \
		-DWITH_APPS="Qt;CLI;KDE" \
		-DBUILD_WITH_QT6=ON \
%if %{use_gstreamer}
		-DWITH_GSTREAMER=ON \
		-DWITH_FFMPEG=OFF \
%else
		-DWITH_GSTREAMER=OFF \
		-DWITH_FFMPEG=ON \
%endif
		-DPYTHON_EXECUTABLE=%{__python} \
		-G ninja

%ninja_build


%install
%ninja_install -C build

%find_lang kid3 --with-man
%find_lang kid3-qt --with-man
%find_lang kid3-cli --with-man
