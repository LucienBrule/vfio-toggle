Name:           vfio_toggle
Version:        0.1.0
Release:        1%{?dist}
Summary:        A utility for toggling VFIO and NVIDIA drivers

License:        MIT
URL:            https://github.com/LucienBrule/vfio-toggle
Source0:        %{name}-%{version}.tar.gz

# Disable automatic debuginfo subpackage if not needed
%global debug_package %{nil}

BuildRequires:  python3-devel
BuildRequires:  python3-pip
BuildRequires:  python3-setuptools
BuildRequires:  python3-wheel
BuildRequires:  pyproject-rpm-macros
Requires:       python3

# If your script interacts with hardware or system files, ensure other needed deps
# Requires: ???

%description
VFIO Toggle is a Python utility for managing VFIO and NVIDIA driver bindings on Linux systems.
It provides commands to switch between VFIO-pci and NVIDIA drivers for selected PCI devices.
A systemd service can be used to trigger toggling on-demand.

%prep
%setup -q

%build
# Build a wheel using standard pyproject macros
%pyproject_wheel

%install
# Install from the wheel into the buildroot
%pyproject_install

# Save the Python files list for %files
%pyproject_save_files vfio_toggle

# Install systemd unit file
install -Dm644 src/vfio_toggle/resources/vfio-toggle.service %{buildroot}%{_unitdir}/vfio-toggle.service

# Create the config directory for device JSON
mkdir -p %{buildroot}/etc/vfio-toggle

%files -f %{pyproject_files}
%license LICENSE.txt
%doc README.md

%{_bindir}/vfio-toggle
%{_bindir}/generate-devices
%dir /etc/vfio-toggle
%{_unitdir}/vfio-toggle.service

%changelog
* Wed Dec 11 2024 Lucien Brule <lucien@lucienbrule.com> - 0.1.0-1
- Initial package
