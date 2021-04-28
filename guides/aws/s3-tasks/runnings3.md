# Guide to running a task on AWS

Summary

<!-- toc -->

- [Step 0: Make sure you have deployed the task](#step-0---make-sure-you-have-deployed-the-task)
- [Step 1: Check AWS Status](#step-1---check-aws-status)
- [Step 2: Eliminate common human errors](#step-2---eliminate-common-human-errors)
- [Step 3: Go through the task once](#step-3---go-through-the-task-once)
- [Step 4: Run](#step-4---run)
- [Step 5: Download data](#step-5---downloading-task-data)
    * [Cyberduck tutorial](#cyberduck-tutorial)

<!-- tocstop -->


## Step 0 - make sure you have deployed the task.
Follow the guide to deploying s3 tasks here. Once you are finished, you should have a link to your task at `your-task-here.hbssurvey.com`. 

## Step 1 - Check [AWS Status](https://status.aws.amazon.com/).
Make sure that "Amazon Cognito (N. Virginia)" is not experiencing errors. Double check to make sure that the save function is working and uploading data into the `task-data-raw` bucket. 

## Step 2 - Eliminate common human errors:

  - linked wrong Qualtrics
  - instructions are wrong / inaccurate
  - consent is wrong / inaccurate
  - functions do not work as intended. For example, a function to ensure that participants only enter numerical responses might also let participants enter no response without triggering an alert.
  
## Step 3 - Go through the task once
Go through your entire task once. Make mistakes and ensure that your checker functions (such as response length, attention checks, etc) are working properly.

Download your AWS data, and make sure it is correct. A correct AWS data has recorded all of the stimuli (and not skipped any trials).

Then check your Qualtrics survey and make sure that your data was recorded.

## Step 4 - Run

Start the task in Prolific, MTurk or the service you are using.

## Step 5 - Downloading task data

Outline: You can only download one file at a time on S3 console. So you need to install the AWS client and use the command line or install a File Transfer software such as [CyberDuck](https://cyberduck.io/) in order to download more data at once.

### Cyberduck tutorial

1. Download the version of [CyberDuck](https://cyberduck.io/) appropriate for your browser.
2. Make sure that you have an AWS access key. If you are unable to follow the steps below, feel free to contact Zi and she will make you one:
 
    - Navigate to the AWS site. Search for "IAM".
    - Press "Users."
    - Click on your own username
    - Go to the "Security credentials" tab
    - Create a new access key

3. In Cyberduck, open a new connection. Select AmazonS3.
4. Enter your access credentials. 
5. Congratulations! You can now transfer files between your computer and S3 via the CyberDuck interface.
