# toolkit
# 
Function: Create VM automately by virt-install cmd. The network and 
hostname will be set.

## Bridge
    ovs-vsctl add-br ovs_br
    创建虚拟机过程中出现如下错误:
    virt-install can not find the ovs bridge, so virsh net-define by ovs_br.xml
    原因:virsh不支持ovs网桥，需要自己定义，告诉virsh网桥的存在

    <netowrk>
        <name>ovs_br</name>
        <forward mode='bridge'/> 
        <bridge name='ovs_br'>
        <virtualport type='openvswitch'/>
    </network>
    
    virsh net-define ovs_br.xml



