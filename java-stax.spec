#
# Conditional build:
%bcond_without	javadoc		# don't build javadoc
%bcond_without	tests		# don't build and run tests
#
%include	/usr/lib/rpm/macros.java
#
%define		apiversion	1.0.1
%define		srcname		stax
Summary:	StAX reference implementation
Name:		java-stax
Version:	1.2.0
Release:	0.1
License:	Apache v2.0
Group:		Libraries/Java
Source0:	http://dist.codehaus.org/stax/distributions/%{srcname}-src-%{version}.zip
# Source0-md5:	980143f96b3f6ce45d2e4947da21a5e9
Patch0:		%{name}-sourcetarget.patch
URL:		http://stax.codehaus.org/
BuildRequires:	ant >= 1.7.1-4
BuildRequires:	java-gcj-compat-devel
BuildRequires:	jpackage-utils
BuildRequires:	rpm-javaprov
BuildRequires:	rpmbuild(macros) >= 1.300
Provides:	stax-api = %{api_version}
BuildArch:	noarch
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
StAX is a standard XML processing API that allows you to stream XML
data from and to your application. This StAX implementation is the
standard pull parser implementation for JSR-173 specification.

%package javadoc
Summary:	Online manual for %{name}
Summary(pl.UTF-8):	Dokumentacja online do %{name}
Group:		Documentation
Requires:	jpackage-utils

%description javadoc
Documentation for %{srcname}.

%description javadoc -l pl.UTF-8
Dokumentacja do %{srcname}.

%description javadoc -l fr.UTF-8
Javadoc pour %{srcname}.

%package examples
Summary:	Examples for %{name}
Summary(pl.UTF-8):	Przykłady dla pakietu %{name}
Group:		Documentation
Requires:	%{name} = %{epoch}:%{version}-%{release}

%description examples
Demonstrations and samples for %{srcname}.

%description examples -l pl.UTF-8
Pliki demonstracyjne i przykłady dla pakietu %{srcname}.

%prep
%setup -qc
%patch0 -p1

%build
export SHELL=/bin/sh

%ant clean
%ant -Dbuild.compiler=gcj dist
%ant javadoc

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT%{_javadir}

cp -a build/%{srcname}-%{version}-dev.jar $RPM_BUILD_ROOT%{_javadir}/%{srcname}-%{version}.jar
ln -s %{srcname}-%{version}.jar $RPM_BUILD_ROOT%{_javadir}/%{srcname}.jar
cp -a build/%{srcname}-api-%{apiversion}.jar $RPM_BUILD_ROOT%{_javadir}/%{srcname}-api-%{apiversion}.jar
ln -s %{srcname}-api-%{apiversion}.jar $RPM_BUILD_ROOT%{_javadir}/%{srcname}-api.jar

install -d $RPM_BUILD_ROOT%{_javadocdir}/%{name}-%{version}
cp -a build/javadoc/* $RPM_BUILD_ROOT%{_javadocdir}/%{name}-%{version}
ln -s %{name}-%{version} $RPM_BUILD_ROOT%{_javadocdir}/%{name} # ghost symlink

install -d $RPM_BUILD_ROOT%{_examplesdir}/%{name}-%{version}
cp -a src/samples/* $RPM_BUILD_ROOT%{_examplesdir}/%{name}-%{version}

%clean
rm -rf $RPM_BUILD_ROOT

%post javadoc
ln -nfs %{name}-%{version} %{_javadocdir}/%{name}

%files
%defattr(644,root,root,755)
%{_javadir}/*.jar

%files examples
%defattr(644,root,root,755)
%{_examplesdir}/%{name}-%{version}

%files javadoc
%defattr(644,root,root,755)
%{_javadocdir}/%{name}-%{version}
%ghost %{_javadocdir}/%{name}
