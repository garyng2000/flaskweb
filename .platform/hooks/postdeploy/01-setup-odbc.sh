#!/bin/bash
if grep -E 'FreeTDS' /etc/odbcinst.ini; then
	echo 'freeTDS already setup in /etc/odbcinst.ini'
else
cat << EOF >> /etc/odbcinst.ini
[FreeTDS]
Description = Freetds v 1.2
Driver = /lib64/libtdsodbc.so.0
EOF
echo 'freeTDS setup done in /etc/odbcinst.ini'
fi

