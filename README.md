# toolkit
# 
Function: Create VM automately by virt-install cmd. The network and 
hostname will be set.

## Bridge
ovs-vsctl add-br ovs_br

virt-install can not find the ovs bridge, so virsh net-define by ovs_br.xml

<netowrk>
    <name>ovs_br</name>
    <forward mode='bridge'/> 
    <bridge name='ovs_br'>
    <virtualport type='openvswitch'/>
</network>