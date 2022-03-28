#
# Conditional build:
%bcond_with	doc		# don't build doc
%bcond_with	tests	# do not perform "make test"
%bcond_without	python2 # CPython 2.x module
%bcond_without	python3 # CPython 3.x module

%define 	module	enum
Summary:	Robust enumerated type support in Python.
Summary(pl.UTF-8):	Odporny typ wyliczeniowy dla Pythona
# Name must match the python module/package name (as in 'import' statement)
Name:		python-%{module}
Version:	0.4.4
Release:	1
License:	GPL or PSF
Group:		Libraries/Python
Source:		http://pypi.python.org/packages/source/e/%{module}/%{module}-%{version}.tar.gz
Patch0:     	%{name}-py3_setup_fix.patch
URL:		http://pypi.python.org/pypi/enum/
BuildRequires:	rpm-pythonprov
# if py_postclean is used
BuildRequires:	rpmbuild(macros) >= 1.710
%if %{with python2}
BuildRequires:	python-distribute
%endif
%if %{with python3}
BuildRequires:	python3-modules
%endif
# Below Rs only work for main package (python2)
#Requires:		python-libs
Requires:		python-modules
BuildArch:	noarch
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
Package provides a module for robust enumerations in Python.

# %description -l pl.UTF-8

%package -n python3-%{module}
Summary:	-
Summary(pl.UTF-8):	-
Group:		Libraries/Python
Requires:		python3-modules

%description -n python3-%{module}

%description -n python3-%{module} -l pl.UTF-8

%package apidocs
Summary:	%{module} API documentation
Summary(pl.UTF-8):	Dokumentacja API %{module}
Group:		Documentation

%description apidocs
API documentation for %{module}.

%description apidocs -l pl.UTF-8
Dokumentacja API %{module}.

%prep
%setup -q -n %{module}-%{version}
%patch0 -p1


%build
%if %{with python2}
%py_build %{?with_tests:test}
%endif

%if %{with python3}
%py3_build %{?with_tests:test}
%endif

%install
rm -rf $RPM_BUILD_ROOT

%if %{with python2}
%py_install

%py_postclean
%endif

%if %{with python3}
%py3_install
%endif


%clean
rm -rf $RPM_BUILD_ROOT

%if %{with python2}
%files
%defattr(644,root,root,755)
%{py_sitescriptdir}/*.py[co]
%if "%{py_ver}" > "2.4"
%{py_sitescriptdir}/%{module}-%{version}-py*.egg-info
%endif
%endif

%if %{with python3}
%files -n python3-%{module}
%defattr(644,root,root,755)
%{py3_sitescriptdir}/%{module}.py
%{py3_sitescriptdir}/__pycache__/*py[co]
%{py3_sitescriptdir}/%{module}-%{version}-py*.egg-info
%endif

%if %{with doc}
%files apidocs
%defattr(644,root,root,755)
%doc docs/_build/html/*
%endif
