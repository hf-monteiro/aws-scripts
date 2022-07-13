# Prerequisites to run this scripts 
* [Install](https://docs.aws.amazon.com/cli/latest/userguide/getting-started-install.html) AWS CLI in the machines that will execute.
* To have or create a IAM user with the right permissions to create and manage the AWS resources.

## Configure AWS CLI
To do that, you gonna need to run the folowing command

1. With your IAM programmatically credentials, login to  AWS CLI running:
```shell
aws configure
 ```
2. After that, you just need to paste your credentials informations 
```shell
 aws_access_key_id=EXAMPLEINFO
 aws_secret_access_key=EXAMPLEINFO
 aws_session_token=EXAMPLEINFO
 ```