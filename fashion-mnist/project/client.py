'''
This code calls the AWS SageMaker endpoint
'''
import boto3
import cv2, os, sys
import json 
import numpy as np
 
from PIL import Image 
from io import BytesIO
#file_name = 'images/24.jpg'
file_name = 'images/51.jpg'
endpoint_name='mnist-notebook-v1'

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


class NumpyArrayEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, np.ndarray):
            return obj.tolist()
        return json.JSONEncoder.default(self, obj)


try:
    runtime = boto3.Session().client(service_name='sagemaker-runtime', region_name='us-east-1')
   
    image = cv2.imread(file_name)
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


    data = json.dumps({"signature_name": "serving_default", "instances": imagearr }, cls=NumpyArrayEncoder)
    #print(data)

    resp = runtime.invoke_endpoint(EndpointName=endpoint_name, ContentType='application/json', Body=data)
    preds = resp['Body'].read().decode()  # byte array
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

    #{'response': resp}
except:
    print(sys.exc_info()[0]) 
