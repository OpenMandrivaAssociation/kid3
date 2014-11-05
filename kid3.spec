%define	use_gstreamer	0

Summary:	ID3 Tagger
Name:		kid3
Version:	3.0.2
Release:	1
License:	GPLv2+
Group:		Sound
Url:		http://kid3.sourceforge.net/
Source0:	http://prdownloads.sourceforge.net/kid3/%{name}-%{version}.tar.gz
BuildRequires:	cmake >= 2.8
BuildRequires:	gettext
BuildRequires:	kdelibs4-devel
BuildRequires:	qt4-devel
BuildRequires:  kde4-macros
BuildRequires:	chromaprint-devel
BuildRequires:	docbook-style-xsl
BuildRequires:	pkgconfig(ogg)
BuildRequires:	pkgconfig(vorbis)
BuildRequires:	id3lib-devel
BuildRequires:	taglib-devel >= 1.4
BuildRequires:	libmp4v2-devel
BuildRequires:	libtunepimp-devel
BuildRequires:	pkgconfig(flac++)
BuildRequires:	readline-devel
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
%setup -q


%build
%cmake_kde4	-DBUILD_SHARED_LIBS:BOOL=OFF \
		-DWITH_TAGLIB=ON -DWITH_MP4V2=ON \
		-DWITH_ID3LIB=ON -DWITH_VORBIS=ON \
		-DWITH_FLAC=ON -DWITH_CHROMAPRINT=ON \
		-DWITH_APPS="Qt;CLI;KDE" \
%if %{use_gstreamer}
		-DWITH_GSTREAMER=ON -DWITH_FFMPEG=OFF \
%else
		-DWITH_GSTREAMER=OFF -DWITH_FFMPEG=ON \
%endif
		-DWITH_PHONON=ON
%make


%install
%makeinstall_std -C build

#--------------------------------------------------------------------

%files
%doc AUTHORS ChangeLog COPYING LICENSE README
%{_docdir}/HTML/*/%{name}/*
%{_kde_bindir}/%{name}
%{_kde_applicationsdir}/%{name}.desktop
%{_kde_appsdir}/%{name}/*
%{_kde_iconsdir}/hicolor/*/apps/%{name}.png
%{_kde_iconsdir}/hicolor/scalable/apps/%{name}.svgz
%{_datadir}/dbus-1/interfaces/*.xml
%{_mandir}/man1/%{name}.1*
%lang(de) %{_mandir}/de/man1/%{name}.1*

#--------------------------------------------------------------------

%files qt
%dir %{_datadir}/%{name}/
%dir %{_datadir}/%{name}/translations/
%{_bindir}/%{name}-qt
%{_datadir}/applications/%{name}-qt.desktop
%{_datadir}/icons/hicolor/*/apps/%{name}-qt.png
%{_datadir}/icons/hicolor/scalable/apps/%{name}-qt.svg
# This is not needed for qt
#{_datadir}/dbus-1/interfaces/*.xml
%{_datadir}/%{name}/translations/*.qm
%{_mandir}/man1/%{name}-qt.1*
%lang(de) %{_mandir}/de/man1/%{name}-qt.1*
%{_docdir}/%{name}-qt

%files cli
%{_bindir}/kid3-cli
%{_mandir}/man1/kid3-cli.1*
%lang(de) %{_mandir}/de/man1/kid3-cli.1*
