#
# Conditional build:
%bcond_without	ea		# build without support for linux extented attributes
%bcond_without	static	# build without dar_static
#
Summary:	dar makes backup of a directory tree and files
Summary(pl):	dar - narzêdzie do tworzenia kopii zapasowych drzew katalogów i plików
Name:		dar
Version:	2.1.4
Release:	1
License:	GPL v2
Group:		Applications
Source0:	http://dl.sourceforge.net/%{name}/%{name}-%{version}.tar.gz
# Source0-md5:	032306021f6a66ef060260acd39da3dd
Patch0:		%{name}-opt.patch
URL:		http://dar.linux.free.fr/
%{?with_ea:BuildRequires:	attr-devel >= 2.4.16-3}
BuildRequires:	autoconf >= 2.59
BuildRequires:	automake
BuildRequires:	bzip2-devel
%ifarch alpha
# ICE in 3.3.x up to 3.3.2 - require patched version
BuildRequires:	gcc-c++ >= 5:3.3.2-0.3
%endif
BuildRequires:	libstdc++-devel
BuildRequires:	libtool >= 2:1.4d
BuildRequires:	zlib-devel
%if %{with static}
%{?with_ea:BuildRequires:	attr-static}
BuildRequires:	bzip2-static
BuildRequires:	glibc-static
BuildRequires:	libstdc++-static
BuildRequires:	zlib-static
%endif
Requires:	%{name}-libs = %{version}-%{release}
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
dar is a shell command, that makes backup of a directory tree and
files.

FILTERS: dar is able to backup from total file system to a single
file. Additionally a mechanism of filters permits, based on the
filename, to exclude or include some files while backing up or
restoring a directory tree. In the other side, a secondary filter
mechanism permits to exclude some branches of a directory tree, or to
only include some branches.

DIFFERENTIAL BACKUP: When making a backup with dar, you have the
possibility to make a full backup or a differential backup. A full
backup, as expected makes backup of all files as specified on the
command line (with or without filters). Instead, a differential
backup, (over filter mechanism), saves only files that have changed
since a given reference backup. Additionally, files that existed in
the reference backup and which do no more exist at the time of the
differential backup are recorded in the backup. At recovery time,
(unless you deactivate it), restoring a differential backup will
update changed files and new files, but also remove files that have
been recorded as deleted. Note that the reference backup can be a full
backup or another differential backup. This way you can make a first
full backup, then many differential backup, each taking as reference
the last backup made.

SLICES: Dar stands for Disk ARchive. From the beginning it was
designed to be able to split an archive over several removable media
whatever their number is and whatever their size is. Thus dar is able
to save over old floppy disk, CD-R, DVD-R, CD-RW, DVD-RW, Zip, Jazz,
etc... Dar is not concerned by un/mounting a removable medium, instead
it is independent of hardware. Given the size, it will split the
archive in several files (called SLICES), eventually pausing before
creating the next one, allowing this way, the user to un/mount a
medium, burn the file on CD-R, send it by email (if your mail system
does not allow huge file in emails, dar can help you here also). By
default, (no size specified), dar will make one slice whatever its
size is. Additionally, the size of the first slice can be specified
separately, if for example you want first to fulfil a partially filled
disk before starting using empty ones. Last, at restoration time, dar
will just pause and prompt the user asking a slice only if it is
missing.

COMPRESSION: last, dar can use compression. By default no compression
is used. Actually only gzip algorithm is implemented, but some room
has been done for bzip2 and any other compression algorithm. Note
that, compression is made before slices, which means that using
compression with slices, will not make slices smaller, but will
probably make less slices in the backup.

DIRECT ACCESS: even using compression dar has not to read the whole
backup to extract one file. This way if you just want to restore one
file from a huge backup, the process will be much faster than using
tar. Dar first reads the catalogue (i.e. the contents of the backup),
then it goes directly to the location of the saved file(s) you want to
restore and proceed to restoration. In particular using slices dar
will ask only for the slice(s) containing the file(s) to restore.

HARD LINK CONSIDERATION: hard links are now properly saved. They are
properly restored if possible. If for example restoring across a
mounted filesystem, hard linking will fail, but dar will then
duplicate the inode and file content, issuing a warning.

EXTENDED ATTRIBUTES: support for extended attributes have to be
activated at compilation time (see INSTALL). Dar is able to save and
restore EA, all or just those of a given namespace (system or user).
If no EA have been saved and restoration occurs over a file that has
EA, they will be preserved. But if they have been saved empty for a
given file, any existing EA for that file will be removed at
restoration time, unless -u and/or -U is given on command-line.

ARCHIVE TESTING thanks to CRC (cyclic redundancy checks), dar is able
to detect data corruption in the archive. Only the file where data
corruption occurred will not be possible to restore, but dar will
restore the other even when compression is used.

USING PIPES dar is now able to produce an archive to its standard
output or named pipe. it is also able to read an archive through a
pair of pipes, to take a remote archive as reference, or even to
restore data from a remote archive. This way it is now possible to
store an archive remotely and in total security (if using encrypted
means)

ISOLATION the catalogue (i.e.: the contents of an archive), can be
extracted (this operation is called isolation) to a small file, that
can in turn be used as reference for differential archive. There is no
more need to provide an archive to be able to create a differential
backup over it, just its catalogue is necessary.

RE-SHAPE SLICES OF AN EXISTING ARCHIVE the external program named
"dar_xform" is able to change the size of slices of a given archive.
The resulting archive is totally identical to archives directly
created by dar. Source archive can be taken from a set of slice, from
standard input or even a named pipe.

%description -l pl
dar jest poleceniem pow³oki, które tworzy kopie zapasowe drzew
katalogów i plików. Mo¿liwo¶ci:
- Filtry: dar mo¿e tworzyæ kopiê zapasow± ca³ego systemu plików do
  pojedynczego pliku; mechanizm filtrów pozwala wy³±czaæ lub do³±czaæ
  pliki przy tworzeniu kopii lub odtwarzaniu z niej.
- Backup ró¿nicowy: dar mo¿e tworzyæ kopie pe³ne lub ró¿nicowe
  (zawieraj±ce tylko te pliki, które zmieni³y siê od innego backupu)
- Czê¶ci (slices): dar oznacza "Disk ARchive". Od pocz±tku ma
  mo¿liwo¶æ dzielenia archiwów na ró¿ne no¶niki wymienialne,
  niezale¿nie od ich liczby i rozmiaru (mo¿na tworzyæ kopie na CD-R,
  DVD-R, CD-RW, Zip, Jazz...).
- Kompresja: domy¶lnie dar nie kompresuje danych; ma zaimplementowany
  algorytm gzip, jest przygotowywany do bzip2 i innych. Kompresja jest
  wykonywana przed podzia³em na czê¶ci.
- Bezpo¶redni dostêp: nawet w przypadku u¿ycia kompresji, dar nie musi
  czytaæ ca³ej kopii aby odtworzyæ jeden plik. Najpierw odczytuje
  katalog, nastêpnie skacze od razu do w³a¶ciwego miejsca.
- Obs³uga twardych dowi±zañ: dar zachowuje i odtwarza je w miarê
  mo¿liwo¶ci; w przypadku niemo¿liwo¶ci wykonania dowi±zania, powiela
  plik i wypisuje ostrze¿enie.
- Obs³uga rozszerzonych atrybutów (zale¿nie od opcji kompilacji): dar
  potrafi zachowywaæ i odtwarzaæ rozszerzone atrubuty - wszystkie lub
  tylko dotycz±ce danej przestrzeni nazw (systemowej lub u¿ytkownika).
- Testowanie archiwów: dziêki u¿yciu CRC dar wykrywa uszkodzone dane;
  tylko uszkodzone pliki nie zostan± odtworzone, reszta tak - nawet w
  przypadku u¿ycia kompresji.
- U¿ycie rurek - dar mo¿e wyprodukowaæ archiwum na standardowe wyj¶cie
  lub do nazwanej rurki. Mo¿e tak¿e czytaæ archiwum z pary rurek, a
  nawet odtwarzaæ ze zdalnego archiwum.
- Rozdzielenie: katalog (zawarto¶æ archiwum) mo¿e byæ wyci±gniêty do
  ma³ego pliku, który mo¿e byæ u¿ywany jako odniesienie dla
  ró¿nicowego backupu.
- Przekszta³canie czê¶ci istniej±cego archiwum: zewnêtrzny program o
  nazwie dar_xform jest w stanie zmieniaæ rozmiary czê¶ci podanego
  archiwum. Mo¿e czytaæ z zestawu kata³ków, standardowego wej¶cia lub
  nazwanej rurki.

%package static
Summary:	Static version of dar backup tool
Summary(pl):	Statyczna wersja archiwizatora dar
Group:		Applications

%description static
Static version of dar backup tool.

%description static -l pl
Statyczna wersja archiwizatora dar.

%package libs
Summary:	Shared version of dar library
Summary(pl):	Wspó³dzielona wersja biblioteki dar
Group:		Libraries

%description libs
Shared version of dar library.

%description libs -l pl
Wspó³dzielona wersja biblioteki dar.

%package devel
Summary:	Header files to develop dar software
Summary(pl):	Pliki nag³ówkowe biblioteki dar
Group:		Development/Libraries
Requires:	%{name}-libs = %{version}-%{release}

%description devel
Header files to develop software which operates on dar.

%description devel -l pl
Pliki nag³ówkowe potrzebne do rozwoju oprogramowania korzystaj±cego z
dara.

%package libs-static
Summary:	Static version of dar library
Summary(pl):	Statyczna wersja biblioteki dar
Group:		Development/Libraries
Requires:	%{name}-devel = %{version}-%{release}

%description libs-static
Static version of dar library.

%description libs-static -l pl
Statyczna wersja biblioteki dar.

%prep
%setup -q
%patch -p1

%build
%{__libtoolize}
%{__aclocal}
%{__autoconf}
%{__autoheader}
%{__automake}
%configure \
	%{?with_ea:--enable-ea-support} \
	%{!?with_static:--disable-dar-static} \
	--disable-upx
%{__make}

%install
rm -rf $RPM_BUILD_ROOT
%{?with_static:install -d $RPM_BUILD_ROOT/bin}

%{__make} install \
	DESTDIR=$RPM_BUILD_ROOT

%{?with_static:mv -f $RPM_BUILD_ROOT{%{_bindir},/bin}/dar_static}

find $RPM_BUILD_DIR/%{name}-%{version}/doc -name "Makefile*" | xargs rm -fv

%clean
rm -rf $RPM_BUILD_ROOT

%post	libs -p /sbin/ldconfig
%postun	libs -p /sbin/ldconfig

%files
%defattr(644,root,root,755)
%doc BUGS README TODO doc
%attr(755,root,root) %{_bindir}/*
%{_datadir}/%{name}
%{_mandir}/man1/*

%files libs
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/libdar.so.*.*.*

%files devel
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/libdar.so
%{_libdir}/libdar.la
%{_includedir}/dar

%if %{with static}
%files static
%defattr(644,root,root,755)
%attr(755,root,root) /bin/*
%endif

%files libs-static
%defattr(644,root,root,755)
%{_libdir}/libdar.a
