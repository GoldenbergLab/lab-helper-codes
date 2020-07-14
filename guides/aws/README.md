# Amazon Web Services (AWS)

The following is a brief series of steps that should help get people up and
running with AWS. 

## Administration

As useful as AWS is, the developer community considers it a necessary evil.
Rightfully so, as using it can be painstaking and full of errors before the 
first sign of success. Major aspects of using AWS rely on setup and
configuration: creating a root account, IAM users and groups, security
credentials, and so on. Once these are set, and with well-defined naming
conventions, the administrative evil can be somewhat bypassed with future use.

## Command Line Interface (CLI)

### Installation

- [MacOS](https://docs.aws.amazon.com/cli/latest/userguide/install-cliv2-mac.html)

### Configuration

- [Basic](https://docs.aws.amazon.com/cli/latest/userguide/cli-configure-quickstart.html)

Note the use of a _named profile_ for credentials associated directly with
a particular project or group (i.e., the lab). This configuration is made via

```
aws configure --profile profilename
```

where _profilename_ is replaced with the intended name of that user profile for
AWS access configuration.

You can both check for existence and view for certainty the configuration and
credentials (do NOT make changes to these files directly):

#### Check configuration

```
open ~/.aws/config
```

#### Check credentials

```
open ~/.aws/credentials
```

## Amazon S3

### Introduction

- [What is Amazon S3?](https://docs.aws.amazon.com/AmazonS3/latest/dev/Welcome.html)
- [Getting Started](https://docs.aws.amazon.com/AmazonS3/latest/gsg/GetStartedWithS3.html)

### General Usage with AWS CLI

- [Using high-level (s3) commands with the AWS CLI](https://docs.aws.amazon.com/cli/latest/userguide/cli-services-s3-commands.html)
- [Using API-Level (s3api) commands with the AWS CLI](https://docs.aws.amazon.com/cli/latest/userguide/cli-services-s3-apicommands.html)

Creating your first bucket from the command line, assuming proper permissions,
should be straightforward with `aws s3api`:

```
aws s3api create-bucket --bucket mytest-bucket
```

where _mytest-bucket_ is the name of the bucket you'd like to create. This is
made at the default location of your AWS profile configuration. If you'd like
to specify a location, include `LocationConstraint=location` as an option on
the command. The _location_ can be one of these 
[regions under the 'Code' column](https://docs.aws.amazon.com/general/latest/gr/rande.html#regional-endpoints). A succesful response of this command to create buckets will look like

```
{
    "Location": "/mytest-bucket"
}
```

## AWS Lambda

### Introduction

- [What is AWS Lambda?](https://docs.aws.amazon.com/lambda/latest/dg/welcome.html)
- [Getting Started](https://docs.aws.amazon.com/lambda/latest/dg/getting-started.html)

### General Usage with AWS CLI

**Important**: In order to use AWS Lambda with package dependencies, such as
the `tweepy` package in Python, the command line interface `aws` must be installed on your
local machine. This is non-negotiable both for security purposes and for
package deployment. If you have not configured your CLI, please scroll back up
and do so before continuing on this section.

- [Using AWS Lambda with the AWS CLI](https://docs.aws.amazon.com/lambda/latest/dg/gettingstarted-awscli.html)
- [Using AWS Lambda with with Amazon S3](https://docs.aws.amazon.com/lambda/latest/dg/with-s3-example.html)

### Python

- [Building Lambda functions with Python](https://docs.aws.amazon.com/lambda/latest/dg/lambda-python.html)
