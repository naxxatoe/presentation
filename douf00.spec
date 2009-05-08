Name:		douf00
Summary:	A simple and fatfree presentation software
Version:	1.0
Release:	1
Source0:	%{name}-%{version}.tar.gz
License:	GPLv3
Group:		Applications/Publishing
Buildroot:	%{_tmppath}/root-%{name}-%{version}
BuildRequires:	python >= 2.5
Requires:	python >= 2.5, wxPython

%{!?python_sitelib: %global python_sitelib %(%{__python} -c "from distutils.sysconfig import get_python_lib; print get_python_lib()")}

%description
DouF00 is a simple presentation- and screenmanagement software,
including timers, previews an audience and presentor screen 

%prep
%setup -q

%build
touch douf00

%install
if test "%{buildroot}" != ""; then
	rm -rf %{buildroot}
	mkdir -p %{buildroot}
fi
mkdir -p %{buildroot}/usr/bin
mkdir -p %{buildroot}/usr/share/doc/douf00/
install -pm 0755 douf00 %{buildroot}/usr/bin/douf00
install -pm 0644 README %{buildroot}/usr/share/doc/douf00/README

mkdir -p %{buildroot}/%{python_sitelib}/douf00
install -pm 0644 config.py %{buildroot}/%{python_sitelib}/douf00/config.py
install -pm 0644 DisplayChoice.py %{buildroot}/%{python_sitelib}/douf00/DisplayChoice.py
install -pm 0644 MyImage.py %{buildroot}/%{python_sitelib}/douf00/MyImage.py
install -pm 0644 NumberFrame.py %{buildroot}/%{python_sitelib}/douf00/NumberFrame.py
install -pm 0644 PresentationScreen.py %{buildroot}/%{python_sitelib}/douf00/PresentationScreen.py
install -pm 0644 PresentorsScreen.py %{buildroot}/%{python_sitelib}/douf00/PresentorsScreen.py
install -pm 0644 py2exe-setup.py %{buildroot}/%{python_sitelib}/douf00/py2exe-setup.py
install -pm 0644 SlideList.py %{buildroot}/%{python_sitelib}/douf00/SlideList.py
install -pm 0644 ThumbnailList.py %{buildroot}/%{python_sitelib}/douf00/ThumbnailList.py

%files
%defattr(-,root,root)
/usr/bin/douf00
%{python_sitelib}/douf00/
%doc /usr/share/doc/douf00/README

%clean
if test "%{buildroot}" != ""; then
	rm -rf "%{buildroot}"
fi

%changelog
* Mon May 4 2009 Stefan Heinecke
- updated specfile for python modules
* Mon Apr 27 2009 Stefan Heinecke <tua.noc45@gmail.com> 1.0-1
- inital specfile creation
