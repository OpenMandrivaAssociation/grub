%define with_gcc_42 0
%define _default_patch_fuzz 2

Summary:	GRand Unified Bootloader
Name:		grub
Version:	0.97
Release:	39
URL:		http://www.gnu.org/software/grub/
Source0:	ftp://alpha.gnu.org/gnu/grub/%{name}-%{version}.tar.gz
Source2:	menu.lst.example

# Mandriva patches
Patch10000:	grub-0.5.96.1-ezd.patch
Patch10001:	grub-0.97-gcc4_warnings.patch
Patch10005:	grub-0.95-eltorito.patch
Patch10007:	grub-0.91-nice-magic.patch
Patch10009:	grub-0.95-mem_lower.patch
Patch10015:	grub-0.97-install_sh.patch
Patch10016:	grub-0.97-reiser4.patch
Patch10018:	grub-0.97-please-automake--add-AM_PROG_AS.patch

# gfxboot patch from SuSE
Patch10017:	grub-gfxmenu-v8.diff

# handle the now default ext3 format (from debian which took it from fedora)
Patch1:		grub-ext3-256byte-inode.patch

# fedora patches
Patch22:	grub-0.94-addsyncs.patch
Patch23:	0002-Add-strspn-strcspn-and-strtok_r.patch
Patch24:	0003-Allow-passing-multiple-image-files-to-the-initrd-com.patch
Patch25:	grub-ext4-support.patch

# patches 100-199 are for features proposed but not accepted upstream
# add support for appending kernel arguments
#XXX patch below conflicts with our graphics patch
#Patch100: grub-0.90-append.patch
# add support for lilo -R-esque select a new os to boot into
Patch101:	grub-0.97-once.patch
Patch102:	grub-0.97-once-info-doc.patch

# patches 500+ are for miscellaneous little things
# support for non-std devs (eg cciss, etc)
Patch500:	grub-0.93-special-device-names.patch
# i2o device support
Patch501:	grub-0.94-i2o.patch
# detect cciss/ida/i2o
Patch502:	grub-0.95-moreraid.patch

# for some reason, using the initrd max part of the setup.S structure
# causes problems on x86_64 and with 4G/4G
Patch505:	grub-0.94-initrdmax.patch

# we need to use O_DIRECT to avoid hitting oddities with caching
Patch800:	grub-0.95-odirect.patch

# odirect actually causes problem (open returns EINVAL) with gfxboot
# install of grub in a file (e.g. preview mode under qemu)
Patch801:	grub-0.97-odirect-on-device-only.patch

# the 2.6 kernel no longer does geometry fixups.  so now I get to do it
# instead in userspace everywhere.  
Patch1000:	grub-0.95-geometry-26kernel.patch

# Support for booting from a RAID1 device
Patch1100:	grub-0.95-md.patch
Patch1101:	grub-0.97-md-rework--mdv-adapted.patch

# Mark the simulation stack executable
# (otherwise grub segfaults on x86_64 which uses "noexec")
Patch1104:	grub-0.97-nxstack.patch
Patch1105:	grub-0.97-nx-multiinstall.patch

# always use a full path for mdadm.
Patch1110:	grub-0.97-mdadm-path.patch
# always install into the mbr if we're on a raid1 /boot.
Patch1111:	grub-0.95-md-mbr.patch

# gcc4 fixes.
#XXX patch below conflicts with our graphics patch
#Patch1115: grub-0.97-gcc4.patch

# Make non-MBR installs work again on non-raid1.
Patch1120:	grub-0.95-nonmbr.patch

# Make "grub-install --recheck" look like the menace it is.
Patch1130:	grub-0.95-recheck-bad.patch

# Fix missing prototypes, since grub nicely sets -Wmissing-prototypes and
# then tries to build conftests without them.
Patch1135:	grub-0.97-prototypes.patch

# install correctly on dmraid devices
Patch1145:	grub-0.97-dmraid.patch
Patch1146:	grub-0.97-dmraid-recheck-bad--mdv-adapted.patch
Patch1147:	grub-0.97-dmraid-partition-names.patch

# fix mactel keyboard bugs
Patch1148:	grub-0.97-mactel-kbd.patch

# fix error reporting
#XXX not very important, and would need adaptation, skipping
#Patch1149: grub-0.97-stderr.patch

# fix grub-install to notice mpath partitions
Patch1150:	grub-0.97-mpath.patch

# fix grub-install to notice virtio partitions (from fedora)
Patch1154:	grub-0.97-virtio-support.patch

# (from ubuntu) (nb: needed for grub-uuid.diff)
Patch1151:	grub-varargs.diff
# (from ubuntu) (nb: needed for grub-uuid.diff)
Patch1152:	grub-gpt.diff

# (from ubuntu)
# note that uuid support is partial (only in menu.lst), stage2 & menu.lst are
# still accessed through (hdX,Y)
# 
# pros of using uuid in menu.lst:
# - menu.lst hd0/hd1 independance.
#   this is mostly useful when menu.lst is read through "configfile"
# missing feature:
# - partition renumbering will still break boot if install.sh is not modified
#  (since install.sh can't use uuid)
# 
# anyway, this patch is useful to have even unused, since it allows
# "configfile" to handle ubuntu's menu.lst
Patch1153:	grub-uuid.diff

# grub patch for dealing with build-id objheader inserted into stage1/2 files 
Patch1155:	grub-0.97-grub-build-id.patch

License:	GPL
Group:		System/Kernel and hardware
BuildRequires:	autoconf2.5
BuildRequires:	automake1.8
%if %{with_gcc_42}
BuildRequires:	gcc4.2
%endif
BuildRequires:	glibc-static-devel
BuildRequires:	libgpm-devel
BuildRequires:	pkgconfig(ncurses)
#BuildRequires:	tetex-dvips
#BuildRequires:	tetex-latex
#BuildRequires:	texinfo
Exclusivearch:	%ix86 x86_64 amd64 ia32e

Provides:	bootloader

%description
GRUB is a GPLed bootloader intended to unify bootloading across x86
operating systems.  In addition to loading the Linux and *BSD kernels,
it implements the Multiboot standard, which allows for flexible loading
of multiple boot images (needed for modular kernels such as the GNU
Hurd).

%prep
%setup -q

%patch1 -p1 -b .256byte-inode
%patch22 -p1 -b .addsync
%patch23 -p1 -b .string-functions
%patch24 -p1 -b .multiple-initrd
%patch25 -p1 -b .ext4

%patch101 -p1 -b .bootonce
%patch102 -p1 -b .bootonce-doc -z .pix

%patch500 -p1 -b .raid
%patch501 -p1 -b .i2o
%patch502 -p1 -b .moreraid

%patch505 -p1 -b .initrdmax

%patch800 -p1 -b .odirect
%patch801 -p1 -b .odirect-on-device-only

%patch1000 -p1 -b .26geom

%patch1100 -p1 -b .md
%patch1101 -p1 -b .md-rework

%patch1104 -p1 -b .nxstack
%patch1105 -p1 -b .nx-multiinstall

%patch1110 -p1 -b .mdadm-path
%patch1111 -p1 -b .md-mbr

%patch1120 -p1 -b .nonmbr

%patch1130 -p1 -b .recheck-bad

%patch1135 -p1 -b .prototypes

%patch1145 -p1 -b .dmraid
%patch1146 -p1 -b .dmraid-recheck-bad
%patch1147 -p1 -b .dmraid-partition-names

%patch1148 -p1 -b .mactel-kbd

%patch1150 -p1 -b .mpath
%patch1154 -p1 -b .virtio

%patch1151 -p1 -b .varargs
%patch1152 -p1 -b .gpt
%patch1153 -p1 -b .uuid
%patch1155 -p1

%patch10000 -p1
%patch10001 -p1
%patch10005 -p1
%patch10007 -p1
%patch10009 -p1
%patch10015 -p1
#%#patch10016 -p1
%patch10018 -p1

%patch10017 -p0

%build
# force building grub.info from grub.texi (since patches do not edit both)
# rm docs/grub.info

# automake 1.11.2
perl -pi -e 's|pkglib_|pkgdata_|g;' stage{1,2}/Makefile.{am,in}
autoreconf

#<akdengi> New binutils with gold failed in adress check 7C00, 8000.
#sed -e "s/for link_addr in 2000 8000 7C00/for link_addr in 2000/" -i configure

CFLAGS="-Os -static -g -fno-strict-aliasing -fno-stack-protector -fno-reorder-functions -Wl,--build-id=none -fuse-ld=bfd" \
./configure --build=%{_target_platform} \
	    --host=%{_host} \
	    --target=%{_target} \
	    --prefix=%{_prefix} \
	    --exec-prefix=/ \
	    --bindir=%{_bindir} \
	    --mandir=%{_mandir} \
	    --infodir=%{_infodir} \
	    --datadir=/lib/grub/%{_arch}-%{_vendor} \
	    --disable-auto-linux-mem-opt
%make pkgdatadir=/lib/grub/%{_arch}-%{_vendor}

%install
rm -rf %{buildroot}
%makeinstall_std pkgdatadir=/lib/grub/%{_arch}-%{_vendor}
rm -f %{buildroot}/%{_infodir}/dir
install -d %{buildroot}/boot/grub
install -m 0644 %{SOURCE2} %{buildroot}/boot/grub

%post

if [ -f /boot/grub/install.sh ]; then
	if [ -x /usr/sbin/detectloader ]; then
		LOADER=$(/usr/sbin/detectloader)
		if [ "$LOADER" = "GRUB" ]; then
			for file in /lib/grub/%{_arch}-%{_vendor}/*stage*; do
				cp -f $file /boot/grub/ || :
			done
			sh /boot/grub/install.sh > /dev/null
		fi
	fi
elif [ -e /boot/grub/menu.lst -a -e /boot/grub/stage2 ]; then
    # no install.sh, trying to get one

    # look for the device
    for DEVICE in `awk '{print "/dev/" $4}' /proc/partitions`; do
	if [ -b $DEVICE ]; then
	    echo "trying $DEVICE"
	    if /bin/dd if=$DEVICE bs=512 count=1 2>/dev/null | /bin/grep -q GRUB; then
		if [ -z "$BOOT" ]; then
		    BOOT=$DEVICE
		else
		    echo "oops, GRUB found on both $DEVICE and $BOOT"
		fi
	    fi
	fi
    done

    if [ -n "$BOOT" ]; then
	echo "installing grub on $BOOT"
	grub-install $BOOT
    else
	echo "can not find where GRUB is installed"
    fi
fi

%preun
# What a hack hell... we need this things because of upgrading from
# previous grub versions. The problem is that previous grub packages
# remove the stage files from /boot/grub in some cases, making the
# system unbootable.
%triggerun -- grub <= 0.97-1mdk
mkdir -p /boot/grub/backup_stagefiles
mv /boot/grub/*stage* /boot/grub/backup_stagefiles/ >/dev/null 2>&1 || :

# Replicate post script code here, because the trigger scripts are
# executed only after post script of this new package, and old
# install.sh was used then. So we need to execute again to use the new
# generated install.sh script.
if [ -f /boot/grub/install.sh ]; then
	if [ -x /usr/sbin/detectloader ]; then
		LOADER=$(/usr/sbin/detectloader)
		if [ "$LOADER" = "GRUB" ]; then
			for file in /lib/grub/%{_arch}-%{_vendor}/*stage*; do
				cp -f $file /boot/grub/ || :
			done
			sh /boot/grub/install.sh > /dev/null
		fi
	fi
fi

%triggerpostun -- grub <= 0.97-1mdk
if [ -d /boot/grub/backup_stagefiles ]; then
	for file in /boot/grub/backup_stagefiles/*stage*; do
		if [ ! -f "/boot/grub/`basename $file`" ]; then
			mv $file /boot/grub/ || :
		else
			rm -f $file;
		fi
	done
	rmdir /boot/grub/backup_stagefiles > /dev/null || :
fi

%files
%defattr(0644,root,root,0755)
/boot/grub
%{_infodir}/*
%{_mandir}/*/*
/lib/grub
%defattr(0755,root,root,0755)
%{_bindir}/mbchk
/sbin/grub*


%changelog
* Mon Oct 1 2012 Alexander Kazancev <akdengi> 0.97-38
- add CCFLAG -fuse-ld=bfd to build with gold default linker
- drop DOC package
- drop tetex requirements

* Wed Jun 13 2012 Andrey Bondrov <abondrov@mandriva.org> 0.97-37
+ Revision: 805368
- Fix BuildRequires
- Drop some legacy junk

* Fri Jan 27 2012 Paulo Andrade <pcpa@mandriva.com.br> 0.97-36
+ Revision: 769246
- Link /sbin/grub statically.
- Correct build with newer automake.

* Wed Jun 08 2011 Paulo Andrade <pcpa@mandriva.com.br> 0.97-35
+ Revision: 683118
- Correct problem with gfxboot qemu preview with grub installed in a mapped file
- Test build using gcc 4.2

* Tue May 10 2011 Paulo Andrade <pcpa@mandriva.com.br> 0.97-34
+ Revision: 673383
- Add extra option to generate a proper stage1/stage2 with gcc 4.6.0

* Tue May 10 2011 Antoine Ginies <aginies@mandriva.com> 0.97-33
+ Revision: 673345
- fix 'GRUB requires a working absolute objcopy error'

  + Oden Eriksson <oeriksson@mandriva.com>
    - mass rebuild

* Thu Dec 02 2010 Oden Eriksson <oeriksson@mandriva.com> 0.97-31mdv2011.0
+ Revision: 605500
- rebuild

  + Sergio Rafael Lemke <sergio@mandriva.com>
    - updated the grub example file

* Wed Mar 17 2010 Oden Eriksson <oeriksson@mandriva.com> 0.97-30mdv2010.1
+ Revision: 522745
- rebuilt for 2010.1

* Tue Sep 15 2009 Frederic Crozat <fcrozat@mandriva.com> 0.97-29mdv2010.0
+ Revision: 443129
- Change CFLAGS to disable stack protector (since gfxboot is tweaking stack and can crash it with protector enabled). Use -Os, used by Fedora since 2002.

* Tue Sep 08 2009 Frederic Crozat <fcrozat@mandriva.com> 0.97-28mdv2010.0
+ Revision: 433833
- Replace ext4 patch with the one from Fedora
- Patches 23 / 24: allow to specify multiple initrd on a single boot

* Thu Aug 27 2009 Christophe Fergeau <cfergeau@mandriva.com> 0.97-27mdv2010.0
+ Revision: 421698
- add fedora patch to support virtio partitions, fix #52397

* Mon Jan 12 2009 Pixel <pixel@mandriva.com> 0.97-25mdv2009.1
+ Revision: 328578
- add patches from ubuntu:
  o add support for "uuid xxx" instead of "root (hdX,Y)"
  o add support GPT (from Marco Gerards)
  o add patch "varargs" (since some changes are used by uuid patch)

* Wed Aug 06 2008 Thierry Vignaud <tv@mandriva.org> 0.97-24mdv2009.0
+ Revision: 264611
- rebuild early 2009.0 package (before pixel changes)

* Thu Jun 05 2008 Pixel <pixel@mandriva.com> 0.97-23mdv2009.0
+ Revision: 215186
- ext4 extents support from Quentin Godfroy (Olivier Lahaye, #41227)

* Wed Feb 06 2008 Pixel <pixel@mandriva.com> 0.97-22mdv2008.1
+ Revision: 163119
- handle ext3 256 bytes inode, which is the default
- use autoreconf
- add patch to help automake

  + Thierry Vignaud <tv@mandriva.org>
    - rebuild
    - kill re-definition of %%buildroot on Pixel's request

  + Olivier Blin <blino@mandriva.org>
    - restore BuildRoot

* Mon Apr 23 2007 Pixel <pixel@mandriva.com> 0.97-20mdv2008.0
+ Revision: 17203
- remove existing savedefault documentation
  (since bootonce patch breaks it)
- adapt bootonce documentation to the bootonce patch we use
- ensure grub.info is rebuilt from grub.texi


* Tue Dec 05 2006 Pixel <pixel@mandriva.com> 0.97-20mdv2007.0
+ Revision: 90997
- replace splashimage patch with gfxboot patch
- drop chainboot patch (it conflicts)

  + Olivier Blin <oblin@mandriva.com>
    - do not show package release in version string, it makes it appear over two lines on top of the menu

* Wed Sep 06 2006 Pixel <pixel@mandriva.com> 0.97-18mdv2007.0
+ Revision: 60006
- our default splashimage is now /boot/grub/splash.xpm.gz, mandriva-theme will modify that file according to the theme

* Sat Aug 12 2006 Pixel <pixel@mandriva.com> 0.97-17mdv2007.0
+ Revision: 55630
- fedora nx patches fix grub segfaulting on x86_64 (#24105)
- add a whole bunch of patches from fedora (2 of them needed applying by hand and rediffing)
- remove our special-device-names patch, using fedora ones instead
- adapted patch install_sh
- moved mandriva patches from 1..15 to 10000..10015
- use %%makeinstall_std
- import grub-0.97-17mdk

* Fri Feb 03 2006 Pixel <pixel@mandriva.com> 0.97-17mdk
- drop reiser4 patch since it breaks

* Thu Feb 02 2006 Pixel <pixel@mandriva.com> 0.97-16mdk
- add BuildRequires: texinfo
- add reiser4 support (though no BuildRequires yet on reiser4progs-devel which is in contrib)
  (thanks to Lukas Oboril <xxlucas@seznam.cz>)

* Tue Jan 24 2006 Pixel <pixel@mandriva.com> 0.97-15mdk
- don't use old gcc 3.3 anymore (it works nicely with gcc 4)
- use mkrel
- drop non working "once" patch

* Mon Jan 23 2006 Pixel <pixel@mandriva.com> 0.97-14mdk
- don't set CFLAGS to optflags
  (when testing objcopy in configure, option -fasynchronous-unwind-tables causes failure)
- add "once" patch from fedora patch:
  add support for lilo -R-esque select a new os to boot into

* Tue Sep 13 2005 Pixel <pixel@mandriva.com> 0.97-13mdk
- search the boot drive and call grub-install
  when there is no install.sh but a menu.lst and a stage2 (for upgrading conectiva)
  (the previous condition was checking device.map, but there is none)
  (maybe we could use /root/tmp/mi/grubcmd...)

* Fri Sep 09 2005 Pixel <pixel@mandriva.com> 0.97-12mdk
- allow /boot to be mounted noexec (using "sh /boot/grub/install.sh") (#17935)

* Fri Sep 02 2005 Pixel <pixel@mandriva.com> 0.97-11mdk
- patch grub-install to generate /boot/grub/install.sh 
- add code in %%post to search the boot drive and call grub-install
  when there is no install.sh but a device.map (for upgrading conectiva)
- remove code modifying existing install.sh
  (sometimes it's better not using "setup" for explictly not using stage1.5,
   for eg. when you use partimage or similar tools which don't save those sectors)

* Tue Aug 16 2005 Herton Ronaldo Krzesinski <herton@mandriva.com> 0.97-10mdk
- Added %%post and %%preun requires for info-install (ticket #17418).

* Sat Aug 06 2005 Herton Ronaldo Krzesinski <herton@mandriva.com> 0.97-9mdk
- Before using perl script to update /boot/grub/install.sh inside
  %%triggerun, we check if the file exists. Also, all output redirected
  to /dev/null as it isn't useful.

* Fri Jul 15 2005 Herton Ronaldo Krzesinski <herton@mandriva.com> 0.97-8mdk
- Revert back change "Replaced /lib references to /%%{_lib}", as Gwenole
  Beauchesne reported it's unlikely we'll have a 64 bits bootloader and could
  cause problems with scripts using /lib in a hardcoded way.

* Thu Jul 14 2005 Herton Ronaldo Krzesinski <herton@mandriva.com> 0.97-7mdk
- Finally fix BuildRequires of gpm and ncurses packages, had forgot to
  fix this.
- Updated bootsplash image, new Mandrivas's wallpaper.
- Replaced /lib references to /%%{_lib}.

* Thu Jul 14 2005 Herton Ronaldo Krzesinski <herton@mandriva.com> 0.97-6mdk
- Escape '$' symbols at embedded perl script inside triggerun script,
  otherwise they get interpreted as shell variables and doesn't work as
  intended.

* Wed Jul 13 2005 Herton Ronaldo Krzesinski <herton@mandriva.com> 0.97-5mdk
- Added athlon 64 architectures to Exclusive Archs, grub also works on
  them (reported by Thierry Vignaud).
- In trigger scripts, do not use cp to copy stage files, instead use mv,
  to avoid problems with grub not finding them on boot because of changed
  inodes and improved trigger script to remove files not used (reported
  by Pascal Rigaux).

* Tue Jun 21 2005 Herton Ronaldo Krzesinski <herton@mandriva.com> 0.97-4mdk
- Compiling grub with gcc 3.3, I'm getting some errors still when trying
  to boot from a root reiserfs partition, will continue to investigate
  this but for now just using a older gcc to not leave grub broken. Also
  readding use of optflags doesn't causes problems.
- Remove /boot/grub/backup_stagefiles after upgrading from grub
  versions prior to 0.97-1mdk, as suggested by Pixel.
- Pass build/host options etc. to configure script.
- Update stage files on /boot/grub (copy them from /lib/grub to
  /boot/grub) because setup command inside /boot/grub/install.sh needs
  this and doesn't copy automatically the stage files (grub-install also
  does this).

* Sat Jun 18 2005 Herton Ronaldo Krzesinski <herton@mandriva.com> 0.97-3mdk
- Readded back previous %%post code, now install.sh from drakboot is
  generated correctly. Removed related Requires(post) too.
- Fix expansion of %%{buildroot} tag on previous changelog entry.

* Tue May 31 2005 Herton Ronaldo Krzesinski <herton@mandriva.com> 0.97-2mdk
- Updated BuildRequires, removed tetex and added tetex-latex/tetex-dvips
  (needed for building ps documentation, they already requires tetex).
- Do not use configure macro (instead call configure directly), because
  it sets gcc flags that are breaking grub when compiling with gcc 4.0 in some
  cases (grub can't boot from a root reiserfs partition because can't load
  kernel, displaying the error "Invalid or unsupported executable
  format", for example, disabling the default gcc flags and reinstalling
  grub seems to fix the problem).
- Replaced $RPM_BUILD_ROOT by %%{buildroot}.
- Moved back text documentation files to subpackage doc.
- Added back mbchk to package.
- Removed grub-install patch: it is better to install stage files in /lib,
  and with this we don't need the patch anymore, keeping compatibility
  with cases where /usr reside in another partition. This also prevents
  that with a new grub release we must update or check grub-install for
  errors and update this patch. Another problem that I experienced with
  stage files installed in /boot/grub is that grub-install itself
  updates these files on each run, and this causes conflicts because grub
  then doesn't have anymore the original stage file from the package,
  sometimes complaining that /boot/grub/stage2 file isn't valid.
- Redid graphics patch: fixed gcc4 warnings, other fixes on code to be
  more robust.
- Redid chainboot patch: fixed gcc4 warnings.
- Added to post section more code to detect and upgrade grub.
- Added patch gcc4_warnings, fixing most of gcc4 compiling warnings.
- Added trigger scripts to handle upgrading from previous grub packages
  (the /boot/grub/*stage* files are removed causing the next boot fail
  with Error 15).

* Mon May 30 2005 Herton Ronaldo Krzesinski <herton@mandriva.com> 0.97-1mdk
- New upstream version: 0.97.
- Making sure that we're using automake and aclocal 1.9, by explicitly calling
  them (without using the binaries from alternatives).
- Reenabled building of documentation files.
- Redid graphics patch: updated to new grub version and removed redundant .orig
  files inside it.
- Renamed graphics_info patch to graphics-chainboot_info to reflect better its
  contents.
- Removed gcc4 patch, applied upstream.
- Fix bug in src.rpm: menu.lst.example wasn't included into the source rpm file.
- Installing additional files (README etc.).
- Added explicitly permission modes on files section (spec).

* Tue May 24 2005 Herton Ronaldo Krzesinski <herton@mandriva.com> 0.96-1mdk
- New upstream version: 0.96.
- Added menu.lst.example file, showing a default configuration as
  example, placed in /boot/grub.
- Added gcc4 patch, fix compilation issues with gcc 4.0.
- Removed init-config-end--prepatch, does nothing.
- Removed robust and fallback-entryno patches, already applied
  upstream.
- Added mdvversion patch, to show release of the package on boot menu,
  spec updated accordingly.
- Added a more complete special-raid-devices patch.
- Removed grub-0.90-grub-install patch file, there is another patch
  grub-0.96-grub-install that does the same thing.
- Removed uneeded compatibility patches, grub just ignore these
  options if they still exists: i18n-messages-and-keytable2,
  altconfigfile-deprecated.
- Added addsyncs patch from Fedora.
- Replaced graphics with a better one, fixes graphical mode bugs, add
  additional opptions (viewport - move drawing of characters and border,
  shade - add shadow for letters). Added also updated info files
  (graphics_info patch), removed splashimagehelp patch.
- Added chainboot patch: this adds chainboot option to grub. Chainboot
  is useful for bootable cdroms for example, where after the timeout
  instead of booting from the cdrom boot from first hard disk.
- Added eltorito patch: fix various issues with grub implementation of
  eltorito non-emulation boot support.
- Replaced geometry-26kernel patch with a better one without bugs (the
  current patch makes grub to display the message "Unable to read
  partition table entry: Invalid Format" when writing mba of a disk for
  example (to reproduce, try with old release 8mdk the command
  grub-install /dev/hda)
- Added mem_lower patch.
- Added odirect patch from Fedora.
- Added a simple splash image, based on current Mandriva wallpaper.
- Spec changed accordingly patches/issues fixed.

* Wed Mar 09 2005 Pixel <pixel@mandrakesoft.com> 0.95-8mdk
- fix loading initrd when you have more than 4GB
  (otherwise 32 bits signed int comparison in memcheck is wrong)

* Fri Jul 30 2004 Jean-Michel Dault <jmdault@mandrakesoft.com> 0.95-7mdk
- fix bug in fallback

* Tue Jul 20 2004 Jean-Michel Dault <jmdault@mandrakesoft.com> 0.95-6mdk
- add stuff from CVS to make grub more robust (fallback and savedefault)

* Wed Jul 14 2004 Jean-Michel Dault <jmdault@mandrakesoft.com> 0.95-5mdk
- add buildrequires

* Wed Jul 14 2004 Jean-Michel Dault <jmdault@mandrakesoft.com> 0.95-4mdk
- need to run aclocal/automake/autoconf to enable the patches!

* Wed Jul 14 2004 Pixel <pixel@mandrakesoft.com> 0.95-3mdk
- fix broken geometry patch (RedHat sucks)

* Tue Jul 13 2004 Pixel <pixel@mandrakesoft.com> 0.95-2mdk
- add splashimage patches and geometry patch (from RedHat)

* Tue Jul 06 2004 Pixel <pixel@mandrakesoft.com> 0.95-1mdk
- new release
- drop grub-0.93-gcc33.patch included upstream
- drop grub-0.93-add-our-own-memcpy.patch included upstream

* Wed Jan 07 2004 Pixel <pixel@mandrakesoft.com> 0.93-5mdk
- provides bootloader (basesystem now requires "bootloader" instead of lilo)

* Fri Jan 02 2004 Pixel <pixel@mandrakesoft.com> 0.93-4mdk
- altconfigfile is kept, but doesn't do anything anymore (bug #6664)

