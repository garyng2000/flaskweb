#!/bin/bash

#set -o xtrace
#set -e

if grep -E 'certbot' /etc/crontab; then
    echo "already has certbot renew"
else
    echo "0 */12 * * * root test -x /bin/certbot && perl -e 'sleep int(rand(3600))' && /bin/certbot -q renew && /tmp/import-certificate 60" >> /etc/crontab
fi