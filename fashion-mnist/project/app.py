from chalice import Chalice
from chalice import BadRequestError
import base64, cv2, os 
#import boto3
import json
# import ast
import numpy as np
 

app = Chalice(app_name='fashion-mnist')
app.debug = True

@app.route('/', methods=['POST'])
def index():

    body = app.current_request.json_body #.json_body

    #print("+++++ body:\n{}".format(body))

    if 'data' not in body:
        raise BadRequestError('Missing image data')
    if 'height' not in body:
        raise BadRequestError('Missing image height')
    if 'width' not in body:
        raise BadRequestError('Missing image width')

    height = body['height']
    width = body['width']

    print("++++++ height: {}  weight: {}".format(height, width))

    # if 'ENDPOINT_NAME' not in os.environ:
    #     raise BadRequestError('Missing endpoint')

    # image = base64.b64decode(body['data'])  # byte array
   

    
    image = base64.b64decode(body['data'])

    length = len(image)

    image = np.fromstring(image, np.uint8)
    image = cv2.imdecode(image, cv2.IMREAD_COLOR)
    (H, W, _) = image.shape
    image = cv2.resize(image, (height, width,))
    image = cv2.imencode('.jpeg', image) 

    if 'ENDPOINT_NAME' not in os.environ:
        raise BadRequestError('Missing endpoint')
    
    endpoint = os.environ['ENDPOINT_NAME']
    print("++++ endpoint:\n{}".format(endpoint))
 
    runtime = boto3.Session().client(service_name='sagemaker-runtime', region_name='us-east-1')
    response = runtime.invoke_endpoint(EndpointName=endpoint, ContentType='application/x-image', Body=image)
    resp = response['Body'].read().decode()  # byte array

    print("+++++ response:\n{}".format(resp))

    
    return {'response': resp}
 
    # return {'response': 'hello world!!!'}

    