Name:           wait-for-copr
Version:        0.0.1
Release:        1%{?dist}
Summary:        A tool for integrating upstream projects with Fedora operating system

License:        MIT
URL:            https://github.com/packit/wait-for-copr
Source0:        %{srcname}-%{version}.tar.gz
BuildArch:      noarch
BuildRequires:  python3-devel

%description
A tool to wait for dependencies being built in Copr.

%prep
%autosetup -n %{srcname}-%{version}


%generate_buildrequires
# The -w flag is required for EPEL 9's older hatchling
%pyproject_buildrequires %{?el9:-w}

%build
%pyproject_wheel


%install
%pyproject_install
%pyproject_save_files wait_for_copr

%files -f %{pyproject_files}
%{_bindir}/wait-for-copr

# Epel9 does not tag the license file in pyproject_files as a license. Manually install it in this case
%if 0%{?el9}
%license LICENSE
%endif

%doc README.md

%changelog
%autochangelog
