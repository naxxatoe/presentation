Name:		douf00
Summary:	A simple and fatfree presentation software
Version:	0.01
Release:	1
Source0:	%{name}-%{version}.tar.gz
License:	GPL
Group:		Applications/Publishing
Buildroot:	%{_tmppath}/root-%{name}-%{version}
BuildRequires:	python >= 2.5
Requires:	python >= 2.5, wxPython

%description
DouF00 is a simple presentation- and screenmanagement software,
including timers, previews an audience and presentor screen 

%prep
%setup -q

%build
touch douf00
touch README

%install
if test "%{buildroot}" != ""; then
rm -rf %{buildroot}
mkdir -p %{buildroot}
fi
mkdir -p %{buildroot}/usr/bin
mkdir -p %{buildroot}/usr/share/doc/DouF00/
install -pm 0755 douf00 %{buildroot}/usr/bin/douf00
install -pm 0644 README %{buildroot}/usr/share/doc/douf00/README

%files
%defattr(-,root,root)
/usr/bin/douf00
%doc /usr/share/doc/douf00/README

%clean
if test "%{buildroot}" != ""; then
	rm -rf "%{buildroot}"
fi

%changelog
* Mon Apr 27 2009 Stefan Heinecke <tua.noc45@gmail.com> 1.0-1
- inital specfile creation

