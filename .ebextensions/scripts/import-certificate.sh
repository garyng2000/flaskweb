#/bin/bash
source /tmp/get-eb-info.sh > /dev/null
change_since=${1:-60}
cert_type=$(/opt/elasticbeanstalk/bin/get-config environment -k CERT_TYPE)
if [[ $cert_type != "production"]] || [[ $LOAD_BALANCER == "null" ]] || [[ $LOAD_BALANCER == "" ]]; then
	echo "not behind ELB or not production, nothing to import"
	exit 0
fi
#find /etc/letsencrypt -type f -mmin -$change_since
#cname=$(aws elasticbeanstalk describe-environments | jq -r --arg EnvironmentId "$environment_id" '.Environments[] | select(.EnvironmentId == $EnvironmentId) | .CNAME')
cname=$(echo $ENVIRONMENT_CNAME | tr '[:upper:]' '[:lower:]')
echo cname=$cname
if [ $cname != "" ]; then
#aws acm list-certificates --query "CertificateSummaryList" | jq -r --arg CNAME "$cname" '.[] | select(.DomainName==$CNAME) | .CertificateArn'
certificate_arn=$(aws acm list-certificates --query "CertificateSummaryList" | jq -r --arg CNAME "$cname" '.[] | select(.DomainName | test($CNAME;"i")) | .CertificateArn')
if [ "$certificate_arn" != "" ]; then
#echo "$certificate_arn"
re_import="--certificate-arn $certificate_arn"
fi
key_file=/etc/letsencrypt/live/$cname/privkey.pem
cert_file=/etc/letsencrypt/live/$cname/cert.pem
ca_file=/etc/letsencrypt/live/$cname/fullchain.pem
file_last_modified=$(find /etc/letsencrypt/live/$cname -type f -mmin -$change_since)
if [ "$re_import" = "" ] || [ "$file_last_modified" != "" ]; then
#disable for now, AWS has a strange limit on how many import is allowed each year!!!!
certificate_arn=$(aws acm import-certificate --certificate file://$cert_file --private-key file://$key_file --certificate-chain file://$ca_file $re_import | jq -r '.CertificateArn')
echo "certificate for $cname updated"
echo certificate_arn=$certificate_arn
else
echo "nothing changed for $cname within last $change_since minutes"
fi
fi
