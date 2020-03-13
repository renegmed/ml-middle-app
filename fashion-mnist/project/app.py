from chalice import Chalice
from chalice import BadRequestError 
import os, sys
import boto3
import json 
import numpy as np
 
from PIL import Image 
from io import BytesIO


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
 
def classify(predictions):
    # It looks like a 2-D array, let's check its shape
    pred = np.array(predictions['predictions'])
    print("Pred:{}".format(pred))

    # # This is the N x K output array from the model
    # # pred[n,k] is the probability that we believe the nth sample belongs to the kth class

    # # Get the predicted classes
    pred = pred.argmax(axis=1)
    print("Pred argmax:{}".format(pred))

    print("Predicted label: {}".format(labels[pred[0]])) 

    return labels[pred[0]]

def predict(data):
    try:
        endpoint = os.environ['ENDPOINT_NAME']
    except:
        endpoint = default_endpoint_name

    print("++++ endpoint:\n{}".format(endpoint))
 
    try: 
        
        response = runtime.invoke_endpoint(EndpointName=endpoint, ContentType='application/json', Body=data) 
        preds = response['Body'].read().decode()  # byte array
        print("+++++ response:\n{}".format(preds)) 
        return classify(preds) 
       
    except:

        return sys.exc_info()[0] 

    
@app.route('/', methods=['POST'],  content_types=['image/jpeg','image/jpg','image/png'], cors=True)
def index():
 
    image = Image.open(BytesIO(app.current_request.raw_body)) 
  
    print("Image size: {}".format(image.size))  
    
    if image.size != (28,28):
        return {'response': "Error: image must be a size of 28 x 28 pix not " + str(image.shape)}
        
        # transform colored image to grayscale
        # image = np.mean(image, axis=2)
        # print("Shape after grayscale conversion: {}".format(image.shape))
        # image = cv2.resize(image, (28,28) )
        # print("Resized Image size: {}".format(image.size))
        # print(image.shape)

    # transform colored image to grayscale
    #image = np.mean(image, axis=2)
    imagearr = np.asarray(image)
    imagearr = imagearr / 255.0
   
    imagearr = imagearr.reshape(-1, 28, 28, 1) 

    # print(imagearr) 
    # data = json.dumps({"signature_name": "serving_default", "instances": imagearr }, cls=NumpyArrayEncoder)
    # return {'response': data }

    data = json.dumps({"signature_name": "serving_default", "instances": imagearr }, cls=NumpyArrayEncoder)
    #print(data) 

    # # call aws lambda requires import boto3 not requests
    pred = predict(data) 
    
    print("Predictions: {}".format(pred))
    
    # convert to json before return
    return json.dumps({'response': pred}) 
    