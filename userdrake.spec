# Changed by Makefile of cvs.
# Please change this file only in cvs!

%define version 1.2.9
%define name userdrake

Summary:	A graphical interface for administering users and groups
Name:		%{name}
Version:	%{version}
Release:	%mkrel 1
#cvs source
# http://www.mandrivalinux.com/en/cvs.php3
Source0:	%{name}-%{version}.tar.bz2
URL:		http://people.mandriva.com/~daouda/mandrake/userdrake.html
License:	GPL
Group:		System/Configuration/Other
Requires:	drakxtools >= 10.4.26-1mdk, libuser >= 0.51.7-5mdk
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
command="/usr/sbin/userdrake" xdg="true"
EOF

mkdir -p $RPM_BUILD_ROOT%{_datadir}/applications
cat > $RPM_BUILD_ROOT%{_datadir}/applications/mandriva-userdrake.desktop <<EOF
[Desktop Entry]
Name=User Administration
Comment=Add or remove users and groups
Exec=/usr/sbin/userdrake
Icon=userdrake
Type=Application
StartupNotify=true
Categories=X-MandrivaLinux-System-Configuration-Other;Settings;
EOF

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


