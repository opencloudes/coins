#!/bin/bash

# /etc/init.d/test

### BEGIN INIT INFO
...
### END INIT INFO

case "$1" in
   start)
      echo "Starting server"
      python /usr/local/bin/test.py start 
      ;;

   stop)
      echo "Stopping server"
      python /usr/local/bin/test.py stop
      ;;

   restart)
      echo "Restarting server"
      python /usr/local/bin/test.py restart
      ;;

   *)
      echo "Usage: /etc/init.d/demonioprueba.sh {start|stop|restart}"
      exit 1
      ;;
esac
exit 0
