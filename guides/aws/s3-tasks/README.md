# Creating and running a task in S3

<!-- toc -->

- [Step 0](#step-0)
- [Create buckets for task](#create-buckets-for-task)
- [Uploading your task to S3](#uploading-your-task-to-s3)
- [Update bucket to host task](#update-bucket-to-host-task)
- [Syncing your task to its `task-data-raw`
  folder](#syncing-your-task-to-its-task-data-raw-folder)
- [Configuring a CloudFront deployment](#configuring-a-cloudfront-deployment)
- [Downloading task data](#downloading-task-data)
- [Specific task variations](#specific-task-variations)

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

```bash 
.  
├── external-html/ 
│   └── consent.html 
├── index.html 
├── jspsych/
└── stimuli/ 
  ├── 1.jpg 
  ├── 2.jpg 
  └── 3.jpg 
```

2. Click the **Upload** button, and you should be able to select all the above
files from (1) and drag-and-drop into the modal window. IMPORTANT: **if you don't drag and drop, AWS WIll NOT upload your folders. That means any img/, jspsych/, etc will not be in the bucket, resulting in a broken website.**
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
bucket!): 

``` 
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
      "Resource": "arn:aws:s3:::<name-of-bucket>/*"
    } 
  ] 
} 
```

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

``` 
<script src="https://sdk.amazonaws.com/js/aws-sdk-2.713.0.min.js"></script>
```

The following JavaScript code block can be configured within another script for
any browser-based task:

``` 

/*
 * You must use this cognitoIdentityPool string value and 
 * the "task-data-raw" value for DATA_BUCKET. The DIRECTORY value
 * will change based on the task.
 */

const cognitoIdentityPool = "us-east-1:0f699842-4091-432f-8b93-a2d4b7bb5f20";
const DATA_BUCKET = "task-data-raw";
const DIRECTORY = "your-task-bucket-name-with-stage-goes-here";

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
    params: { Bucket: DATA_BUCKET }, 
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


}
```

You will then reference this saving function within `on_finish` tags within
your jsPsych timeline when you would like to write data to S3. Remember to pass
in a participant identifier and the data to be saved in CSV format. This will 
look like:

```
...,
on_finish: function() {

  const id = "<whatever-the-subject-id-is>"
  const csv = jsPsych.data.get().csv()
  
  saveDataToS3(id, csv)
  
}
...
```

It's _very_ important that you follow this pattern. The `on_finish` piece of jsPsych
structures should use a generic function that _contains_ the `saveDataToS3` function.

## Configuring a CloudFront deployment

Now, you must create a CloudFront distribution for the S3 bucket, which will deploy
the bucket's contents and publish the task.

1. Navigate to the CloudFront service from the AWS Console.
2. Click **Create Distribution** and then press **Get Started** under the "Web"
   method of content delivery.
3. Paste the endpoint (web address) of your task's S3 bucket in the field called **Origin Domain Name**.
4. Where it asks for **Viewer Protocol Policy**, select **Redirect HTTP to HTTPS**.
5. For the dropdown selector called **Cache Policy**, select **Managed-CachingDisabled**.
6. For the option **Compress Objects Automatically**, select **Yes**.
7. You must make an **Alternate Domain Name (CNAME)** to link it to our lab's study web domain. To do so,
   you will include text describing your task, such as `example-task-name-and-phase.hbssurvey.com`.
8. For **SSL Certificate**, select **Custom SSL Certificate (example.com)**. Then select
   from the dropdown `*.hbssurvey.com (a715bbbd-ad62-49a0-8c75-9fdb9d542633)`
9. Submit by choosing **Create Distribution** again.

Once these steps are completing, AWS will begin deploying the task. It can take up to a few
hours to finish deploying depending on how busy AWS's deployment queue is. Typically, however,
it should be less than ten minutes. Once ready, you'll be able to navigate to your deployed
task website.

This website will soon be customized for our lab (see point 7. above), but for now, you will
find the task at a domain of type: `*.cloudfront.net`.

## Configuring task web domain on Route 53

With a CloudFront deployment of a task, the final step to making it ready for participants
is to create a subdomain on our lab's study domain (e.g., `new-task-name-and-phase.hbssurvey.com`).
You will need your CloudFront deployment's URL to complete this step. The URL will look similar to
`dbmsd35c91.cloudfront.net`.


1. Navigate to the Route 53 service from the AWS Console.
2. Click **Hosted zones**, and then click the **hbssurvey.com** domain link in the table.
3. A list in a table called "Records" will appear. Click **Create record**.
4. When prompted to "Choose routing policy", select **Simple routing** and click **Next**.
5. Configure **two** separate records, *A* and *AAAA*. Do the following to create each:
  a. Click **Define simple record**.
  b. For "Record name", write the subdomain for the task and phase. This should _match exactly_ the
     name you give to the CloudFront distribution `new-task-name-and-phase`.
  c. For "Value/Route traffic to", select "Alias to CloudFront distribution". It should automatically
     fill in "US East (N. Virginia)" for the region. Then, "Choose distribution" will provide in a dropdown
     the names of CloudFront distributions that are equipped for the _exact name_ used as a CNAME in the previous
     set of steps. The distribution you should match the CloudFront URL (i.e., `dbmsd35c91.cloudfront.net`).
  d. Select for "Record type" either **A** or **AAAA**, or whichever of these two you have not yet done.
6. Finally, click **Create records**.

## Downloading task data

Outline: You can only download one file at a time on S3 console. So you need to install the aws client in order to effectively download more stuff

## Specific task variations

### Sequential Tasks

1. Make sure function saveDataToS3 is in the functions.js file and not the main html file.

2. Modify the function so that id refers to the global Face.ID variable and so that the function can be called without passing in arguments.

```
function saveDataToS3() {


  id = Face.ID
  csv = jsPsych.data.get().csv()

  AWS.config.update({
    region: "us-east-1", 
    credentials: new AWS.CognitoIdentityCredentials({
      IdentityPoolId: cognitoIdentityPool 
    }), 
  });

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


} 
```
3. Modify the following variables to contain the saveDataToS3 function. Not that sometimes the function fails to work with on_finish and instead we use on_start.

``` 
var imageDescription = {
    type: 'survey-text',
    questions: [{prompt: "Please describe the picture in your own words"}],
    preamble: function() {
      var curr_stim = imageTestDescription.shift()
      return '<img src='+curr_stim+'></img>';
    },
    on_finish: function(data){
      saveDataToS3()
      Face.description = JSON.parse(data.responses).Q0; } //save description
  };


var attentionCheck = { //function for the attention check
    timeline: [askTypeWord],
    loop_function: checkTyping,
    on_start: function(data){
      saveDataToS3()}
  };

  var connectSurvey = {
      type: 'image-button-response',
      stimulus: "",
      choices: ['Begin Survey'],
      on_finish: function(data){
      saveDataToS3()}
  };
  ```

4. Final notes of modifications: make new distinction between EU and US consent, get rid of references to checkUser function (temporarily until we construct a new one), change the order of items pushed into collective_emotion_estimation

```
var participant_id = { //to check if participants have entered ID (number/character, no punctuation allowed)
    timeline: [enter_id],
    loop_function: checkID,
    // loop_function: checkUser
  };
  
collective_emotion_estimation.push(checkPhone, participant_id, imageDescription);
```
