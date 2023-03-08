# Week 2 — Distributed Tracing

## Week 2 Tasks

These are the tasks I completed during this week.

```
✅ Implemented HoneyComb
✅ Implemented X-Ray
✅ Implemented CloudWatch Logs to my App
✅ Added Subsegments, Annotations and Metadata to X-Ray Traces
```

### ✅ Implemented HoneyComb

Here is the [commit](https://github.com/OpeOginni/aws-bootcamp-cruddur-2023/commit/e9e01d653578a899e6959ecb969cd97fba198556) that shows the implementation of HoneyComb to my app.

***Proof Of the Task***

- Recent Traces displayed on the HoneyComb site

<img src="screenshots/week2/week2_9.png" width="600">

- Trace for Route `/api/activities/home`
<img src="screenshots/week2/week2_10.png">

- Trace for Route `/api/activities/notification` 
<img src="screenshots/week2/week2_11.png">


### ✅ Implemented X-Ray

***Proof Of the Task***

- Created X-Ray Group Using CLI
<img src="screenshots/week2/week2_0.png" width="600">

<img src="screenshots/week2/week2_1.png" >

- Created Sampling Rule

<img src="screenshots/week2/week2_2.png" width="600">

<img src="screenshots/week2/week2_3.png" width="600">

### ✅ Implemented CloudWatch Logs to my App

***Proof Of the Task***

- Log Group
<img src="screenshots/week2/week2_8.png" >

- Active Logs
<img src="screenshots/week2/week2_7.png" >

## Homework Challenges

### ✅ Implemented Subsegments, Annotations and Metadata from AWS X-Ray

For this task, I made use of the AWS Docs from there, I found some issues with Andrew's implementation of subsegments. Mainly I had to get rid of the `segment` declaration and also making use of the `xray_recorder.end_subsegment()` method.

I implemented subsegment in the notifications page, the [`notifications_activites.py`](https://github.com/OpeOginni/aws-bootcamp-cruddur-2023/blob/main/backend-flask/services/notifications_activities.py) file and in the [`user_activities.py`](https://github.com/OpeOginni/aws-bootcamp-cruddur-2023/blob/main/backend-flask/services/user_activities.py) file.

Here is the [Docs](https://docs.aws.amazon.com/xray/latest/devguide/xray-sdk-python-subsegments.html) I found during my research. 

Here is the [commit](https://github.com/OpeOginni/aws-bootcamp-cruddur-2023/commit/781e1b869ab1e903f7e661beda4c6b216467e179) of the implementation.

***Proof Of the Task***

- Trace Overview
<img src="screenshots/week2/week2_4.png" >

- Complete Trace Data
<img src="screenshots/week2/week2_5.png" width="600" >

- Part of Trace Data Showing **Subsegment, Annotations and Metadata**
<img src="screenshots/week2/week2_6.png" width="600" >


