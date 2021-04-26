# Guide to running a task on AWS

- Step 0: Make sure you have deployed the task. Is your-task-here.hbssurvey.com up and running? 
- Step 1: Check [AWS status](https://status.aws.amazon.com/). 
- Step 2: Eliminate common human errors
- Step 3: Go through the task once


## Step 0 - make sure you have deployed the task.
Follow the guide to deploying s3 tasks here. Once you are finished, you should have a link to your task at `your-task-here.hbssurvey.com`. 

## Step 1 - Check [AWS Status](https://status.aws.amazon.com/).
Make sure that "Amazon Cognito (N. Virginia)" is not experiencing errors. Double check to make sure that the save function is working and uploading data into the `task-data-raw` bucket. 

## Step 2 - Eliminate common human errors:
Common errors:

  - linked wrong Qualtrics
  - instructions are wrong
  - consent is wrong
  - functions do not work as intended. For example, a function to ensure that participants only enter numerical responses might also let participants enter no response without triggering an alert.
  
## Step 3 - Go through the task once
Go through your entire task once. Make mistakes and ensure that your checker functions (such as response length, attention checks, etc) are working properly.

Download your AWS data, and make sure it is correct. Then check your Qualtrics survey.

## Step 4 - Run

Start the task in Prolific, MTurk or the service you are using.

## Step 5 - Downloading task data

Outline: You can only download one file at a time on S3 console. So you need to install the AWS client or a File Transfer software such as [CyberDuck](https://cyberduck.io/) in order to effectively download more
