Creating and running a task in S3

0. Make sure AWS is configured, which means your IAM user account is valid and working with permissions to create and edit buckets in S3.

Create buckets for task

1. Log into the AWS Console and navigate to S3.
2. For your new task, you’ll create 3 buckets. The goal of three buckets is to enforce phased development of tasks, as well as to provision data records based on the phase (i.e., pilot data should be saved to a folder for only this task’s pilot data). The three buckets are listed below (see following step for how to create and configure):
    1. <your-unique-bucket-name>-staging
    2. <your-unique-bucket-name>-pilot
    3. <your-unique-bucket-name>-production
3. To create a bucket, click the Create bucket button in the S3 console. You do this for each bucket name as in (2) above. Select US East (N. Virginia) us-east-1 as the region from the drop-down in General configuration.
4. You will uncheck the Block all public access box. This will allow public access to the bucket’s contents (i.e., the task).
5. Then select Enable under Bucket Versioning.
6. (Optional, but recommended) Add two tags to easily designate what phase of development a bucket is, and what kind of task it is (i.e., survey):
    1. {Key: environment, Value: phase}
    2. {Key: task-type, Value: type}
7. Click Create bucket and you will be brought back to the main S3 console.

Update bucket to host task

1. From the S3 console, click on the bucket name you want to update (i.e., <your-unique-bucket-name>-staging), which will bring you to the bucket’s configuration dashboard.
2. Click on Properties, and then select the Static website hosting card. 
3. It will expand, and you will select Use this bucket to host a website.
    1. It will prompt for an Index document, which you should call index.html, or whichever HTML file is the true index of your task. 
    2. (Optional, but recommended) Add an error.html file that AWS will route to in case of errors in server-side logic that happen from time to time.
    3. Click Save.
4. Now click on Permissions and then Bucket Policy.
5. A code block editor should appear, and inside of that, paste the following (note that <name-of-bucket> needs to be replaced by the actual name of your bucket!):

{
    "Version": "2012-10-17",
    "Statement": [
        {
            "Sid": "PublicRead",
            "Effect": "Allow",
            "Principal": "*",
            "Action": [
                "s3:GetObject",
                "s3:GetObjectVersion"
            ],
            "Resource": "arn:aws:s3:::<name-of-bucket>/*”
        }
    ]
}

6. Click Save and follow the prompt to confirm that this should be public.

