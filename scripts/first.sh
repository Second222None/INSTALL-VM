#!/bin/bash
# write by weisong
# version 2017.10.10

# get script path
selfpath=$(cd "$(dirname "$0")";pwd)
echo $selfpath
cd $selfpath

# install libvirt guestfish virtualization
sudo apt-get update
sudo apt-get -q -y --force-yes --allow-unauthenticated \
	-o Dpkg::Options::="--force-confnew" install libvirt-bin
sudo apt-get -q -y --force-yes --allow-unauthenticated \
	-o Dpkg::Options::="--force-confnew" install libguestfs-tools