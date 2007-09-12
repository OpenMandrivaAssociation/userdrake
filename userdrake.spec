# Changed by Makefile of cvs.
# Please change this file only in cvs!

%define version 1.2.10
%define name userdrake

Summary:	A graphical interface for administering users and groups
Name:		%{name}
Version:	%{version}
Release:	%mkrel 2
#cvs source
# http://www.mandrivalinux.com/en/cvs.php3
Source0:	%{name}-%{version}.tar.bz2
URL:		http://people.mandriva.com/~daouda/mandrake/userdrake.html
License:	GPL
Group:		System/Configuration/Other
Requires:	drakxtools >= 10.4.26-1mdk, libuser >= 0.51.7-5mdk
Requires:	usermode-consoleonly >= 1.92-4mdv2008.0
BuildRoot:	%{_tmppath}/%{name}-buildroot
BuildRequires:  gettext perl-devel libuser-devel libglib2.0-devel pam-devel

%description
Userdrake is a user-friendly and powerful tool for administrating users and 
groups. It depends on the libuser library. 

%prep
%setup -q
		
%build
cd USER
%{__perl} Makefile.PL INSTALLDIRS=vendor 
make OPTIMIZE="$RPM_OPT_FLAGS -w" 

%install
rm -rf $RPM_BUILD_ROOT
make PREFIX=$RPM_BUILD_ROOT install 

cd USER
%makeinstall_std
cd ..

#install lang
%{find_lang} userdrake

mkdir -p $RPM_BUILD_ROOT%{_menudir}
cat > $RPM_BUILD_ROOT%{_menudir}/%{name} << EOF
?package(%{name}):\ 
needs="x11" \
icon="userdrake.png" \
section="System/Configuration/Other" \
title="User Administration" \
longtitle="Add or remove users and groups" \
command="/usr/bin/userdrake" xdg="true"
EOF

mkdir -p $RPM_BUILD_ROOT%{_datadir}/applications
cat > $RPM_BUILD_ROOT%{_datadir}/applications/mandriva-userdrake.desktop <<EOF
[Desktop Entry]
Name=User Administration
Comment=Add or remove users and groups
Exec=/usr/bin/userdrake
Icon=userdrake
Type=Application
StartupNotify=true
Categories=GTK;System;X-MandrivaLinux-CrossDesktop;
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

%post
%{update_menus}

%postun
%{clean_menus}

%clean
rm -rf %{buildroot}

%files -f userdrake.lang
%defattr(-,root,root)
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
%{_menudir}/%{name}
%{perl_vendorarch}/USER.pm
%{perl_vendorarch}/auto/USER
%{_iconsdir}/*.png
%{_miconsdir}/*.png
%{_liconsdir}/*.png

