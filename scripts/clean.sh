#!/bin/bash

vmlist=`virsh list --all | awk '{print $2}' | grep -v "Name"`

for vm in $vmlist
do
    echo "destroy "$vm
    virsh destroy $vm
    echo "undefine "$vm
    virsh undefine $vm
    echo "remove "${vm}.*
    rm -rf "/datapool/"${vm}.*
done


