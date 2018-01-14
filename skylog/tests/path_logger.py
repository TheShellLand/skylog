#!/bin/usr/env python3

from skylog.logger.path import WatchDog

path = '/var/log'
logs = WatchDog(path)

logs.start()
