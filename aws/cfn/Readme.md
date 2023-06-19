## Architecture Guide

Before you run any templates, be sure to create an S3 Bucket to contain
all of our artifacts for CloudFormation.

```
aws s3 mk s3://cfn-artifacts-opeoginni
export CFN_BUCKET="cfn-artifacts-opeoginni"
gp env CFN_BUCKET="cfn-artifacts-opeoginni"
```

> remember bucket names are unique to the provide code example you may need to adjust