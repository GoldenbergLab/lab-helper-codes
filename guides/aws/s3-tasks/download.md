# Guide to running a task on AWS

Summary

<!-- toc -->
- [Download data with cyberduck](#step-5---downloading-with-cyberduck)
    * [Cyberduck tutorial](#cyberduck-tutorial)

<!-- tocstop -->


## Step 5 - Downloading with Cyberduck

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
