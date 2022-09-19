Name:      rockit-focuser-c863
Version:   %{_version}
Release:   1
Summary:   Physik Instrumente C-863 Mercury Servo Controller
Url:       https://github.com/rockit-astro/focusd-c863
License:   GPL-3.0
BuildArch: noarch

%description


%build
mkdir -p %{buildroot}%{_bindir}
mkdir -p %{buildroot}%{_unitdir}
mkdir -p %{buildroot}/etc/bash_completion.d
mkdir -p %{buildroot}%{_sysconfdir}/focusd/
mkdir -p %{buildroot}%{_udevrulesdir}

%{__install} %{_sourcedir}/focus %{buildroot}%{_bindir}
%{__install} %{_sourcedir}/c863_focusd %{buildroot}%{_bindir}
%{__install} %{_sourcedir}/c863_focusd@.service %{buildroot}%{_unitdir}
%{__install} %{_sourcedir}/completion/focus %{buildroot}/etc/bash_completion.d
%{__install} %{_sourcedir}/10-onemetre-redfocuser.rules %{buildroot}%{_udevrulesdir}
%{__install} %{_sourcedir}/onemetre.json %{buildroot}%{_sysconfdir}/focusd/

%package server
Summary:  Focuser control server.
Group:    Unspecified
Requires: python3-rockit-focuser-c863 python3-pyserial
%description server

%files server
%defattr(0755,root,root,-)
%{_bindir}/c863_focusd
%defattr(0644,root,root,-)
%{_unitdir}/c863_focusd@.service

%package client
Summary:  Focuser control client.
Group:    Unspecified
Requires: python3-rockit-focuser-c863
%description client

%files client
%defattr(0755,root,root,-)
%{_bindir}/focus
/etc/bash_completion.d/focus

%package data-onemetre
Summary: Focuser data for the W1m
Group:   Unspecified
%description data-onemetre

%files data-onemetre
%defattr(0644,root,root,-)
%{_sysconfdir}/focusd/onemetre.json
%{_udevrulesdir}/10-onemetre-redfocuser.rules

%changelog