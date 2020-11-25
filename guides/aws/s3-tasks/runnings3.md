# Guide to running a task on AWS

- Step 0: Make sure you have deployed the task. 

## Step 0 - make sure you have deployed the task.
Follow the guide to deploying s3 tasks here. Once you are finished, you should have a link to your task at your-task-here.hbssurvey.com. Only proceed once you have done this. 

## Step 1 - Check [AWS Status](https://status.aws.amazon.com/).
Make sure that "Amazon Cognito (N. Virginia)" is not experiencing errors. Double check to make sure that the save function is working and uploading data into the `task-data-raw` bucket. 

## Step 2 - Eliminate common human errors:
Common errors we've run into that we want you to avoid:
  - linked wrong Qualtrics
  - instructions are wrong
  - consent is wrong
  - functions do not work as intended. For example, a function to ensure that participants only enter numerical responses might also let participants enter no response without triggering an alert.
  
## Step 3 - Go through the task once
Go through your entire task once, download your AWS data, and make sure it is correct. Then check your Qualtrics survey.

## Step 4 - Run



## Step 5 - Downloading task data

Outline: You can only download one file at a time on S3 console. So you need to install the aws client in order to effectively download more stuff
