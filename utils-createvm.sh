#!/bin/bash
VM=$1
DS=$2
CPUN=$3
MEM=$4
RAM=$5
vboxmanage createhd --filename $VM.vdi --size $DS
vboxmanage createvm --name $VM --ostype "Linux26_64" --register
vboxmanage storagectl $VM --name "SATA Controller" --add sata --controller IntelAHCI
vboxmanage storageattach $VM --storagectl "SATA Controller" --port 0 --device 0 --type hdd --medium $VM.vdi
vboxmanage storagectl $VM --name "IDE Controller" --add ide
vboxmanage storageattach $VM --storagectl "IDE Controller" --port 0 --device 0 --type dvddrive --medium mini.iso
vboxmanage modifyvm $VM --ioapic on
vboxmanage modifyvm $VM --boot1 dvd --boot2 disk --boot3 none --boot4 none
vboxmanage modifyvm $VM --cpus $CPUN
vboxmanage modifyvm $VM --memory $MEM  
vboxmanage modifyvm $VM --vram $RAM
# ./utils-createvm.sh osprueba 32738 2 1024 124
