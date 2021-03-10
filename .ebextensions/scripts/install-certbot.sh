#!/bin/bash
cert_type=$(/opt/elasticbeanstalk/bin/get-config environment -k CERT_TYPE)
cert_email=$(/opt/elasticbeanstalk/bin/get-config environment -k CERT_EMAIL)
cert_domain=$(/opt/elasticbeanstalk/bin/get-config environment -k CERT_DOMAIN)

if [[ "$cert_type" != "production" ]]; then
# !! --test-cert: REMOVE FOR PRODUCTION, use the staging server for the certificate !!
staging=--test-cert
fi
certbot $staging --debug --non-interactive --redirect --agree-tos --nginx --email ${cert_email} --domains ${cert_domain} --keep-until-expiring
#make the modified http-https-proxy.conf listen on 80/443(certbot make it 443 only which is not good for behind ALB
sed -i 's/listen 443 ssl;/listen 80; listen 443 ssl;/' /etc/nginx/conf.d/http-https-proxy.conf
#enable ssl redirection
sed -i 's/set \$ssl N;/set $ssl Y;/' /etc/nginx/conf.d/http-https-proxy.conf
#4. make a copy of the modified .conf to platform(disappeared after deploy !!, restore via postdeploy hook)
#mkdir -p /tmp/nginx/conf.d && cp -a /etc/nginx/conf.d/http-https-proxy.conf /tmp/nginx/conf.d/
#5 also save it to /tmp, urber important
cp -a /etc/nginx/conf.d/http-https-proxy.conf /tmp/  
[[ -e /etc/letsencrypt/live/${cert_domain} ]] && ln -nsf ${cert_domain} /etc/letsencrypt/live/default
