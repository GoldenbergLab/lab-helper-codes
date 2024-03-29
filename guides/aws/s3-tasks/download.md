# Guide to Downloading Data from AWS

<!-- toc -->
- You can only download **one file at a time on S3 console.** This is done by *manually clicking* the download function on the aws file
- **No terminal option** You can download multiple files with **[Cyberduck](#downloading-with-cyberduck)**
- **Download from terminal** you can use the aws command line **[interface](#Command-line-interface)**

For setting up your AWS infrastructure go to **[run](/guides/aws/s3-tasks/runnings3.md)** 


<!-- tocstop -->

## Downloading with Cyberduck

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


## Command Line Interface

We have an extensive .R code which downloads data automatically into your system. Find the template repository [here.](https://github.com/GoldenbergLab/r-project-template-no-enviroment-control) 

AWS has good documentation on how to use their interface to connect to s3.

- **Installation** The first thing you need to do is [install](https://docs.aws.amazon.com/cli/latest/userguide/install-cliv2-mac.html) the aws command line interface and make sure its connected to the lab s3.
- **Copy Files** in order to copy files to a local folder, the easiest thing is to go to that local folder in the terminal and use this code:

```
aws s3 cp s3://task-data-raw/NAME-OF-THE-FOLDER/ . --recursive
```

This code will copy all the files to your local library.
