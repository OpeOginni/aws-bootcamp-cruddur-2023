# Week 1 — App Containerization

## Week 1 Tasks

These are the tasks I completed during this week.

```
✅ Watched all Bootcamp Videos for the week
✅ Containerized my application (Docker files, Docker Compose)
✅ Containerized my application (Docker files, Docker Compose)
✅ Added Documentation for the Notification Endpoint on the OpenAI Document, Wrote a Flask Backend Endpoint for Notifactions and wrote a React Page for Notifications
✅ I ran DynamoDB Local Container and Postgres Container
✅ Added NPM install command to gitpod.yml
```
All these Individual tasks will be discussed below. I will state my process of completing the task, add screenshot proofs and give details about some issues I came across and how I debugged these issues for tasks that requires these information.

### ✅ Watched all Bootcamp Videos for the week

### ✅ Containerized my application (Docker files, Docker Compose)

- Created Docker Files for the Frontend and Backend
    - **[Frontend Docker File](https://github.com/OpeOginni/aws-bootcamp-cruddur-2023/blob/main/frontend-react-js/Dockerfile)**
    - **[Backend Docker File](https://github.com/OpeOginni/aws-bootcamp-cruddur-2023/blob/main/backend-flask/Dockerfile)**
- Built the Backend Docker File
<img src="screenshots/week1/week1_0.png" >

- Created Docker Compose File
    - **[Check out Docker Compose Code](https://github.com/OpeOginni/aws-bootcamp-cruddur-2023/blob/main/docker-compose.yml)**
- I ran the compose file and tested the app
<img src="screenshots/week1/week1_2.png" >

### ✅ Added Documentation for the Notification Endpoint on the OpenAI Document, Wrote a FLask Backend Endpoint for Notifactions and wrote a React Page for Notifications

- Commit that shows I Documented the Notification Endpoint in the OpenAI file: [commit 12091f5](https://github.com/OpeOginni/aws-bootcamp-cruddur-2023/commit/12091f574cd7e580342cc52971b7ad5a8070ede6)
- Created `notifications_activites.py` file: 
    - [notifications_activities.py](https://github.com/OpeOginni/aws-bootcamp-cruddur-2023/blob/main/backend-flask/services/notifications_activities.py)
    - Commit change creating the `/notifications` route in the `app.js` file: [commit 66e37c0](https://github.com/OpeOginni/aws-bootcamp-cruddur-2023/commit/66e37c0b62875f45a60fbbfad3e38da2729fcf98)
- Wrote a React Page for Notifications: [`NotificationsFeedPage.js`](https://github.com/OpeOginni/aws-bootcamp-cruddur-2023/blob/main/frontend-react-js/src/pages/NotificationsFeedPage.js)
<img src="screenshots/week1/week1_3.png" >

**Issues and Fixes**

- I encountered a 404 error when trying to view the notifications page. I did some debugging and found out I had not assigned the correct route to display the notification page. I used the route `/` instead of `/notifications`. I made use of the browser console to do my debugging, so i easily fixed the big.

### ✅ I ran DynamoDB Local Container and Postgres Container
<img src="screenshots/week1/week1_4.png" >

## Homework Challenges

### ✅ Added NPM install command to gitpod.yml

- [Check out the commit](https://github.com/OpeOginni/aws-bootcamp-cruddur-2023/commit/2049edad4784d69ee4abfa296d2f6c386e041b1a) 




