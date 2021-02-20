#!/bin/bash
# helper script to retrieve instance info say the external defined url
# this requires IAM access to ElasticBeanStalkResource(DescribeEnvironments) and EC2(DescribeTags)
# for getting EB environment info
# {
#     "Version": "2012-10-17",
#     "Statement": [
#         {
#             "Sid": "VisualEditor0",
#             "Effect": "Allow",
#             "Action": [
#                 "elasticbeanstalk:DescribeEnvironments",
#             ],
#             "Resource": "*"
#         }
#     ]
# }

# for retrieving EC2 instance related info
# {
#     "Version": "2012-10-17",
#     "Statement": [
#         {
#             "Sid": "VisualEditor0",
#             "Effect": "Allow",
#             "Action": "ec2:DescribeTags",
#             "Resource": "*"
#         }
#     ]
# }

region=$(curl -s http://169.254.169.254/latest/dynamic/instance-identity/document | jq -r '.region')
echo $region
export AWS_DEFAULT_REGION=$(cat /opt/elasticbeanstalk/config/ebenvinfo/region)
cat > /root/.aws/config  <<EOF
[default]
region = ${region}
EOF
instance_id=$(curl -s http://169.254.169.254/latest/meta-data/instance-id)
echo $instance_id
environment_id=$(cat /opt/elasticbeanstalk/config/ebenvinfo/envid)
#environment_id=$(aws ec2 describe-tags | jq -r --arg InstanceId "$instance_id" '.Tags[] | select(.ResourceType == "instance" and .Key == "elasticbeanstalk:environment-id" and .ResourceId == $InstanceId) | .Value')
echo $environment_id
cname=$(aws elasticbeanstalk describe-environments | jq -r --arg EnvironmentId "$environment_id" '.Environments[] | select(.EnvironmentId == $EnvironmentId) | .CNAME')
echo $cname

