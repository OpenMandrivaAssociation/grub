%define _default_patch_fuzz 2

Summary:	GRand Unified Bootloader
Name:		grub
Version:	0.97
Release:	42
License:	GPLv2
Group:		System/Kernel and hardware
Url:		http://www.gnu.org/software/grub/
Source0:	ftp://alpha.gnu.org/gnu/grub/%{name}-%{version}.tar.gz
Source2:	menu.lst.example
Exclusivearch:	%{ix86} x86_64 amd64 ia32e

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
#Patch100:	grub-0.90-append.patch
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
#Patch1115:	grub-0.97-gcc4.patch

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
#Patch1149:	grub-0.97-stderr.patch

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

Patch1156:	grub-0.97-automake-fixes.patch

BuildRequires:	automake1.8
BuildRequires:	tetex-dvips
BuildRequires:	tetex-latex
BuildRequires:	texinfo
BuildRequires:	glibc-static-devel
BuildRequires:	gpm-devel
BuildRequires:	pkgconfig(ncursesw)
Provides:	bootloader

%description
GRUB is a GPLed bootloader intended to unify bootloading across x86
operating systems.  In addition to loading the Linux and *BSD kernels,
it implements the Multiboot standard, which allows for flexible loading
of multiple boot images (needed for modular kernels such as the GNU
Hurd).

%package	doc
Summary:	More documentation for grub
Group:		Books/Computer books

%description	doc
More documentation for grub

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
%patch1156 -p1

%patch10000 -p1
%patch10001 -p1
%patch10005 -p1
%patch10007 -p1
%patch10009 -p1
%patch10015 -p1
#%#patch10016 -p1
%patch10018 -p1

%patch10017 -p0

autoreconf -fi

%build
# force building grub.info from grub.texi (since patches do not edit both)
rm docs/grub.info

# automake 1.11.2
perl -pi -e 's|pkglib_|pkgdata_|g;' stage{1,2}/Makefile.{am,in}

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
%make -C docs ps

%install
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

%files
%defattr(0644,root,root,0755)
/boot/grub
%{_infodir}/*
%{_mandir}/*/*
/lib/grub
%defattr(0755,root,root,0755)
%{_bindir}/mbchk
/sbin/grub*

%files doc
%defattr(0644,root,root,0755)
%doc AUTHORS BUGS ChangeLog docs/grub.ps docs/multiboot.ps NEWS README
%doc THANKS TODO

