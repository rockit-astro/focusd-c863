Name:           python3-rockit-focuser-c863
Version:        %{_version}
Release:        1%{dist}
License:        GPL3
Summary:        Common backend code for Physik Instrumente C-863 Mercury Servo Controller daemon
Url:            https://github.com/rockit-astro/focusd-c863
BuildArch:      noarch
BuildRequires:  python3-devel

%description

%prep
rsync -av --exclude=build --exclude=.git --exclude=.github .. .

%generate_buildrequires
%pyproject_buildrequires -R

%build
%pyproject_wheel

%install
%pyproject_install
%pyproject_save_files rockit

%files -f %{pyproject_files}