#!/bin/bash



## This script should only be used if you are 100% sure your Access Keys are only configued in your ~/.aws/credentials file.

# Verify an AWS user/profile was specified
if [ "$1" != "" ]; then
	profile=$1
else
        echo "You must specify an AWS user/profile in \$1"
        echo "$1 is blank!"
	exit 1

	
# Create list of access keys
echo -n "Create list of access keys from AWS API "
akm=$(aws iam list-access-keys --profile $profile)
akcnt=$(echo $akm | jq .AccessKeyMetadata[].AccessKeyId | wc -l)
echo "Got em!"
## DEBUG code
#echo BEGIN DEBUG
#echo $akcnt
#echo END DEBUG

echo Check that there is only one access key, fail if there are two

if [ "$akcnt" == "1"  ]; then
	echo "There is one access key"
	oldaki=$(echo $akm | jq -r .AccessKeyMetadata[].AccessKeyId)
	echo $oldaki

elif [ "$akcnt" == "2" ]; then
	echo "There are two access keys! Exiting"
	exit 1
else
	echo "The environment may not be sane! Exiting"
	exit 1
fi

echo -n "Create second access key "
newak=$(aws iam create-access-key --profile $profile)
access_key_id=$(echo $newak | jq -r .AccessKey.AccessKeyId)
secret_access_key=$(echo $newak | jq -r .AccessKey.SecretAccessKey)
echo "Got em!"

echo "Test new keys are correct length"
akiln=$(echo $access_key_id | wc -m )
sakln=$(echo $secret_access_key | wc -m)

if [ "$akiln" == "21" ];then
	echo "AccessKeyId is the correct length"
else
	echo "AccessKeyId is NOT the correct length"
	exit 1
fi

if [ "$sakln" == "41" ];then
	echo "SecretAccessKey is the correct length"
else
	echo "SecretAccessKey is NOT the correct length"
	exit 1
fi

## DEBUG code
#echo BEGIN DEBUG
#echo $newak
#echo $access_key_id
#echo $secret_access_key
#echo END DEBUG

echo "Backup existing access keys"
akbu=$(grep -A 2 $profile ~/.aws/credentials)

## DEBUG code
##echo BEGIN DEBUG
##echo "$akbu"
##echo END DEBUG

echo "Setting new access keys"
aws configure set aws_access_key_id $access_key_id --profile $profile
akiexit=$?

## DEBUG code
#echo BEGIN DEBUG
#echo $akiexit
#echo END DEBUG

aws configure set aws_secret_access_key $secret_access_key --profile $profile
sakexit=$?

## DEBUG code
#echo BEGIN DEBUG
#echo $sakexit
#echo END DEBUG

if [[ "$akiexit" == "0" && "$sakexit" == "0" ]]; then
	echo "Access Keys set successfully"
	echo "Deleting old keys"
	echo "aws iam delete-access-key --access-key-id $oldaki --profile $profile"
	aws iam delete-access-key --access-key-id $oldaki --profile $profile
else
	echo "There was a problem settting Access Keys!"
	echo "Here is the backup"
	echo "$akbu"
fi
