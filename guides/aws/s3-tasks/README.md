# Creating and running a task in S3

<!-- toc -->

- [Step 0](#step-0)
- [Create buckets for task](#create-buckets-for-task)
- [Uploading your task to S3](#uploading-your-task-to-s3)
- [Update bucket to host task](#update-bucket-to-host-task)
- [Syncing your task to its `task-data-raw`
  folder](#syncing-your-task-to-its-task-data-raw-folder)
- [Configuring a CloudFront deployment](#configuring-a-cloudfront-deployment)

<!-- tocstop -->

## Step 0

Make sure AWS is configured, which means your IAM user account is valid and
working with permissions to create and edit buckets in S3.

## Create buckets for task

1. Log into the AWS Console and navigate to S3.
2. For your new task, you’ll create **3 buckets**. The goal of three buckets is
to enforce phased development of tasks, as well as to provision data records
based on the phase (i.e., pilot data should be saved to a folder for only this
task’s pilot data). The three buckets are listed below (see following step for
how to create and configure):

    1. `<your-unique-bucket-name>-staging`
    2. `<your-unique-bucket-name>-pilot`
    3. `<your-unique-bucket-name>-production`
    
3. To create a bucket, click the **Create bucket** button in the S3 console.
You do this for each bucket name as in (2) above. Select **US East (N.
Virginia) us-east-1** as the region from the drop-down in **General
configuration**.
4. You will uncheck the **Block all public access** box. This will allow public
access to the bucket’s contents (i.e., the task).
5. Then select **Enable** under **Bucket Versioning**.
6. (Optional, but recommended) Add two tags to easily designate what phase of
development a bucket is, and what kind of task it is (i.e., survey):
    1. {Key: **environment**, Value: *phase*}
    2. {Key: **task-type**, Value: *type*}
7. Click **Create bucket** and you will be brought back to the main S3 console.
8. Your bucket is ready to be populated with the task and related requirements
(i.e., stimuli).

## Uploading your task to S3

1. On your computer, gather the task materials you will upload to S3. For
example, you may have a structure of files that looks like this:

```bash .  ├── external-html/ │   └── consent.html ├── index.html ├── jspsych/
└── stimuli/ ├── 1.jpg ├── 2.jpg └── 3.jpg ```

2. Click the **Upload** button, and you should be able to select all the above
files from (1) and drag-and-drop into the modal window.
3. Confirm that the files are correct and click **Upload**.

## Update bucket to host task

1. From the S3 console, click on the bucket name you want to update (i.e.,
`<your-unique-bucket-name>-staging`), which will bring you to the bucket’s
configuration dashboard.
2. Click on **Properties**, and then select the **Static website hosting**
card. 
3. It will expand, and you will select **Use this bucket to host a website**.
    1. It will prompt for an **Index document**, which you should call
`index.html`, or whichever HTML file is the true index of your task. 
    2. (Optional, but recommended) Add an `error.html` file that AWS will route
to in case of errors in server-side logic that happen from time to time.
    3. Click **Save**.
4. Now click on **Permissions** and then **Bucket Policy**.
5. A code block editor should appear, and inside of that, paste the following
(note that `<name-of-bucket>` needs to be replaced by the actual name of your
bucket!): ``` { "Version": "2012-10-17", "Statement": [ { "Sid": "PublicRead",
"Effect": "Allow", "Principal": "*", "Action": [ "s3:GetObject",
"s3:GetObjectVersion" ], "Resource": "arn:aws:s3:::<name-of-bucket>/*”
} ] } ```
6. Click **Save** and follow the prompt to confirm that this should be public.
7. Your bucket is ready to configure with CloudFront.

## Syncing your task to its `task-data-raw` folder

Our S3 service has a variety of buckets, but the bucket we save data to will be
the same bucket for all tasks. It's named `task-data-raw`. The only change will
be which _folder_ of the bucket, where that folder will have the same name as
the bucket of the task. So if the task is called
`fun-new-task-with-a-twist-production`, we save data to a folder located
within-bucket: `task-data-raw/fun-new-task-with-a-twist-production`.

To save data from a task, whether it is in staging, pilot, or production, you
must use the [AWS Browser SDK](https://aws.amazon.com/sdk-for-browser/). In
particular, we need this SDK to link to both Cognito and S3 from the task.
There are two ways to use the SDK. The most common way this lab will import the
script is through a direct script link in the main HTML file:

``` <script src="https://sdk.amazonaws.com/js/aws-sdk-2.713.0.min.js"></script>
```

The following JavaScript code block can be configured within another script for
any browser-based task:

``` 

/*
 * You must use this cognitoIdentityPool string value and 
 * the "task-data-raw" value for the DIRECTORY. The BUCKET value
 * will change based on the task.
 */

const cognitoIdentityPool = "us-east-1:0f699842-4091-432f-8b93-a2d4b7bb5f20";
const DIRECTORY = "task-data-raw"; const BUCKET = your-awesome-task-bucket;
const BUCKET = "your-bucket-name-goes-here";

/*
 * Save data at any point to S3 using this function.
 * It takes as arguments the string identifier of a participant
 * and the data in CSV form from the jsPsych data getter.  
 */ 

function saveDataToS3(id, csv) {

  AWS.config.update({
    region: "us-east-1", 
    credentials: new AWS.CognitoIdentityCredentials({
      IdentityPoolId: cognitoIdentityPool 
    }), 
  });

  // You can change anything after the first `/` here, but only if
  // you know the intended behavior of changing this.
  const filename = `${DIRECTORY}/${id}.csv`;

  const bucket = new AWS.S3({
    params: { Bucket: BUCKET }, 
    apiVersion: "2006-03-01", 
  })

  const objParams = { 
    Key: filename, 
    Body: csv 
  }

  bucket.putObject(objParams, function(err, data) { 
    if (err) { 
      console.log("Error: ", err.message); 
    } else {
      console.log("Data: ", data); 
    } 
  });


} ```

You will then reference this saving function within `on_finish` tags within
your jsPsych timeline when you would like to write data to S3. Remember to pass
in a participant identifier and the data to be saved in CSV format.

## Configuring a CloudFront deployment

