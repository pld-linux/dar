#
# Conditional build:
%bcond_without	ea		# build without support for linux extented attributes
%bcond_without	static		# build without dar_static
%bcond_without	static_libs	# don't build static libraries
#
%if %{with static}
%define with_static_libs 1
%endif
#
Summary:	dar makes backup of a directory tree and files
Summary(pl.UTF-8):	dar - narzędzie do tworzenia kopii zapasowych drzew katalogów i plików
Name:		dar
Version:	2.4.9
Release:	1
License:	GPL v2
Group:		Applications/Archiving
Source0:	http://dl.sourceforge.net/%{name}/%{name}-%{version}.tar.gz
# Source0-md5:	c7e8d6c480c068a52dc8cdfca9c5f615
Patch0:		%{name}-opt.patch
URL:		http://dar.linux.free.fr/
%{?with_ea:BuildRequires:	attr-devel >= 2.4.16-3}
BuildRequires:	autoconf >= 2.59
BuildRequires:	automake
BuildRequires:	bzip2-devel
BuildRequires:	doxygen >= 1:1.3
BuildRequires:	e2fsprogs-devel
%ifarch alpha
# ICE in 3.3.x up to 3.3.2 - require patched version
BuildRequires:	gcc-c++ >= 5:3.3.2-0.3
%endif
BuildRequires:	gettext-devel
BuildRequires:	groff
BuildRequires:	libgcrypt
BuildRequires:	libgpg-error
BuildRequires:	libstdc++-devel
BuildRequires:	libtool >= 2:1.4d
BuildRequires:	lzo-devel
BuildRequires:	openssl-devel >= 0.9.7k
BuildRequires:	zlib-devel
%if %{with static}
%{?with_ea:BuildRequires:	attr-static}
BuildRequires:	bzip2-static
BuildRequires:	glibc-static
BuildRequires:	libgcrypt-static
BuildRequires:	libgpg-error-static
BuildRequires:	libstdc++-static
BuildRequires:	lzo-static
BuildRequires:	openssl-static
BuildRequires:	zlib-static
%endif
Requires:	%{name}-libs = %{version}-%{release}
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

# don't generate `Requires' for sample scripts
%define	_noautoreq bash perl

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

%description -l pl.UTF-8
dar jest poleceniem powłoki, które tworzy kopie zapasowe drzew
katalogów i plików. Możliwości:
- Filtry: dar może tworzyć kopię zapasową całego systemu plików do
  pojedynczego pliku; mechanizm filtrów pozwala wyłączać lub dołączać
  pliki przy tworzeniu kopii lub odtwarzaniu z niej.
- Backup różnicowy: dar może tworzyć kopie pełne lub różnicowe
  (zawierające tylko te pliki, które zmieniły się od innego backupu)
- Części (slices): dar oznacza "Disk ARchive". Od początku ma
  możliwość dzielenia archiwów na różne nośniki wymienialne,
  niezależnie od ich liczby i rozmiaru (można tworzyć kopie na CD-R,
  DVD-R, CD-RW, Zip, Jazz...).
- Kompresja: domyślnie dar nie kompresuje danych; ma zaimplementowany
  algorytm gzip, jest przygotowywany do bzip2 i innych. Kompresja jest
  wykonywana przed podziałem na części.
- Bezpośredni dostęp: nawet w przypadku użycia kompresji, dar nie musi
  czytać całej kopii aby odtworzyć jeden plik. Najpierw odczytuje
  katalog, następnie skacze od razu do właściwego miejsca.
- Obsługa twardych dowiązań: dar zachowuje i odtwarza je w miarę
  możliwości; w przypadku niemożliwości wykonania dowiązania, powiela
  plik i wypisuje ostrzeżenie.
- Obsługa rozszerzonych atrybutów (zależnie od opcji kompilacji): dar
  potrafi zachowywać i odtwarzać rozszerzone atrybuty - wszystkie lub
  tylko dotyczące danej przestrzeni nazw (systemowej lub użytkownika).
- Testowanie archiwów: dzięki użyciu CRC dar wykrywa uszkodzone dane;
  tylko uszkodzone pliki nie zostaną odtworzone, reszta tak - nawet w
  przypadku użycia kompresji.
- Użycie rurek - dar może wyprodukować archiwum na standardowe wyjście
  lub do nazwanej rurki. Może także czytać archiwum z pary rurek, a
  nawet odtwarzać ze zdalnego archiwum.
- Rozdzielenie: katalog (zawartość archiwum) może być wyciągnięty do
  małego pliku, który może być używany jako odniesienie dla
  różnicowego backupu.
- Przekształcanie części istniejącego archiwum: zewnętrzny program o
  nazwie dar_xform jest w stanie zmieniać rozmiary części podanego
  archiwum. Może czytać z zestawu kawałków, standardowego wejścia lub
  nazwanej rurki.

%package static
Summary:	Static version of dar backup tool
Summary(pl.UTF-8):	Statyczna wersja archiwizatora dar
Group:		Applications

%description static
Static version of dar backup tool.

%description static -l pl.UTF-8
Statyczna wersja archiwizatora dar.

%package libs
Summary:	Shared version of dar library
Summary(pl.UTF-8):	Współdzielona wersja biblioteki dar
Group:		Libraries

%description libs
Shared version of dar library.

%description libs -l pl.UTF-8
Współdzielona wersja biblioteki dar.

%package devel
Summary:	Header files to develop dar software
Summary(pl.UTF-8):	Pliki nagłówkowe biblioteki dar
Group:		Development/Libraries
Requires:	%{name}-libs = %{version}-%{release}
%{?with_ea:Requires:	attr-devel >= 2.4.16-3}
Requires:	bzip2-devel
Requires:	libstdc++-devel
Requires:	openssl-devel
Requires:	zlib-devel

%description devel
Header files to develop software which operates on dar.

%description devel -l pl.UTF-8
Pliki nagłówkowe potrzebne do rozwoju oprogramowania korzystającego z
dara.

%package libs-static
Summary:	Static version of dar library
Summary(pl.UTF-8):	Statyczna wersja biblioteki dar
Group:		Development/Libraries
Requires:	%{name}-devel = %{version}-%{release}

%description libs-static
Static version of dar library.

%description libs-static -l pl.UTF-8
Statyczna wersja biblioteki dar.

%package doc
Summary:	dar - documentation
Summary(pl.UTF-8):	dar - dokumentacja
Group:		Documentation
Requires:	%{name} = %{version}-%{release}

%description doc
Dar ducumentation.

%description doc -l pl.UTF-8
Dokumentacja dla dar.

%prep
%setup -q
%patch0 -p1

%build
%{__gettextize}
%{__libtoolize}
%{__aclocal}
%{__autoconf}
%{__autoheader}
%{__automake}
%configure \
	%{!?with_ea:--disable-ea-support} \
	%{!?with_static:--disable-dar-static} \
	--enable-static=%{?with_static_libs:yes}%{!?with_static_libs:no} \
	--enable-mode=64 \
	--disable-upx
%{__make}

%install
rm -rf $RPM_BUILD_ROOT
%{?with_static:install -d $RPM_BUILD_ROOT/bin}

%{__make} install \
	DESTDIR=$RPM_BUILD_ROOT

%{?with_static:mv -f $RPM_BUILD_ROOT{%{_bindir},/bin}/dar_static}

ln -sf %{_datadir}/%{name} misc/doc

%find_lang %{name}

%clean
rm -rf $RPM_BUILD_ROOT

%post	libs -p /sbin/ldconfig
%postun	libs -p /sbin/ldconfig

%files -f %{name}.lang
%defattr(644,root,root,755)
%doc ChangeLog NEWS README THANKS TODO misc/doc
%dir %{_datadir}/%{name}
%attr(755,root,root) %{_bindir}/*
%{_mandir}/man1/*.1*
%attr(644,root,root) %config(noreplace) %verify(not md5 mtime size) /etc/darrc

%files libs
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/libdar64.so.*.*.*

%files devel
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/libdar64.so
%{_libdir}/libdar64.la
%{_includedir}/dar
%{_pkgconfigdir}/libdar64.pc

%if %{with static}
%files static
%defattr(644,root,root,755)
%attr(755,root,root) /bin/*
%endif

%if %{with static_libs}
%files libs-static
%defattr(644,root,root,755)
%{_libdir}/libdar64.a
%endif

%files doc
%defattr(644,root,root,755)
%{_datadir}/%{name}/*
