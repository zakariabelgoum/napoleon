import requests
import boto3
import json
from requests.auth import AuthBase
from datetime import datetime
import hashlib
import hmac

# Amazon credentials (replace with your actual credentials)
aws_access_key_id = 'YOUR_AWS_ACCESS_KEY_ID' #done
aws_secret_access_key = 'YOUR_AWS_SECRET_ACCESS_KEY' #done
lwa_client_id = 'YOUR_LWA_CLIENT_ID' #solene
lwa_client_secret = 'YOUR_LWA_CLIENT_SECRET' #solene
refresh_token = 'YOUR_REFRESH_TOKEN'  #do later
region = 'us-east-1' #zak
marketplace_id = 'YOUR_MARKETPLACE_ID' #zak
seller_id = 'YOUR_SELLER_ID' #solene

# Generate an access token using Login with Amazon (LWA)
def get_access_token():
    url = "https://api.amazon.com/auth/o2/token"
    payload = {
        "grant_type": "refresh_token",
        "client_id": lwa_client_id,
        "client_secret": lwa_client_secret,
        "refresh_token": refresh_token
    }
    headers = {"Content-Type": "application/x-www-form-urlencoded;charset=UTF-8"}
    response = requests.post(url, data=payload, headers=headers)
    return response.json()["access_token"]

# Signature for SP-API using AWS Signature Version 4
class AWSSigV4(AuthBase):
    def __init__(self, access_key, secret_key, region, service, request_parameters):
        self.access_key = access_key
        self.secret_key = secret_key
        self.region = region
        self.service = service
        self.request_parameters = request_parameters

    def __call__(self, request):
        t = datetime.utcnow()
        amz_date = t.strftime('%Y%m%dT%H%M%SZ')
        date_stamp = t.strftime('%Y%m%d')  # Date w/o time, used in credential scope

        # Create a canonical request
        canonical_uri = request.path_url
        canonical_headers = 'host:' + request.url.split("/")[2] + '\n'
        signed_headers = 'host'
        payload_hash = hashlib.sha256((self.request_parameters).encode('utf-8')).hexdigest()
        canonical_request = f"{request.method}\n{canonical_uri}\n\n{canonical_headers}\n{signed_headers}\n{payload_hash}"

        # Create the string to sign
        algorithm = 'AWS4-HMAC-SHA256'
        credential_scope = f"{date_stamp}/{self.region}/{self.service}/aws4_request"
        string_to_sign = f"{algorithm}\n{amz_date}\n{credential_scope}\n" + hashlib.sha256(canonical_request.encode('utf-8')).hexdigest()

        # Calculate the signature
        def sign(key, msg):
            return hmac.new(key, msg.encode('utf-8'), hashlib.sha256).digest()

        k_date = sign(('AWS4' + self.secret_key).encode('utf-8'), date_stamp)
        k_region = sign(k_date, self.region)
        k_service = sign(k_region, self.service)
        k_signing = sign(k_service, 'aws4_request')
        signature = hmac.new(k_signing, (string_to_sign).encode('utf-8'), hashlib.sha256).hexdigest()

        # Add signing information to the request headers
        authorization_header = (
            f"{algorithm} Credential={self.access_key}/{credential_scope}, SignedHeaders={signed_headers}, Signature={signature}"
        )

        headers = request.headers
        headers['x-amz-date'] = amz_date
        headers['Authorization'] = authorization_header
        return request

# Function to get listings from SP-API
def get_listings_item(sku):
    access_token = get_access_token()
    url = f"https://sellingpartnerapi-na.amazon.com/listings/2021-08-01/items/{seller_id}/{sku}?marketplaceIds={marketplace_id}"
    
    headers = {
        "x-amz-access-token": access_token,
        "Content-Type": "application/json"
    }

    # Add the AWS signature
    response = requests.get(url, headers=headers, auth=AWSSigV4(aws_access_key_id, aws_secret_access_key, region, 'execute-api', '{}'))
    if response.status_code == 200:
        return response.json()
    else:
        print("Error:", response.status_code, response.text)
        return None

# Test the function
sku = 'YOUR_PRODUCT_SKU'  # Replace with the SKU of the product you want to retrieve
listing_info = get_listings_item(sku)
print(json.dumps(listing_info, indent=4))
