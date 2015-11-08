#!/bin/bash

DEST=/root/backup
TEMP=`mktemp -d`
TODAY=`date +%d%m%y`

if [ ! -d $DEST ]; then
   mkdir -p $DEST
fi

find $DEST/* -maxdepth 0 -type f -mtime +40 -exec rm -v '{}' \;

cp -a /usr/local/nagios/etc /etc/check_mk /etc/openvpn $TEMP

tar -cjf $DEST/config-$TODAY.tar.bz2 -C $TEMP .

rm -r $TEMP

/usr/local/bin/s3cmd put /root/backup/config-$TODAY.tar.bz2 s3://nag-back-ara/
