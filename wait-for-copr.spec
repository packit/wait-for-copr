Name:           wait-for-copr
Version:        0.0.post1+g12811b4
Release:        1.20230703170440785550.main%{?dist}
Summary:        A tool for integrating upstream projects with Fedora operating system

License:        MIT
URL:            https://github.com/packit/wait-for-copr
Source0:        wait_for_copr-0.0.post1+g12811b4.tar.gz
BuildArch:      noarch
BuildRequires:  python3-devel
BuildRequires:  python3dist(click-man)

%description
A tool to wait for dependencies being built in Copr.

%prep
%autosetup -n wait_for_copr-0.0.post1+g12811b4


%generate_buildrequires
%pyproject_buildrequires


%build
%pyproject_wheel


%install
%pyproject_install
%pyproject_save_files wait_for_copr
PYTHONPATH="%{buildroot}%{python3_sitelib}" click-man wait-for-copr --target %{buildroot}%{_mandir}/man1

%files -f %{pyproject_files}
%license LICENSE
%{_bindir}/wait-for-copr
%{_mandir}/man1/wait-for-copr*.1*

%doc README.md

%changelog
* Mon Jul 03 2023 Frantisek Lachman <flachman@redhat.com> - 0.0.post1+g12811b4-1.20230703170440785550.main
- Development snapshot (12811b44)

* Mon Jul 03 2023 Frantisek Lachman <flachman@redhat.com> - 0.0.post1+g12811b4-1.20230703170224152868.main
- Development snapshot (12811b44)

* Mon Jul 03 2023 Frantisek Lachman <flachman@redhat.com> - 0.0.post1+g12811b4-1.20230703165551646432.main
- Development snapshot (12811b44)
