# Automatic Image Content Moderation and Reporting System
## Objective
The goal of this project is to build an automated system that moderates user-uploaded images for inappropriate content using AWS services. It ensures that all uploaded images comply with safety and ethical guidelines, providing a seamless and secure experience for users and administrators.
## Background
Content moderation is crucial in platforms where users can upload media. Manually reviewing content is time-intensive and prone to human error. This project leverages AWS services to automate the detection of inappropriate content (e.g., violence, explicit material) and provides a mechanism to notify stakeholders and store moderation results for future reference.
## Description
This system uses a serverless architecture to analyze user-uploaded images in real-time. Users upload images to an S3 bucket (frontend interface). AWS Lambda triggers AWS Rekognition to scan the images for inappropriate content. If detected, the system sends an alert email via SES and stores the image metadata and results in DynamoDB. This data can be used for moderation reports and decision-making.
## Architecture:

## Workflow
Image Upload:
Users upload images to an S3 bucket using the S3 web interface as the frontend. Content Analysis:
An S3 event triggers a Lambda function when a new image is uploaded. The Lambda function uses AWS Rekognition to analyze the image for inappropriate content. Alert Notification:
If inappropriate content is detected, the system triggers an alert via Amazon SES to notify administrators or users. Result Storage:
The image metadata, along with the moderation result (safe/unsafe), is stored in a DynamoDB table for logging and reporting. Compliance & Moderation:
The data stored in DynamoDB can be used to generate moderation reports and improve compliance with platform policies.
## Tech Stack
Frontend S3: Serves as the frontend for uploading images. Backend & Moderation Logic AWS Lambda: Orchestrates the workflow, processes the images, and triggers other AWS services. AWS Rekognition: Analyzes uploaded images for inappropriate content. DynamoDB: Stores image metadata, moderation results, and logs for future reference. Notifications Amazon SES: Sends alert notifications to administrators or users when inappropriate content is detected.
