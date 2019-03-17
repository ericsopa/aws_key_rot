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

def keylst():
    global akm
    akm = iam_client.list_access_keys(
        UserName = profile
    )
    return

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
#akm = iam_client.list_access_keys(
#    UserName=profile
#)
## BEGIN DEBUG CODE
#print "BEGIN DECODE OUTPUT"
#print(akm) # print entire object
#print "END DECODE OUTPUT"
## END DEBUG CODE
keycnt()
#akcnt = len([access_key['AccessKeyId'] for access_key in akm['AccessKeyMetadata']])
## BEGIN DEBUG CODE
#print "BEGIN DECODE OUTPUT"
#print (akcnt)
#print "END DECODE OUTPUT"
## END DEBUG CODE

if akcnt == 1:
    print "There is one acccess key"
    oldaki = ([access_key['AccessKeyId'] for access_key in akm['AccessKeyMetadata']])
elif akcnt == 2:
    print "There are two access keys! Exiting!"
    quit()
else:
    print "The environment is not sane! Exiting!"
    quit()
# BEGIN DEBUG CODE
#print "BEGIN DECODE OUTPUT"
#print (oldaki)
#print "END DECODE OUTPUT"
# END DEBUG CODE

print "Create second access key"
newak = user.create_access_key_pair()
print (newak)

access_key_id = (newak.id)
secret_access_key = (newak.secret)

print (access_key_id)
print (secret_access_key)

cmd=('aws configure set aws_access_key_id ' + str(access_key_id) + ' --profile ' + str(profile))
print (cmd)
push=subprocess.Popen(cmd, shell=True, stdout = subprocess.PIPE)
print push.returncode

cmd=('aws configure set aws_secret_access_key ' + str(secret_access_key) + ' --profile ' + str(profile))
print (cmd)
push=subprocess.Popen(cmd, shell=True, stdout = subprocess.PIPE)
print push.returncode

# Create list of access keys
keylst()
keycnt()
#akm = iam_client.list_access_keys(
#    UserName=profile
#)
#akcnt = len([access_key['AccessKeyId'] for access_key in akm['AccessKeyMetadata']])

if akcnt == 1:
    print "There is ONLY one acccess key! Create must have failed! Exiting"
    quit()
elif akcnt == 2:
    print "There are two access keys, deleting the old one..."
    response = iam_client.delete_access_key(
        UserName=profile,
        AccessKeyId=(oldaki[0])
    )
    print (response)
else:
    print "The environment is not sane! Exiting!"
    quit()
