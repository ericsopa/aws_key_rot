#!/usr/bin/python
import sys
import boto3
import subprocess

## This script should only be used if you are 100% sure your Access Keys are only configued in your ~/.aws/credentials file.

# Verify an AWS user/profile was specified
try:
    sys.argv[1]
except IndexError as error:
    print "You must specify an AWS user/profile in sys.argv[1]"
    print ("sys.argv[1] is blank!")
    quit()
else:
    profile = sys.argv[1]

# Function that lists keys
def keylst():
    global akm
    akm = iam_client.list_access_keys(
        UserName = profile
    )
    return

# Function that counts keys
def keycnt():
    global akcnt
    akcnt = len([access_key['AccessKeyId'] for access_key in akm['AccessKeyMetadata']])
    return

# Init IAM client
iam = boto3.resource('iam')    # for resource interface
iam_client = boto3.client('iam') # for client interface
user = iam.User(profile)

# Create list of access keys
print "Create list of access keys from AWS API "
keylst()
keycnt()

# Verify there is only one Access Key
if akcnt == 1:
    print "There is one acccess key"
    oldaki = ([access_key['AccessKeyId'] for access_key in akm['AccessKeyMetadata']])
elif akcnt == 2:
    print "There are two access keys! Exiting!"
    quit()
else:
    print "The environment is not sane! Exiting!"
    quit()

# Create new Access Key in AWS
print "Create second access key"
newak = user.create_access_key_pair()
access_key_id = (newak.id)
secret_access_key = (newak.secret)

# Rotate the Access Key where it's used
cmd=('aws configure set aws_access_key_id ' + str(access_key_id) + ' --profile ' + str(profile))
push=subprocess.Popen(cmd, shell=True, stdout = subprocess.PIPE)

cmd=('aws configure set aws_secret_access_key ' + str(secret_access_key) + ' --profile ' + str(profile))
push=subprocess.Popen(cmd, shell=True, stdout = subprocess.PIPE)

# Delete old Access Key in AWS
keylst()
keycnt()

if akcnt == 1:
    print "There is ONLY one acccess key! Create must have failed! Exiting"
    quit()
elif akcnt == 2:
    print "There are two access keys, deleting the old one..."
    response = iam_client.delete_access_key(
        UserName=profile,
        AccessKeyId=(oldaki[0])
    )
    retcode = response['ResponseMetadata']['HTTPStatusCode']
    if retcode == 200:
        print "Success! Old access key deleted!"
else:
    print "The environment is not sane! Exiting!"
    quit()
