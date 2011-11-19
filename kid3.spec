Summary:	ID3 Tagger
Name:		kid3
Version:	2.0.1
Release:	%mkrel 2
Source0:	http://prdownloads.sourceforge.net/kid3/%{name}-%{version}.tar.gz
License:	GPLv2+
Group:		Sound
Url:		http://kid3.sourceforge.net/
BuildRoot:	%{_tmppath}/%{name}-%{version}-%{release}-buildroot
BuildRequires:	cmake >= 2.8
BuildRequires:	gettext
BuildRequires:	kdelibs4-devel
BuildRequires:	qt4-devel
# For the QT build
BuildRequires:	docbook-style-xsl
BuildRequires:	libogg-devel
BuildRequires:	libvorbis-devel
BuildRequires:	id3lib-devel
BuildRequires:	taglib-devel >= 1.4
BuildRequires:	libmp4v2-devel
BuildRequires:	libtunepimp-devel
BuildRequires:	libflac++-devel
BuildRequires:	automoc4
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

%prep
%setup -q
#patch0 -p1 -b .qt4

%build
# First the KDE version
mkdir kde
cd kde
%cmake_kde4 -DBUILD_SHARED_LIBS:BOOL=OFF ../..
%make
cd ../..

# Then the "pure QT" version
mkdir qt
cd qt
%cmake_qt4	-DBUILD_SHARED_LIBS:BOOL=OFF -DWITH_KDE=OFF \
		-DWITH_DOCDIR=/usr/share/doc/%{name}-qt-%{version} \
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
%find_lang %{name} --with-kde --with-html
grep -F kid3 %{name}.lang > %{name}-kde.lang

%clean
rm -rf %{buildroot}

#--------------------------------------------------------------------

%files -f %{name}-kde.lang
%defattr(-,root,root)
%doc AUTHORS ChangeLog COPYING LICENSE README
%{_kde_bindir}/%{name}
%{_kde_applicationsdir}/%{name}.desktop
%{_kde_appsdir}/%{name}/*
%{_kde_iconsdir}/hicolor/*/apps/%{name}.png
%{_kde_iconsdir}/hicolor/scalable/apps/%{name}.svgz
%{_datadir}/dbus-1/interfaces/*.xml
%{_mandir}/man1/%{name}.1*

#--------------------------------------------------------------------

%files qt
%defattr(-,root,root)
%doc %{_docdir}/%{name}-qt-%{version}/
%dir %{_datadir}/%{name}-qt/
%{_bindir}/%{name}-qt
%{_datadir}/applications/%{name}-qt.desktop
%{_datadir}/icons/hicolor/*/apps/%{name}-qt.png
%{_datadir}/icons/hicolor/scalable/apps/%{name}-qt.svgz
%{_datadir}/dbus-1/interfaces/*.xml
%{_datadir}/%{name}-qt/translations/*.qm
%{_mandir}/man1/%{name}-qt.1*

