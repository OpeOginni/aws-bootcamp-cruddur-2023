# Week 0 — Billing and Architecture

## Week 0 Tasks

These are the tasks I completed during this week.

```
✅ Set up MFA for Root Account and create IAM role
✅ Set up 2 AWS Budget
✅ Generated AWS Credentials
✅ Used and Tested CloudShell
✅ Installed the AWS CLI on Gitpod and added my AWS Credentials
✅ Used the CLI from Gitpod to create a Budget and a Billing Alarm
✅ Created a Conceptual Architecture Diagram on a Napkin
✅ Created an architectural diagram the CI/CD logical pipeline in Lucid Charts
✅ Reviewed all the questions of each pillars in the Well Architected Tool
✅ Did some research on the technical and service limits of specific services and how they could impact the technical path for technical flexibility
✅ Open a support ticket and request a service limit
✅ Used EventBridge to hookup Health Dashboard to SNS and send notification when there is a service health issue
```
All these Individual tasks will be discussed below. I will state my process of completing the task, add screenshot proofs and give details about some issues I came across and how I debugged these issues for tasks that requires these information.

### ✅ Set up MFA for Root Account and create IAM role

- Added MFA for my Root Account using Authy
- Created new User and added that user to an 'admin' user group
- Added MFA for my new 'admin' user

<img src="screenshots/week0/week0_1.png" >

### ✅ Set up 2 AWS Budget

For this task I created 2 separate Budgets, one for Credits use and the other was created using the CLI and covers all forms of spending.

<img src="screenshots/week0/week0_2.png" >

**As proof, here is an alert I got after creating a ZeroSpend Budget**

<img src="screenshots/week0/week0_3.png" >

I deleted it to create other test budgets.


### ✅ Generated AWS Credentials
- Generated Access Keys
- Gave it a description of "My New Access Key"
- Downloaded and saved the .csv file

### ✅ Used and Tested CloudShell

<img src="screenshots/week0/week0_4.png" width="600">


### ✅ Installed the AWS CLI on Gitpod and added my AWS Credentials

<img src="screenshots/week0/week0_5.png" width="600">

<img src="screenshots/week0/week0_credentials.png" width="600">

#### Bugs and Fixes
For this task I ran through some bugs
- First bug was that the terminal wis giving me the wrong outputs after running `aws budgets create-budget`. I solved this bug by correctly naming my `budget-notifiactions-with-subscriber.json` file.
- After solving this bug I was still reciving the wrong out put from the terminal, after looking at the error, I found out that I hadn't properly exported my `ACCOUNT_ID` to an environment variable. I solved this bug by running the command `export ACCOUNT_ID = $(aws sts get-caller-identiy --query Account --output text)`

### ✅ Used the CLI from Gitpod to create a Budget and a Billing Alarm

- Created an sns topic from the CLI using gitpod with the command `aws sns create-topic --name CLI-generated-billing-alarm`

**Proof is in the commits made to the code 🚀**

- **SNS Confirmation**
<img src="screenshots/week0/week0_7.png" width="600" >

- **CloudWatch Alarm**
<img src="screenshots/week0/week0_8.png" >

### ✅ Created a Conceptual Architecture Diagram on a Napkin
<img src="screenshots/week0/week0_9.jpeg" >

### ✅ Created an architectural diagram the CI/CD logical pipeline in Lucid Charts
<img src="screenshots/week0/week0_10.png" >


