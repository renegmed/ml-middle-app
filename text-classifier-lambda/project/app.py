from chalice import Chalice
from chalice import BadRequestError
import base64, os 
import boto3
import json
# import ast
#import numpy as np
 

app = Chalice(app_name='text-classifier')


@app.route('/', methods=['POST'],  content_types=['application/json'])
def index():
    body = app.current_request.json_body


    if 'input' not in body:
        raise BadRequestError('Missing image data')

    print("+++++ body:\n{}".format(body))

    if 'ENDPOINT_NAME' not in os.environ:
        raise BadRequestError('Missing endpoint')

    # image = base64.b64decode(body['data'])  # byte array
    endpoint = os.environ['ENDPOINT_NAME']

    print("++++ endpoint:\n{}".format(endpoint))
 
    # convert to string
    payload = json.dumps(body)   # bytearray(body)
    print("+++++ payload type: {}".format(type(payload)))

    runtime = boto3.Session().client(service_name='sagemaker-runtime', region_name='us-east-1')
    response = runtime.invoke_endpoint(EndpointName=endpoint, ContentType='application/json', Body=payload)
    resp = response['Body'].read().decode()  # byte array

    print("+++++ response:\n{}".format(resp))

    return {'response': resp}

    # probs = ast.literal_eval(probs)  # array of floats
    # probs = np.array(probs)   # numpy array of floats

    # topk_indexes = probs.argsort()  # indexes in ascending order of probabilities
    # topk_indexes = topk_indexes[::-1][:topk] # indexes for top k probabilities in descending order

    # topk_categories = []
    # for i in topk_indexes:
    #     topk_categories.append((i+1, probs[i]))

    # return {'response': str(topk_categories)}

    