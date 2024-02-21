# TrackSSL

## Description

This Python script automates the process of adding hosts to be monitored for SSL certificate status using the TrackSSL API. It retrieves an API key from AWS Secrets Manager and uses this key to authenticate and add a specified host to the TrackSSL monitoring service.

## Installation

1. `python3 -m venv track-ssl`
2. `pip install -r requirements.txt`

- AWS CLI configured with appropriate credentials that have permissions to access AWS Secrets Manager.
- An API key for TrackSSL stored in AWS Secrets Manager under the `example/track-ssl-key` secret.

## Configuration

1. **AWS CLI Setup**: Ensure your AWS CLI is configured with at least one profile that has permission to access Secrets Manager.
 
2. **Secret in AWS Secrets Manager**: Make sure the `example/track-ssl-key` secret exists in Secrets Manager and contains a valid TrackSSL API key in the following JSON format:
 ```json
 {
   "api-key": "YOUR_TRACKSSL_API_KEY"
 }


## Running Script

1. `cd trackSSL`
2. `source track-ssl/bin/activate`
3. `./trackSSL.py <hostname>`