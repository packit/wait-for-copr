Name:           wait-for-copr
Version:        0.0.post1+g12811b4
Release:        1.20230703170440785550.main%{?dist}
Summary:        A tool for integrating upstream projects with Fedora operating system

License:        MIT
URL:            https://github.com/packit/wait-for-copr
Source0:        wait_for_copr-0.0.post1+g12811b4.tar.gz
BuildArch:      noarch
BuildRequires:  python3-devel

%description
A tool to wait for dependencies being built in Copr.

%prep
%autosetup -n wait_for_copr-0.0.post1+g12811b4


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
* Mon Jul 03 2023 Frantisek Lachman <flachman@redhat.com> - 0.0.post1+g12811b4-1.20230703170440785550.main
- Development snapshot (12811b44)

* Mon Jul 03 2023 Frantisek Lachman <flachman@redhat.com> - 0.0.post1+g12811b4-1.20230703170224152868.main
- Development snapshot (12811b44)

* Mon Jul 03 2023 Frantisek Lachman <flachman@redhat.com> - 0.0.post1+g12811b4-1.20230703165551646432.main
- Development snapshot (12811b44)
