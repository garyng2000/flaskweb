#!/bin/bash
# this is a hack to restore the dynamically created certbot modified conf
cp /var/app/current/.platform/nginx/conf.d/*.conf /etc/nginx/conf.d/
systemctl restart nginx
# cleanup(for security reason)
rm -rf /var/app/current/.platform/nginx