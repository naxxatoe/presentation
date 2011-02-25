Name:		douf00
Summary:	A simple and fatfree presentation software
Version:	3.0.2
Release:	3
Source0:	%{name}-%{version}.tar.gz
License:	BSD
Group:		Applications/Publishing
Buildroot:	%{_tmppath}/root-%{name}-%{version}
BuildRequires:	python >= 2.5
Requires:	python >= 2.5, wxPython, pypoppler

%{!?python_sitelib: %global python_sitelib %(%{__python} -c "from distutils.sysconfig import get_python_lib; print get_python_lib()")}

%description
DouF00 is a simple presentation- and screenmanagement software,
including timers, previews an audience and presentor screen 

%prep
%setup -q

%build
cd pysrc && python setup.py build

%install
if test "%{buildroot}" != ""; then
	rm -rf %{buildroot}
	mkdir -p %{buildroot}
fi

cd pysrc && python setup.py install --root=%{buildroot}
mkdir -p %{buildroot}/usr/share/doc/douf00/
install -pm 0644 README %{buildroot}/usr/share/doc/douf00/README

%files
%defattr(-,root,root)
/usr/bin/douf00
%{python_sitelib}/DouF00
%doc /usr/share/doc/douf00/README

%clean
if test "%{buildroot}" != ""; then
	rm -rf "%{buildroot}"
fi

%changelog
* Sun Aug 23 2009 Bernd Zeimetz
- Updated to use the new setup.py/distutils
* Mon May 4 2009 Stefan Heinecke
- updated specfile for python modules
* Mon Apr 27 2009 Stefan Heinecke <tua.noc45@gmail.com> 1.0-1
- inital specfile creation
