#!/bin/bash

virt-filesystems --long --parts --blkdevs -h -a /datapool/ubuntu14.04.qcow2

qemu-img create -f qcow2 resize.qcow2 20G

virt-resize --expand /dev/sda1 ubuntu14.04.qcow2 resize.qcow2


