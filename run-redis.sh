#!/bin/bash
if ! [ -x "$(command -v redis-server)" ]; then
    echo 'Warning: redis is not installed or is not in the $PATH.' >&2
    if [ -f "/etc/arch-release" ]; then
        # TODO add an alert notification here saying we need your password
        sudo pacman -S redis
        redis-server
    else
    	curl -O http://download.redis.io/redis-stable.tar.gz
    	tar xvzf redis-stable.tar.gz
    	rm redis-stable.tar.gz
    	cd redis-stable
    	make -j8
        server/redis-server
    fi
else
    # check if redis is running
    pong=$(redis-cli ping)
    if [[ "$pong" == "PONG" ]]; then
        # exit
        echo "redis already running exiting..."
        exit 1
        # echo $pong
    else
        redis-server
    fi
fi
