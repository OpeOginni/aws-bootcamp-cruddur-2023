# Week X — Cleanup

## Week X Tasks

These are the tasks I completed during the last week of the bootcamp.

```
✅ Sync tool for static website hosting (Hosting Frontend on CloudFront)
✅ Reconnected the DB and Postgre Confirmation Lambda
✅ Fixed CORS to use domain name for web-app
✅ Ensure CI/CD pipeline works and create activity works		
```

### ✅ Sync tool for static website hosting (Hosting Frontend on CloudFront)

- First off we created a Static Build Script for building the frontend on cloud-front. [**Check out Commit**](https://github.com/OpeOginni/aws-bootcamp-cruddur-2023/commit/d81bc78397b8cba0c9f02756e76c556b1ee0dd42#diff-a404a57eef73276ef9d2af5eaf105d2f7e316b4999078e89d1ed1bd47cc00704)
- I then Unzipped the the build folder and uploaded it to the CloudFront s3 bucket.
- Next, I created a sync ruby script for the static site S3-Bucker, with an extra sync.env file that holds extra environment variables for updating the static cloudfront site. [**Check out Commit**](https://github.com/OpeOginni/aws-bootcamp-cruddur-2023/commit/d825f1ca947e33c43a320f339eb63392c640716f#diff-9404828f7a16807d6d3d6e6fb5f7fbb0197fd084127ab97b25b112906965c634)
- I used CFN to create a CrdSyncStack
- Finnally created and added a role to the CrdSyncStack to give access to updated the static Site S3 Bucket

***Proof Of Task***

**Cloudfront Static Site working**

<img src="screenshots/weekX/weekX_0.png" width="800" >

**CrdSyncRole CFN Stack**

<img src="screenshots/weekX/weekX_1.png" width="800" >

**CrdSyncRole Stack Role for acceccing the Static Site S3 Bucket**

<img src="screenshots/weekX/weekX_2.png" width="800" >

### ✅ Reconnected the DB and Postgre Confirmation Lambda

- Removed the Python Flask Service from running on Debug Mode. [**Check out Commit**](https://github.com/OpeOginni/aws-bootcamp-cruddur-2023/commit/0b6ad62ef6a131a884c3a4d8f3e88e955519f22a). I didnt have to delete the Stack like Mr Andrew did, instead after building the prod container with the --no-debug tag added, I pushed the new image to ECR and made and executed a change set to the CFN template, and just waited, the conainer ended up being healthy.
- Updated my Environment Variables to use the datails from the new Cruddur Database Instance made with CFN, so we can connect to the DB using our scripts on GITPOD.
- I loaded the Schema and Migration to the Production DB Instance.
- Set Up error handling page in the CFN template. [**Check out Commit**](https://github.com/OpeOginni/aws-bootcamp-cruddur-2023/commit/49999c4e7d1845989755c8223cea8d98ada91926)
- My lambda code already creates a user object in the Dtabase corretly, so I did not hsve sny errord in creating Cruds. [`aws/lambdas/cruddur-post-confirmation.py`](https://github.com/OpeOginni/aws-bootcamp-cruddur-2023/blob/main/aws/lambdas/cruddur-post-confirmation.py)

***Proof Of Task***

**Created SG for Post Confirmation Lambda to connect to our DB**

<img src="screenshots/weekX/weekX_3.png" width="800" >

**Working Backend after connectin Production Database and Loading the Schema**

<img src="screenshots/weekX/weekX_4.png" width="800" >

### ✅ Fixed CORS to use domain name for web-app

### ✅ Ensure CI/CD pipeline works and create activity works

- I have already made an implementation for users creating activities that showcased their original name and username, not the hardcoded one. [`backend-flask/app.py`](https://github.com/OpeOginni/aws-bootcamp-cruddur-2023/blob/main/backend-flask/app.py#L282)
- I fixed the CICD pipeline CFN template. **Check out Commits**[Fixed the config param](https://github.com/OpeOginni/aws-bootcamp-cruddur-2023/commit/7ca838ef265fadd8299406d6af68f19a53e9b474), [Fixed codebuild name](https://github.com/OpeOginni/aws-bootcamp-cruddur-2023/commit/d08386856378c655de535b411a058f20ae65f148),[Week-X CICD Pipeline and Create Activity](https://github.com/OpeOginni/aws-bootcamp-cruddur-2023/commit/4f10000da861b5672517c491f38b2320e6c89e9a)
