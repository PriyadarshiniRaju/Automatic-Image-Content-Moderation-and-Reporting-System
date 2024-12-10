import streamlit as st
import boto3
import os

# Fetch AWS credentials from environment variables
aws_access_key = os.getenv('AWS_ACCESS_KEY_ID')
aws_secret_key = os.getenv('AWS_SECRET_ACCESS_KEY')
aws_region = os.getenv('AWS_DEFAULT_REGION')

# Use the credentials to create an S3 client
s3_client = boto3.client('s3',
                         aws_access_key_id=aws_access_key,
                         aws_secret_access_key=aws_secret_key,
                         region_name=aws_region)

# Streamlit file uploader
uploaded_file = st.file_uploader("Choose an image",
                                 type=["jpg", "jpeg", "png"])

if uploaded_file is not None:
    # Define S3 bucket and key
    s3_bucket = 'imagemoderationbucket'
    s3_key = f"images/{uploaded_file.name}"

    # Upload the file to S3
    s3_client.upload_fileobj(
        uploaded_file,
        s3_bucket,
        s3_key,
        ExtraArgs={'Metadata': {
            'user_email': 'user1@example.com'
        }})

    st.success(f"File uploaded to {s3_bucket}/{s3_key}")
