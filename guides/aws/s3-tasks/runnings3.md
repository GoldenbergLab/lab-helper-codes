# Guide to running a task on AWS

- Step 0: Make sure you have deployed the task. 

## Step 0 - make sure you have deployed the task.
Follow the guide to deploying s3 tasks here. Once you are finished, you should have a link to your task at your-task-here.hbssurvey.com. Only proceed once you have done this. 

## Step 1 - Check [AWS Status](https://status.aws.amazon.com/).
Make sure that "Amazon Cognito (N. Virginia)" is not experiencing errors. Double check to make sure that the save function is working and uploading data into the `task-data-raw` bucket. 

## Downloading task data

Outline: You can only download one file at a time on S3 console. So you need to install the aws client in order to effectively download more stuff
