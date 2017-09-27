#################################################
# Default frequency
# $TIMES x $INTERVAL = performance collection long
# 
#eg:
# TIMES=180 , INTERVAL=10  collection long is 0.5h
#
#################################################
#!/bin/bash
TIMES=10
INTERVAL=2
PWD=`pwd`
TIME=`date "+%F %H:%M:%S"`
TAR=`whereis tar|awk -F ":" '{print $2}'|awk '{print $1}'`
SAR=`whereis sar|awk -F ":" '{print $2}'|awk '{print $1}'`
IOSTAT=`whereis iostat|awk -F ":" '{print $2}'|awk '{print $1}'`

SysInfo(){
    echo "sysip : $SYSIP" | tee $PWD/$SYSIP/sysinfo
    echo "starttime : $TIME" |tee -a $PWD/$SYSIP/sysinfo
    /sbin/ifconfig >>$PWD/$SYSIP/sysinfo
    echo "===================================" >> $PWD/$SYSIP/sysinfo
    /usr/sbin/dmidecode >>$PWD/$SYSIP/sysinfo
    echo "===================================" >> $PWD/$SYSIP/sysinfo
    /bin/cat /proc/cpuinfo >> $PWD/$SYSIP/sysinfo
    echo "===================================" >> $PWD/$SYSIP/sysinfo
    /sbin/fdisk -l >> $PWD/$SYSIP/sysinfo
    echo "===================================" >> $PWD/$SYSIP/sysinfo
    /bin/df -Th >>$PWD/$SYSIP/sysinfo
    echo "===================================" >> $PWD/$SYSIP/sysinfo
    /usr/bin/free -m >> $PWD/$SYSIP/sysinfo
    echo "===================================" >> $PWD/$SYSIP/sysinfo    
    echo ""
}

CheckEnv(){
    PUB_IP=`/sbin/ifconfig |grep "inet addr" | \
     awk -F: '{print $2}'| awk '{print $1}'| \
     grep -v "172\|127\|192"|sed -n 1p`
     
    PRI_IP=`/sbin/ifconfig |grep "inet addr" | \
     awk -F: '{print $2}'| awk '{print $1}'| \
     grep "10"|sed -n 1p`
     
    if [ $PUB_IP == "" ];then
        SYSIP=$PRI_IP
    else
        SYSIP=$PUB_IP
    fi
    
    if [ -d $PWD/$SYSIP ];then
        rm -rf $PWD/$SYSIP
    fi
    
    echo $PWD/$SYSIP
    
    mkdir -p $PWD/$SYSIP
    
    if ! grep iostat /usr/bin/iostat ;then
        apt-get install -y iostat
    fi
}

GetPerf(){
    CPUUSAGE="$PWD/$SYSIP/cpuusage.log"
    MEMUSAGE="$PWD/$SYSIP/memusage.log"
    DISKUSAGE="$PWD/$SYSIP/diskusage.log"
    NETWORK="$PWD/$SYSIP/network.log"
    $SAR -u $INTERVAL $TIMES >> $CPUUSAGE &
    $SAR -r $INTERVAL $TIMES >> $MEMUSAGE &
    $SAR -l $INTERVAL $TIMES >> $NETWORK &
    $IOSTAT -dkx $INTERVAL $TIMES >> $DISKUSAGE &
    
    for ((i=0;i<$TIMES;i++))
    do
        sleep $INTERVAL
    done
}


CheckEnv
SysInfo
GetPerf

if [ -d $PWD/$SYSIP ];then
    cd $PWD
    rm -f $SYSIP.tar.gz
    tar zcvf $SYSIP.tar.gz $SYSIP
fi



