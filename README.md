# TOOLKIT
# 
Function: Create VM automately by virt-install cmd. The network and 
hostname will be set.


## The function of the script

- Create VM 
- Set up the IP
- Set up the hostname
- Modify the size of disk
 
All these functions run in an automatic way and controlled by /config/vm.csv.


## Supported OS:

1. ubuntu


## Setting Environment

- The directory of image is /datapool/ on host.
- The name of lvm must be 'vmvg'.(If used)
- Libvirt, guestfish

## Run the script

- Download the script:

'''
	git clone https://github.com/Second222None/toolkit
'''

- Prepare the environment:

'''
	# bash /toolkit/scripts/first.sh
'''

- Edit the /toolkit/config/vm.csv to customize your configuration.

1. vm - qcow2, vmLvm - lvm, vmCpOnly - copy the image directly
2. The name of the image in the /datapool/.
3. The name of the VM.
4. The password of the VM.
5. The size of the first disk.
6. The size of the second disk.
7. The size of Memory.
8. The number of vcpu.
9. The virtualization of the first nic.(e1000,virtio)
10. The birdge the first nic connected to.
11. The birdge the second nic connected to.
12. The VNC port.
13. First IP.
14. First netmask.
15. First gateway.
16. Second IP.
17. Second netmask.
18. Second gateway.

- Run the script:

'''
	python /toolkit/virtauto.py
'''

## Bridge
    
'''    
    ovs-vsctl add-br ovs_br
'''

    创建虚拟机过程中出现如下错误:
    virt-install can not find the ovs bridge, so virsh net-define by ovs_br.xml
    原因:virsh不支持ovs网桥，需要自己定义，告诉virsh网桥的存在
    
'''
    <netowrk>
        <name>ovs_br</name>
        <forward mode='bridge'/> 
        <bridge name='ovs_br'>
        <virtualport type='openvswitch'/>
    </network>
'''
    
    virsh net-define ovs_br.xml



