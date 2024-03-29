# VirtualBox command lines

## Manage VM

List all the VMs: `vboxmanage list vms`

Start a vm: `vboxmanage startvm "Ubuntu Server" --type headless`

Pause a VM: `VBoxManage controlvm "Ubuntu Server" pause --type headless`

Resume a VM: `VBoxManage controlvm "Ubuntu Server" resume --type headless`

PowerOff a VM: `VBoxManage controlvm "Ubuntu Server" poweroff --type headless`


## List of OS Type
`VBoxManage list ostypes`

## Create VM
`VBoxManage createvm --name [MACHINE NAME] --ostype [Os Type, ex: "Debian_64"] --register --basefolder '/var/vms' `

`VBoxManage createvm --name "openbb" --ostype "Ubuntu" --register --basefolder '/var/vms'`

`VBoxManage createhd --filename /var/vms/openbb/openbb_disk.vdi --size 40000 --format VDI`  

## Delete VM
`VBoxManage unregistervm <uuid>|<name> [--delete]`

## Set memory and network


```
VBoxManage modifyvm [MACHINE NAME] --ioapic on              
VBoxManage modifyvm [MACHINE NAME] --memory 1024 --vram 128  
VBoxManage modifyvm [MACHINE NAME] --nic1 nat
VBoxManage modifyvm [MACHINE NAME] --nic1 bridged
```

## Create the Disk and connect the CD ISO
```
VBoxManage createhd --filename `pwd`/[MACHINENAME]/[MACHINE NAME]_DISK.vdi --size 80000 --format VDI
VBoxManage storagectl [MACHINE NAME] --name "SATA Controller" --add sata --controller IntelAhci
VBoxManage storageattach [MACHINE NAME] --storagectl "SATA Controller" --port 0 --device 0 --type hdd --medium  `pwd`/[MACHINE NAME]/[MACHINE NAME]_DISK.vdi                
VBoxManage storagectl [MACHINE NAME] --name "IDE Controller" --add ide --controller PIIX4
VBoxManage storageattach [MACHINE NAME] --storagectl "IDE Controller" --port 1 --device 0 --type dvddrive --medium `pwd`/debian.iso       
VBoxManage modifyvm [MACHINE NAME] --boot1 dvd --boot2 disk --boot3 none --boot4 none 
```

## Set RDP access and start the VM
```
VBoxManage modifyvm [MACHINE NAME] --vrde on                  
VBoxManage modifyvm [MACHINE NAME] --vrdemulticon on --vrdeport 10001

VBoxHeadless --startvm [MACHINE NAME] 
```


## Script
```
#!/bin/bash
MACHINENAME=$1

# Download debian.iso
if [ ! -f ./debian.iso ]; then
    wget https://cdimage.debian.org/debian-cd/current/amd64/iso-cd/debian-12.5.0-amd64-netinst.iso -O debian.iso
fi

#Create VM
VBoxManage createvm --name $MACHINENAME --ostype "Debian_64" --register --basefolder `pwd`
#Set memory and network
VBoxManage modifyvm $MACHINENAME --ioapic on
VBoxManage modifyvm $MACHINENAME --memory 1024 --vram 128
VBoxManage modifyvm $MACHINENAME --nic1 nat
#Create Disk and connect Debian Iso
VBoxManage createhd --filename `pwd`/$MACHINENAME/$MACHINENAME_DISK.vdi --size 80000 --format VDI
VBoxManage storagectl $MACHINENAME --name "SATA Controller" --add sata --controller IntelAhci
VBoxManage storageattach $MACHINENAME --storagectl "SATA Controller" --port 0 --device 0 --type hdd --medium  `pwd`/$MACHINENAME/$MACHINENAME_DISK.vdi
VBoxManage storagectl $MACHINENAME --name "IDE Controller" --add ide --controller PIIX4
VBoxManage storageattach $MACHINENAME --storagectl "IDE Controller" --port 1 --device 0 --type dvddrive --medium `pwd`/debian.iso
VBoxManage modifyvm $MACHINENAME --boot1 dvd --boot2 disk --boot3 none --boot4 none

#Enable RDP
VBoxManage modifyvm $MACHINENAME --vrde on
VBoxManage modifyvm $MACHINENAME --vrdemulticon on --vrdeport 10001

#Start the VM
VBoxHeadless --startvm $MACHINENAME
```

# References
- https://andreafortuna.org/2019/10/24/how-to-create-a-virtualbox-vm-from-command-line/
- https://www.techrepublic.com/article/how-to-run-virtualbox-virtual-machines-from-the-command-line/


```
#!/bin/bash
MACHINE_NAME=openbb
MACHINE_DESCRIPTION=OpenBB Server
CPU=1
RAM=4096
HD=30000
OS_TYPE=Ubuntu
ISO=/home/david/iso/ubuntu-22.04.3-live-server-amd64.iso

# Register the VM 
VBoxManage createvm --name $MACHINE_NAME --register 
# Configure VM settings  
VBoxManage modifyvm $MACHINE_NAME --ostype "$OS_TYPE" --memory $RAM --acpi on --cpus $CPU --description "$MACHINE_DESCRIPTION"
# Declare a bridge interface 
VBoxManage modifyvm $MACHINE_NAME  --nic1 bridged --nictype1 82545EM --bridgeadapter1 virtualbox
# VRDE is for access via rdp client
# VBoxManage modifyvm $MACHINE_NAME  --vrde on 
# Create an HDD 
VBoxManage createhd --filename /var/vms/$MACHINE_NAME/${MACHINE_NAME}_disk.vdi --size $HD --format VDI
# Add an HDD Controller 
# VBoxManage storagectl $MACHINE_NAME  --name "IDE Controller" --add ide --controller PIIX4
VBoxManage storagectl $MACHINE_NAME --name "SATA Controller" --add sata # --controller IntelAhci
# Map the HDD and ISO via IDE Controller
VBoxManage storageattach $MACHINE_NAME --storagectl "SATA Controller" --port 0 --device 0 --type hdd --medium  /var/vms/$MACHINE_NAME/${MACHINE_NAME}_disk.vdi
VBoxManage storageattach $MACHINE_NAME --storagectl "SATA Controller" --port 1 --device 0 --type dvddrive --medium $ISO
# Boot from DVD 
VBoxManage modifyvm $MACHINE_NAME --boot1 dvd
```