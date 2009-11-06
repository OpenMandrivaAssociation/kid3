Summary:	ID3 Tagger
Name:		kid3
Version: 	1.3
Release: 	%mkrel 1
Source0: 	http://prdownloads.sourceforge.net/kid3/%name-%version.tar.gz
License: 	GPLv2+
Group: 		Sound
Url: 		http://kid3.sourceforge.net/
BuildRoot: 	%{_tmppath}/%{name}-%{version}-%{release}-buildroot
BuildRequires: 	kdelibs4-devel
BuildRequires:	libvorbis-devel
BuildRequires:	libid3lib3.8-devel
BuildRequires:	taglib-devel
BuildRequires:	libmp4v2-devel
BuildRequires:	libtunepimp-devel
BuildRequires:	libflac++-devel

%description 
If you want to easily tag multiple MP3, Ogg/Vorbis, FLAC, MPC, MP4/AAC,
MP2, Speex, TrueAudio and WavPack files (e.g. full albums) without typing
the same information again and again and have control over both ID3v1 and
ID3v2 tags, then Kid3 is the program you are looking for.

%if %mdkversion < 200900
%post
%update_menus

%postun
%clean_menus
%endif

%files -f %name.lang
%defattr(-,root,root)
%_kde_bindir/*
%_kde_datadir/applications/kde4/*.desktop
%_kde_appsdir/*
%_kde_iconsdir/*/*/*/*
%_datadir/dbus-1/interfaces/*.xml

#--------------------------------------------------------------------

%prep
%setup -q -n %name-%version

%build
%cmake_kde4
%make

%install
rm -rf %{buildroot}
%{makeinstall_std} -C build

%find_lang %name --with-html

%clean
rm -rf %{buildroot}
