%define debug_package %{nil}

Summary:	A graphical interface for administering users and groups
Name:		userdrake
Version:	2.2
Release:	1
Source0:	%{name}-%{version}.tar.xz
URL:		https://abf.io/omv_software/userdrake
License:	GPL
Group:		System/Configuration/Other
Requires:	drakxtools >= 16.65
Requires:	libuser
Requires:	polkit
Requires:	transfugdrake
#Suggests:	xguest
BuildRequires:	gettext
BuildRequires:	intltool
BuildRequires:	perl-devel
BuildRequires:	pkgconfig(libuser)
BuildRequires:	pkgconfig(glib-2.0)
BuildRequires:	pam-devel
Requires:	accountsservice
Requires:	perl(Net::DBus)
Requires:	shadow >= 4.2.1-14

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

%files -f userdrake.lang
%doc README COPYING RELEASE_NOTES
%config(noreplace) %{_sysconfdir}/sysconfig/userdrake
# two symlinks in sysconfdir
%{_prefix}/bin/*
%{_libexecdir}/drakuser
%{_datadir}/userdrake
%{_mandir}/man3/USER*
%{_datadir}/applications/mandriva-*.desktop
%{_datadir}/polkit-1/actions/*
%{perl_vendorarch}/USER.pm
%{perl_vendorarch}/auto/USER
%{_iconsdir}/*.png
%{_miconsdir}/*.png
%{_liconsdir}/*.png
