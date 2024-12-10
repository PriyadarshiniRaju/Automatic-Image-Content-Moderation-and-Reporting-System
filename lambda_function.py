import boto3
import uuid
from datetime import datetime
import urllib.parse
 
# Initialize the AWS clients
rekognition_client = boto3.client('rekognition',region_name='us-west-2')
s3_client = boto3.client('s3')
dynamodb = boto3.resource('dynamodb')
ses_client = boto3.client('ses')
 
# DynamoDB table name
dynamodb_table = 'ImageModerationMetadata'
 
# S3 bucket names
final_bucket_safe = 'imagemoderation-safepics'
final_bucket_violent = 'imagemoderation-violentpics'
 
# SES email recipient
email_recipient = 'youremail@domain.com'
 
def lambda_handler(event, context):
    # Extract the S3 bucket name and object key from the event trigger
    bucket_name = event['Records'][0]['s3']['bucket']['name']
    s3_key = event['Records'][0]['s3']['object']['key']
   
    # Generate a unique ImageID (could be S3 key or a UUID)
    image_id = str(uuid.uuid4())
 
    # URL encode the S3 key
    s3_key_encoded = urllib.parse.quote_plus(s3_key)
   
    # Get the image metadata (user email, etc.) from S3 object metadata (if stored)
    try:
        metadata = s3_client.head_object(Bucket=bucket_name, Key=s3_key)
        user_email = metadata.get('Metadata', {}).get('user_email', 'unknown')
    except s3_client.exceptions.ClientError as e:
        print(f"Error retrieving metadata for {s3_key}: {str(e)}")
        user_email = 'unknown'  # Default value when metadata is not found
 
    # Use Rekognition to analyze the image for moderation labels
    rekognition_response = rekognition_client.detect_moderation_labels(
        Image={'S3Object': {'Bucket': bucket_name, 'Name': s3_key}}
    )
   
    # Check if the image contains any violent or inappropriate content
    is_violent = False
    for label in rekognition_response['ModerationLabels']:
        if label['Name'].lower() in ['violence', 'explicit', 'gore','blood','partial nudity','nudity','drug','death','drug abuse','smoking','drinking']:  # You can add other labels if necessary
            is_violent = True
            break
 
    # Categorize the image based on the results
    if is_violent:
        final_bucket = final_bucket_violent
        category = 'violent'
    else:
        final_bucket = final_bucket_safe
        category = 'safe'
 
    # Prepare the new S3 key (optional - change to avoid overwriting original file)
    new_s3_key = f"{category}/{image_id}_{s3_key.split('/')[-1]}"  # Create a new key with category and unique ID
 
    # Copy the image to the respective S3 bucket (violent or safe)
    try:
        s3_client.copy_object(
            Bucket=final_bucket,
            CopySource={'Bucket': bucket_name, 'Key': s3_key},
            Key=new_s3_key
        )
    except Exception as e:
        print(f"Error copying object: {e}")
        return {
            'statusCode': 500,
            'body': 'Error copying the image to the target bucket.'
        }
   
    # Prepare the metadata to store in DynamoDB
    upload_time = datetime.utcnow().isoformat()
    final_record = {
        'ImageID': image_id,
        'ImageCategory': category,
        'UploadTime': upload_time,
        'OriginalBucket': bucket_name,
        'FinalBucket': final_bucket,
        'S3Key': new_s3_key,  # Store the new S3 key
        'UserEmail': user_email
    }
 
    # Insert the metadata into DynamoDB
    table = dynamodb.Table(dynamodb_table)
    table.put_item(Item=final_record)
 
    # Send an email notification if the image is flagged as violent
    if category == 'violent':
        send_email_notification(user_email, s3_key)
 
    return {
        'statusCode': 200,
        'body': 'Image processed successfully.'
    }
 
def send_email_notification(user_email, s3_key):
    # Create the email body
    subject = "Inappropriate Image Alert"
    body = f"An image you uploaded with key {s3_key} has been flagged as inappropriate and moved to the 'violent' bucket. Please review the image content."
 
    # Send email via SES
    ses_client.send_email(
        Source='youremail@domain.com',  # Replace with your domain
        Destination={'ToAddresses': [email_recipient]},
        Message={
            'Subject': {'Data': subject},
            'Body': {'Text': {'Data': body}}
        }
    )
