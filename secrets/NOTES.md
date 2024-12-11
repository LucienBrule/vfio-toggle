# VFIO modprobe conf

```
/etc/modprobe.d/vfio.conf
options vfio-pci ids=10de:2206,10de:1aef
```

# GRUB CMDLINE

```
GRUB_CMDLINE_LINUX="rd.driver.blacklist=nouveau modprobe.blacklist=nouveau intel_iommu=on iommu=pt rd.driver.pre=vfio-pci vfio-pci.ids=10de:2206,10de:1aef,8086:10bc pcie_acs_override=downstream,multifunction"
```


cat /etc/modprobe.d/blacklist-nouveau.conf
blacklist nouveau
options nouveau modeset=0
developer@devbox ~/Developer/src/vfio-toggle main*                                                                                                 12:38:20
❯ cat /etc/modprobe.d/blacklist-nvidia.conf
blacklist nouveau
blacklist nvidia
blacklist nvidia_drm
blacklist nvidia_modeset
blacklist nvidia_uvm
