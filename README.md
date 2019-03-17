# aws_key_rot
Collection of code for rotating long term access keys

This code supports three use cases for long term access key rotation:
 1. ~/.aws/credentials file
 1. AWS Secrets Manager service
 1. Jenkins
 
Assumptions:
 - AWS IAM user only has one long term access key
 - Current Access Key will be deleted immediately after new one is created
 - AWS IAM Username and credential file profile are the same value
 
 ## AWS CLI Credentials File
 ### credfile.py
 ```
 $ ./credfile.py <profile/username>
 ```
 ## AWS Secrets Manager
 CloudFormation Template that creates a stack set starting from zero
  - AWS IAM User
  - AWS IAM User Access Key
  - AWS IAM Role for Lambda
  - AWS IAM Managed Policy for Lambda Role
  - AWS KMS key
  - AWS Secrets Manager Secret
  - AWS Lambda function to rotate Access Keys for user in Secrets Manager encrypted with the KMS key
  - Create the CloudFormation Stack Set
  - Rotate Access Key
 
 ## Jenkins
 ### awskeyrot.sh
 Bash script that rotates the AWS IAM User Access Keys stored in Jenkins
