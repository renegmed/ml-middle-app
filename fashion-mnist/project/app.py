from chalice import Chalice
from chalice import BadRequestError

import base64, cv2, os, sys
import boto3
import json 
import numpy as np
 
from PIL import Image 
from io import BytesIO
#import requests

app = Chalice(app_name='fashion-mnist')
app.debug = True 

default_endpoint_name='mnist-notebook-v1'

# Label mapping
labels = '''T-shirt/top
Trouser
Pullover
Dress
Coat
Sandal
Shirt
Sneaker
Bag
Ankle boot'''.split("\n")

runtime = boto3.Session().client(service_name='sagemaker-runtime', region_name='us-east-1')

class NumpyArrayEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, np.ndarray):
            return obj.tolist()
        return json.JSONEncoder.default(self, obj)

@app.route('/', methods=['POST'],  content_types=['image/jpeg','image/jpg','image/png'], cors=True)
def index():
 
    image = Image.open(BytesIO(app.current_request.raw_body)) 
  
    print("Image size: {}".format(image.size))  
    
    if image.size != (28,28):
        
        # transform colored image to grayscale
        image = np.mean(image, axis=2)
        print("Shape after grayscale conversion: {}".format(image.shape))
        image = cv2.resize(image, (28,28) )
        print("Resized Image size: {}".format(image.size))
        print(image.shape)
     
    imagearr = np.asarray(image)
    imagearr = imagearr / 255.0
   
    imagearr = imagearr.reshape(-1, 28, 28, 1) 

    # print(imagearr) 
    # data = json.dumps({"signature_name": "serving_default", "instances": imagearr }, cls=NumpyArrayEncoder)
    # return {'response': data }



    data = json.dumps({"signature_name": "serving_default", "instances": imagearr }, cls=NumpyArrayEncoder)
    
    print(data)

    # headers = {"content-type": "application/json"} 
    # r = requests.post('http://localhost:8080/invocations', data=data, headers=headers)
    # j = r.json()
    # #print(j.keys())
    # #print(j)

    # # It looks like a 2-D array, let's check its shape
    # pred = np.array(j['predictions'])
     
    # # This is the N x K output array from the model
    # # pred[n,k] is the probability that we believe the nth sample belongs to the kth class

    # # Get the predicted classes
    # pred = pred.argmax(axis=1)

    # # Map them back to strings
    # pred = [labels[i] for i in pred]
    # print("Predicted label: {}".format(pred)) 

    # return {'response': pred}




    # if 'ENDPOINT_NAME' not in os.environ:         
    #     return {'response': 'Missing endpoint'}
    #     #raise BadRequestError('Missing endpoint')
    
    try:
        endpoint = os.environ['ENDPOINT_NAME']
    except:
        endpoint = default_endpoint_name

    # if 'ENDPOINT_NAME' not in os.environ: 
    #     endpoint = default_endpoint_name

    print("++++ endpoint:\n{}".format(endpoint))
 
    try: 
        
        response = runtime.invoke_endpoint(EndpointName=endpoint, ContentType='application/json', Body=data) 
        preds = response['Body'].read().decode()  # byte array
        print("+++++ response:\n{}".format(preds))
 
        j =  json.loads(preds)
        print(j.keys())
        print(j)

        # It looks like a 2-D array, let's check its shape
        pred = np.array(j['predictions'])
        print("Pred:{}".format(pred))

        # # This is the N x K output array from the model
        # # pred[n,k] is the probability that we believe the nth sample belongs to the kth class

        # # Get the predicted classes
        pred = pred.argmax(axis=1)
        print("Pred argmax:{}".format(pred))

        print("Predicted label: {}".format(labels[pred[0]])) 

        return {'response': labels[pred[0]]}
    except:

        return {'response': sys.exc_info()[0]} 

    