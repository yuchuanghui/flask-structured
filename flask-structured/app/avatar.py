import time
import hmac
import hashlib
from PIL import Image
from io import BytesIO
import base64
import json
import requests
from datetime import datetime
import os

def get_authorization(method, key):
    # timestamp
    start_timestamp = time.time()
    expired_time = 3600
    end_timestamp = start_timestamp + expired_time
    key_time = str(start_timestamp) + ";" + str(end_timestamp)

    # sign_key
    secret_id = os.getenv("COS_SECRET_ID")
    secret_key = os.getenv("COS_SECRET_KEY")
    sign_key = hmac.new(secret_key.encode('utf-8'), key_time.encode('utf-8'), hashlib.sha1).hexdigest()

    # list
    url_param_list = ''
    http_param = ''
    http_headers = ''
    header_list = ''
    
    http_method = f'{method}'
    http_uri = f'{key}'
    http_str = http_method + '\n' + http_uri + '\n' + http_param + '\n' + http_headers + '\n'

    sha1_http_str = hashlib.sha1(http_str.encode('utf-8')).hexdigest()
    str_to_sign = f'sha1\n{key_time}\n{sha1_http_str}\n'
    signature = hmac.new(sign_key.encode('utf-8'), str_to_sign.encode('utf-8'), hashlib.sha1).hexdigest()

    q_algorithm = 'q-sign-algorithm=sha1'
    q_ak = f'&q-ak={secret_id}'
    q_sign_time = f'&q-sign-time={key_time}'
    q_key_time = f'&q-key-time={key_time}'
    q_header_list = f'&q-header-list={header_list}'
    q_url_param_list = f'&q-url-param-list={url_param_list}'
    q_signature = f'&q-signature={signature}'

    authorization = q_algorithm + q_ak + q_sign_time + q_key_time + q_header_list + q_url_param_list + q_signature

    return authorization

def show_avatar(method, key):
    authorization = get_authorization(method, key)
    headers = {'Authorization': authorization}
    url = 'https://flask-media-1305646899.cos.ap-beijing.myqcloud.com' + key
    r = requests.get(url=url, headers=headers)
    return(r.content)

def upload_avatar(name, image, type):
    start_sign_time = int(time.time())
    time_expire = 10000
    sign_time = "{bg_time};{ed_time}".format(bg_time=start_sign_time - 60, ed_time=start_sign_time + time_expire)
    secret_key = b"RbU7TYLr76oFPIuFJ6crqXx6zbwzlGUR"
    sign_key = hmac.new(secret_key, sign_time.encode('utf-8'), hashlib.sha1).hexdigest()

    expiration = datetime.fromtimestamp(start_sign_time + time_expire).isoformat() + 'Z'
    condition = [
        # {"acl": "private"},
        {"bucket": "flask-media-1305646899"},
        # ["starts-with", "$key", "photo"],
        # ["starts-with", "$Content-Type", "image/"],
        # ["starts-with", "$success_action_redirect", "https://my.website/"],
        # ["eq", "$x-cos-server-side-encryption", "AES256"],
        {"q-sign-algorithm": "sha1"},
        {"q-ak": "AKIDrXx63j8G7i24pKcePu74j7E4dvxiCPM2"},
        {"q-sign-time": sign_time},
        {"key": name}
    ]
    policy = json.dumps({"expiration": expiration, "conditions": condition})

    string_to_sign = hashlib.sha1(policy.encode('utf-8')).hexdigest()
    signature = hmac.new(sign_key.encode('utf-8'), string_to_sign.encode('utf-8'), hashlib.sha1).hexdigest()

    data = {

        # "bucketName": (None, 'avatar'),
        # "type'": (None, 'image'),
        # "x-cos-security-token": ,
        "policy": base64.b64encode(policy.encode('utf-8')),
        "q-sign-algorithm": 'sha1',
        "q-ak": "AKIDrXx63j8G7i24pKcePu74j7E4dvxiCPM2",
        "q-key-time": sign_time,
        "q-signature": signature,
        "key": name,
        "file": (name, image, type),
    }

    r = requests.post("https://flask-media-1305646899.cos.ap-beijing.myqcloud.com", files=data)

    return True
# i = Image.open(BytesIO(r.content))
# i.show()