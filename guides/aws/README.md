# Amazon Web Services (AWS)

The following is a brief series of steps that should help get people up and
running with AWS. 

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

## AWS Lambda

### Introduction

- [What is AWS Lambda?](https://docs.aws.amazon.com/lambda/latest/dg/welcome.html)
- [Getting Started](https://docs.aws.amazon.com/lambda/latest/dg/getting-started.html)

### General Usage

**Important**: In order to use AWS Lambda with package dependencies, such as
the `tweet` package in Python, the command line interface `aws` must be installed on your
local machine. This is non-negotiable both for security purposes and for
package deployment. If you have not configured your CLI, please scroll back up
and do so before continuing on this section.

- [Using AWS Lambda with the AWS CLI](https://docs.aws.amazon.com/lambda/latest/dg/gettingstarted-awscli.html)

### Python

- [Building Lambda functions with Python](https://docs.aws.amazon.com/lambda/latest/dg/lambda-python.html)
