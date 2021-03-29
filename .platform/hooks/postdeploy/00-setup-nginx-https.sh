#!/bin/bash
cert_type=$(/opt/elasticbeanstalk/bin/get-config environment -k CERT_TYPE)
if [[ $cert_type != "None" ]]; then
      #enable ssl redirection
      sed -i 's/set \$ssl N;/set $ssl Y;#changed by posthooks/' /etc/nginx/conf.d/http-https-proxy.conf
      systemctl restart nginx
fi
# this is a hack to restore the dynamically created certbot modified conf
#cp /tmp/nginx/conf.d/http*.conf /etc/nginx/conf.d/
#sed -i -e 's/default_type/server_names_hash_bucket_size 128;\n    default_type/' /etc/nginx/nginx.conf
#find /etc/nginx
#systemctl restart nginx
# cleanup(for security reason)
#rm -rf /var/app/current/.platform/nginx