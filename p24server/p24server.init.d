#!/bin/sh                                                                  
#                                                                          
# chkconfig: 2405 32 12                                                     
# description: Starts and stops p24server                                   
#                                                                           
# pidfile: /var/run/p24server.pid                                              
#                                                                              
# remade by Henrietta                                                          

# Avoid using root's TMPDIR
unset TMPDIR               

# Source networking configuration.
. /etc/sysconfig/network          

# Check that networking is up.
[ ${NETWORKING} = "no" ] && exit 0

RETVAL=0

start() {
        if [ -f /var/run/p24server.pid ] ; then
                echo "p24server already started" && exit 0
        fi                                                
        echo -n $"Starting p24server: "                   
        /usr/local/bin/p24server/p24server.py      
        echo                                              
        RETVAL=$?                                         
        /sbin/pidof p24server.py > /var/run/p24server.pid 
}                                                         

stop() {
        if [ -f /var/run/p24server.pid ] ; then
                echo -n $"Stopping p24server: "
                killall p24server.py           
                daemon /usr/local/bin/p24server/cleanup.py
                echo                               
                RETVAL=$?                          
                rm -f /var/run/p24server.pid       
        else                                       
                echo "p24server is not running" && exit 0
        fi                                               
        return $RETVAL                                   
}                                                        

restart() {
        stop
        start
}

case "$1" in
  start)
        start
        ;;
  stop)
        stop
        ;;
  restart)
        restart
        ;;
  *)
        echo $"Usage: $0 {start|stop|restart}"
        exit 1
esac

exit $?
