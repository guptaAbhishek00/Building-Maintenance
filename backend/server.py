from flask import Flask, request, jsonify
from flask_cors import CORS
import boto3
import uuid
import datetime
import os
from env import *

s3 = boto3.client(
    "s3",
    aws_access_key_id=AWS_ACCESS_KEY,
    aws_secret_access_key=AWS_SECRET_ACCESS_KEY
)

app = Flask(__name__)
CORS(app)

def upload_to_s3(file_name, s3_file_name, bucket, ): 
    """ 
    Uploads a file to S3. 
    Usage: 
    upload_to_s3('local_file.jpg', 's3_path/to/save/file.jpg', 'bucket_name', 
    'YOUR_AWS_ACCESS_KEY', 'YOUR_AWS_SECRET_KEY') 

    """ 
    try: 
        s3.upload_file(file_name, bucket, s3_file_name, ExtraArgs={'ACL':'public-read'}) 
        return f"https://{bucket}.s3.amazonaws.com/{s3_file_name}" 
    except FileNotFoundError: 
        print("The file was not found") 
        return False 
    except Exception as e: 
        print(e) 
        return False
    

# bill upload route
# TODO: add this url to the csv data. Take the index for the row in the csv to modify it's url field
@app.route('/upload_bill', methods=['POST'])
def upload():
    try:
        image = request.files['image']
        if not image:
            return jsonify({'error': 'No image provided'}), 400

        # random file name
        fileName = 'uploads/bap_{}{:-%Y%m%d%H%M%S}.jpeg'.format(str(uuid.uuid4().hex), datetime.datetime.now())
        # store locally to uploads/
        image.save(f'{fileName}')
        # upload the image to s3
        url = upload_to_s3(fileName, fileName, AWS_BUCKET_NAME)
        # delete the image from uploads/
        os.remove(f'{fileName}')
        if not url:
            return jsonify({'error': 'Error uploading the image'}), 500
        return jsonify({'url': url}), 200
    except Exception as e:
        print(e)
        return jsonify({'error': 'Error uploading the image'}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=3001, debug=True)