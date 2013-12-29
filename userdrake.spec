%define debug_package %{nil}
Summary:	A graphical interface for administering users and groups
Name:		userdrake
Version:	1.14
Release:	6
Source0:	%{name}-%{version}.tar.xz
URL:		https://abf.rosalinux.ru/omv_software/userdrake
License:	GPL
Group:		System/Configuration/Other
Requires:	drakxtools
Requires:	libuser
Requires:	usermode-consoleonly
Requires:	transfugdrake
#Suggests:	xguest
BuildRequires:	gettext
BuildRequires:	perl-devel
BuildRequires:	pkgconfig(libuser)
BuildRequires:	pkgconfig(glib-2.0)
BuildRequires:	pam-devel
Requires:	accountservice

%description
Userdrake is a user-friendly and powerful tool for administrating users and 
groups. It depends on the libuser library.

%prep
%setup -q

%build
cd USER
%{__perl} Makefile.PL INSTALLDIRS=vendor
cd ..
make OPTIMIZE="%{optflags} -w"

%install
make PREFIX=%{buildroot} install

cd USER
%makeinstall_std
cd ..

#install lang
%find_lang userdrake


mkdir -p %{buildroot}%{_datadir}/applications
cat > %{buildroot}%{_datadir}/applications/mandriva-userdrake.desktop <<EOF
[Desktop Entry]
Name=User Administration
Comment=Add or remove users and groups
Exec=/usr/bin/userdrake
Icon=userdrake
Type=Application
StartupNotify=true
Categories=GTK;System;X-MandrivaLinux-CrossDesktop;
NoDisplay=true
EOF

# consolehelper configuration
ln -sf %{_bindir}/consolehelper %{buildroot}%{_bindir}/userdrake
ln -sf %{_bindir}/userdrake %{buildroot}%{_bindir}/drakuser
mkdir -p %{buildroot}%{_sysconfdir}/pam.d
ln -sf %{_sysconfdir}/pam.d/mandriva-simple-auth %{buildroot}%{_sysconfdir}/pam.d/userdrake
mkdir -p %{buildroot}%{_sysconfdir}/security/console.apps/
cat > %{buildroot}%{_sysconfdir}/security/console.apps/userdrake <<EOF
USER=root
PROGRAM=/usr/sbin/userdrake
FALLBACK=false
SESSION=true
EOF

# userdrake <-> drakuser
ln -s %{_sysconfdir}/pam.d/userdrake %{buildroot}%{_sysconfdir}/pam.d/drakuser
ln -s %{_sysconfdir}/security/console.apps/userdrake \
        %{buildroot}%{_sysconfdir}/security/console.apps/drakuser

%files -f userdrake.lang
%doc README COPYING RELEASE_NOTES
%config(noreplace) %{_sysconfdir}/sysconfig/userdrake
%config(noreplace) %{_sysconfdir}/pam.d/userdrake
%config(noreplace) %{_sysconfdir}/security/console.apps/userdrake
# two symlinks in sysconfdir
%{_sysconfdir}/pam.d/drakuser
%{_sysconfdir}/security/console.apps/drakuser
%{_prefix}/bin/*
%{_prefix}/sbin/*
%{_datadir}/userdrake
%{_mandir}/man3/USER*
%{_datadir}/applications/mandriva-*.desktop
%{perl_vendorarch}/USER.pm
%{perl_vendorarch}/auto/USER
%{_iconsdir}/*.png
%{_miconsdir}/*.png
%{_liconsdir}/*.png
