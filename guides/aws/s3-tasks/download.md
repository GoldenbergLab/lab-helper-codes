# Guide to Downloading Data from AWS


There are few options to downloading:
You can only download one file at a time on S3 console. So you need to install the AWS client and use the command line or install a File Transfer software such as [CyberDuck](https://cyberduck.io/) in order to download more data at once.

<!-- toc -->
- You can only download **one file at a time on S3 console.** This is done by manually clicking the download function on the aws file
- **no terminal option** You can download multiple files with **[cyberduck](#downloading-with-cyberduck)**
- **download from terminal** you can use the aws command line **[interfece](#Command-line-interface)**

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

Generally speaking, aws has really good documentation on how to use their interface to connect to s3.

- **Instalation** The first thing you need to do is [install](https://docs.aws.amazon.com/cli/latest/userguide/install-cliv2-mac.html) the aws command line interface and make sure its connected to the lab s3.
- **Copy Files** in order to copy files to a local folder, the easiest thing is to go to that local folder in the terminal and use this code:

```
aws s3 cp s3://task-data-raw/NAME-OF-THE-FOLDER/ . --recursive
```

This code will copy all the files to your local library. 
